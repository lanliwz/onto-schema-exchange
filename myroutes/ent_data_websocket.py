from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import json
import asyncio

router = APIRouter()
# Example seed graph data
N = lambda key, type, label, subtitle="": {"key": key, "type": type, "label": label, "subtitle": subtitle}
L = lambda from_, to, label: {"from": from_, "to": to, "label": label}

seed_nodes = [
    N("u_alice", "User", "user-alice", "Finance + All Employees"),
    N("u_bob", "User", "user-bob", "Client Support + All Employees"),
    N("u_carol", "User", "user-carol", "IT + All Employees"),

    N("pg_all", "PolicyGroup", "All Employees", "bundle: mask_salary_v1"),
    N("pg_fin", "PolicyGroup", "Finance Group", "row_filter_finance_only"),
    N("pg_hr", "PolicyGroup", "HR Group", "row_filter_hr_only"),
    N("pg_it", "PolicyGroup", "IT Group", "row_filter_it_only"),
    N("pg_cs", "PolicyGroup", "Client Support Team", "no mask policy"),

    N("p_mask", "Policy", "mask_salary_v1", "Mask Salary"),
    N("p_fin", "Policy", "row_filter_finance_only", "dept_name = 'Finance'"),
    N("p_hr", "Policy", "row_filter_hr_only", "dept_name = 'HR'"),
    N("p_it", "Policy", "row_filter_it_only", "dept_name = 'IT'"),

    N("s_bank", "Schema", "bank", "Schema"),
    N("t_emp", "Table", "employee", "Table"),
    N("t_dep", "Table", "department", "Table"),
    N("c_sal", "Column", "salary", "Column of employee"),
    N("c_dnm", "Column", "dept_name", "Column of department"),
]

seed_links = [
    L("u_alice", "pg_all", "memberOf"),
    L("u_alice", "pg_fin", "memberOf"),
    L("u_bob", "pg_all", "memberOf"),
    L("u_bob", "pg_cs", "memberOf"),
    L("u_carol", "pg_all", "memberOf"),
    L("u_carol", "pg_it", "memberOf"),

    L("pg_all", "p_mask", "includesPolicy"),
    L("pg_fin", "p_fin", "includesPolicy"),
    L("pg_hr", "p_hr", "includesPolicy"),
    L("pg_it", "p_it", "includesPolicy"),

    L("p_mask", "c_sal", "hasColumnRule"),
    L("p_fin", "c_dnm", "hasRowRule"),
    L("p_hr", "c_dnm", "hasRowRule"),
    L("p_it", "c_dnm", "hasRowRule"),

    L("t_emp", "s_bank", "belongsToSchema"),
    L("t_dep", "s_bank", "belongsToSchema"),
    L("c_sal", "t_emp", "belongsToTable"),
    L("c_dnm", "t_dep", "belongsToTable"),
]

connected_clients: List[WebSocket] = []


@router.websocket("/ws-ent-model")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    print("✅ Client connected:", websocket.client)

    # Send initial graph
    await websocket.send_json({
        "type": "full_graph",
        "nodes": seed_nodes,
        "links": seed_links
    })

    try:
        while True:
            msg = await websocket.receive_text()
            data = json.loads(msg)
            print("📩 Received:", data)
            if data.get("type") in {"hello", "request_full"}:
                await websocket.send_json({
                    "type": "full_graph",
                    "nodes": seed_nodes,
                    "links": seed_links
                })
            elif data.get("type") == "ping":
                await websocket.send_json({"type": "pong", "t": data.get("t")})
            else:
                await websocket.send_json({"type": "info", "message": "Unknown message type"})
    except WebSocketDisconnect:
        print("❌ Client disconnected:", websocket.client)
        connected_clients.remove(websocket)
    except Exception as e:
        print("⚠️ WebSocket error:", e)
        if websocket in connected_clients:
            connected_clients.remove(websocket)


# Optional: broadcast function for updates
async def broadcast_update(update: dict):
    """Send an incremental update to all connected clients."""
    msg = json.dumps(update)
    for ws in list(connected_clients):
        try:
            await ws.send_text(msg)
        except Exception:
            connected_clients.remove(ws)