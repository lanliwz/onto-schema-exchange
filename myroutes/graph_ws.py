# routes/graph_ws.py
from __future__ import annotations

import asyncio
import json
import os
from typing import List, Dict, Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi import HTTPException
from neo4j import GraphDatabase, Driver

router = APIRouter()

# -----------------------------
# Neo4j connection (env-driven)
# -----------------------------
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASS", "neo4j0001")

driver: Driver | None = None
try:
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
except Exception as e:
    print("⚠️ Could not initialize Neo4j driver:", e)


# -----------------------------
# Clients registry + helpers
# -----------------------------
connected_clients: List[WebSocket] = []

def _label_fallback(props: Dict[str, Any], type_hint: str) -> str:
    """
    Try to pick a sensible display label for different node kinds.
    Extend this mapping to your property schema.
    """
    candidates_by_type = {
        "User":       ["label", "name", "userId", "username", "rdfs__label"],
        "PolicyGroup":["label", "policy_group_name", "name", "rdfs__label"],
        "Policy":     ["label", "policy_name", "name", "rdfs__label"],
        "Column":     ["label", "column_name", "name", "rdfs__label"],
        "Table":      ["label", "table_name", "name", "rdfs__label"],
        "Schema":     ["label", "schema_name", "name", "rdfs__label"],
    }
    for k in candidates_by_type.get(type_hint, ["label", "name", "rdfs__label"]):
        v = props.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    # nothing matched; last resort: first non-empty string prop
    for v in props.values():
        if isinstance(v, str) and v.strip():
            return v.strip()
    return type_hint

def _subtitle_fallback(props: Dict[str, Any]) -> str:
    for k in ["subtitle", "definition", "skos__definition", "desc", "note"]:
        v = props.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""

async def _broadcast(update: dict):
    msg = json.dumps(update)
    for ws in list(connected_clients):
        try:
            await ws.send_text(msg)
        except Exception:
            try:
                connected_clients.remove(ws)
            except ValueError:
                pass

# -----------------------------
# Neo4j fetchers
# -----------------------------
NODE_TYPES = ["User", "PolicyGroup", "Policy", "Column", "Table", "Schema"]
REL_TYPES  = ["memberOf", "includesPolicy", "hasColumnRule", "hasRowRule",
              "belongsToTable", "belongsToSchema"]

def _fetch_graph_from_neo4j() -> dict:
    """
    Query Neo4j for the nodes/links we care about and adapt to GoJS model shape.
    Uses elementId(*) for stable keys.
    """
    if driver is None:
        raise RuntimeError("Neo4j driver is not initialized")

    with driver.session() as session:
        # Nodes
        node_records = session.run(
            """
            MATCH (n)
            WHERE any(l IN labels(n) WHERE l IN $keep)
            RETURN elementId(n) AS key, labels(n) AS labels, n AS props
            """,
            keep=NODE_TYPES,
        )

        nodes = []
        for rec in node_records:
            key: str = rec["key"]


            labels: list[str] = rec["labels"] or []
            props: Dict[str, Any] = dict(rec["props"]) if rec["props"] else {}
            # We prefer the "primary" label that matches the types we expect
            type_hint = next((l for l in labels if l in NODE_TYPES), labels[0] if labels else "Node")
            nodes.append({
                "key": key,
                "type": type_hint,
                "label": _label_fallback(props, type_hint),
                "subtitle": _subtitle_fallback(props),
                # you can surface raw props to the frontend if desired:
                # "__props": props
            })

        # Relationships
        rel_records = session.run(
            """
            MATCH (a)-[r]->(b)
            WHERE type(r) IN $types
              AND any(la IN labels(a) WHERE la IN $keep)
              AND any(lb IN labels(b) WHERE lb IN $keep)
            RETURN elementId(r) AS rid,
                   elementId(a) AS from,
                   elementId(b) AS to,
                   type(r)       AS label,
                   r             AS rprops
            """,
            types=REL_TYPES,
            keep=NODE_TYPES,
        )

        links = []
        for rec in rel_records:
            rid: str = rec["rid"]
            links.append({
                # key is optional for GoJS, but helps if you later want partial updates
                "key": rid,
                "from": rec["from"],
                "to": rec["to"],
                "label": rec["label"],
                # "__props": dict(rec["rprops"]) if rec["rprops"] else {}
            })

        return {"nodes": nodes, "links": links}


# -----------------------------
# WebSocket endpoint
# -----------------------------
@router.websocket("/ws-ent-model")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    print("✅ WS client connected:", websocket.client)

    # On connect: send full graph from Neo4j
    # graph = {"nodes": [...], "links": [...]}
    # {"type": "full_graph", **graph}
    # The **graph syntax unpacks the contents of another dictionary called graph into this one.
    # {"type": "full_graph", "nodes": [...], "links": [...]}
    try:
        graph = _fetch_graph_from_neo4j()
        await websocket.send_json({"type": "full_graph", **graph})
    except Exception as e:
        await websocket.send_json({"type": "info", "message": f"Neo4j load failed: {e}"})

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                await websocket.send_json({"type": "info", "message": "invalid JSON"})
                continue

            mtype = msg.get("type")
            if mtype in {"hello", "request_full"}:
                graph = _fetch_graph_from_neo4j()
                await websocket.send_json({"type": "full_graph", **graph})
            elif mtype == "ping":
                await websocket.send_json({"type": "pong", "t": msg.get("t")})
            else:
                await websocket.send_json({"type": "info", "message": f"Unknown message type: {mtype}"})
    except WebSocketDisconnect:
        print("❌ WS client disconnected:", websocket.client)
        try:
            connected_clients.remove(websocket)
        except ValueError:
            pass
    except Exception as e:
        print("⚠️ WebSocket error:", e)
        try:
            connected_clients.remove(websocket)
        except ValueError:
            pass


# -----------------------------
# Optional: HTTP trigger to push a fresh snapshot to all clients
# -----------------------------
@router.post("/ws/refresh")
async def refresh_from_neo4j_and_broadcast():
    """
    Call this after you write to Neo4j to push a new full snapshot to all WS clients.
    """
    try:
        graph = _fetch_graph_from_neo4j()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Neo4j load failed: {e}")

    await _broadcast({"type": "full_graph", **graph})
    return {"ok": True, "nodes": len(graph["nodes"]), "links": len(graph["links"])}


# -----------------------------
# (Optional) background poller
# -----------------------------
# If you want automatic refresh every N seconds, you can launch this task
# at startup and compute a hash to avoid spamming identical snapshots.

import hashlib

def _fingerprint(graph: dict) -> str:
    # stable-ish hash of the snapshot
    blob = json.dumps(graph, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()

async def periodic_refresh_task(interval_sec: int = 10):
    last_fp = None
    while True:
        try:
            graph = _fetch_graph_from_neo4j()
            fp = _fingerprint(graph)
            if fp != last_fp:
                await _broadcast({"type": "full_graph", **graph})
                last_fp = fp
        except Exception as e:
            # log and keep trying
            print("⚠️ periodic refresh error:", e)
        await asyncio.sleep(interval_sec)