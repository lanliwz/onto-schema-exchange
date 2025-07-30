from typing import List
from fastapi import APIRouter, Response, WebSocket
import asyncio
import hashlib
import os

from starlette.websockets import WebSocketDisconnect

from gojs_models.er.gojs_er_data_model import Node,Link
from fastapi.responses import JSONResponse, PlainTextResponse

from gojs_models.er.gojs_er_init import init as er_init
from gojs_models.ft.gojs_ft_init import init as ft_init
from js_util import *

from gojs_models.gojs_er_product import product_data_array
from gojs_models.gojs_ft_king import king_george_v_tree_data
from util.file_monitor import PrintingFileWatcher,print_it,get_text
import websockets

router = APIRouter()


data_store = {"message": "Hello from FastAPI!", "timestamp": "2025-02-23 12:00:00"}



def compute_hash(file_path: str) -> str:
    try:
        with open(file_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception:
        return ""

def get_text(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connected, waiting for file path...")

    try:
        # Wait for file path with timeout
        file_path = await asyncio.wait_for(websocket.receive_text(), timeout=300)

        if not os.path.isfile(file_path):
            await websocket.send_text(f"Invalid file path: {file_path}")
            return

        print(f"Started watching: {file_path}")
        last_hash = ""

        while True:
            try:
                # Send heartbeat ping
                await websocket.send_text("__ping__")
                print("__ping__")
                pong = await asyncio.wait_for(websocket.receive_text(), timeout=10)

                if pong != "__pong__":
                    print(f"Invalid pong received: {pong}")
                    break  # or raise Exception("Invalid pong")
                print("__pong__")

                # Check file change
                current_hash = compute_hash(file_path)
                if current_hash and current_hash != last_hash:
                    print(f"File changed: {last_hash} -> {current_hash}")
                    last_hash = current_hash
                    content = get_text(file_path)
                    await websocket.send_text(content)

                await asyncio.sleep(5)

            except WebSocketDisconnect:
                print("WebSocket client disconnected.")
                break
            except Exception as e:
                print("WebSocket error during heartbeat or send:", e)
                break

    except asyncio.TimeoutError:
        await websocket.send_text("Timeout: No file path received in 5 minutes. Closing connection.")
    except WebSocketDisconnect:
        print("WebSocket client disconnected before sending file path.")
    except Exception as e:
        print("WebSocket error before streaming started:", e)
    finally:
        try:
            await websocket.close()
            print("WebSocket closed.")
        except RuntimeError as e:
            # This happens if the connection is already closed
            print("WebSocket already closed:", e)
        except Exception as e:
            print("Error while closing WebSocket:", e)



@router.get("/data", response_class=JSONResponse)
async def get_data():
    return data_store


@router.get("/model/er_model_data.js",response_class=PlainTextResponse)
def get_er_model():
    js = product_data_array.node_to_javascript() + " " + product_data_array.link_to_javascript()
    model_data=remove_js_format(js)
    # print(model_data)
    return Response(content=model_data, media_type="application/javascript")

@router.get("/model/er_model_template.js",response_class=PlainTextResponse)
def get_er_template():
    js = er_init()
    js_template = remove_js_format(js)
    # print(js_template)
    return Response(content=js_template, media_type="application/javascript")

@router.get("/model/ft_model_template.js",response_class=PlainTextResponse)
def get_er_template():
    js_template = ft_init()
    # js_template = remove_js_format(js)
    print(js_template)
    return Response(content=js_template, media_type="application/javascript")

@router.get("/model/ft_model_data.js",response_class=PlainTextResponse)
def get_er_model():
    model_data = king_george_v_tree_data.to_javascript()
    # model_data=remove_js_format(js)
    print(model_data)
    return Response(content=model_data, media_type="application/javascript")


@router.post(path="/model/er_nodes",response_class=JSONResponse)
def save_er_model_node(nodes: List[Node]):
    return {"received": nodes, "count": len(nodes)}


@router.post(path="/model/er_links",response_class=JSONResponse)
def save_er_model_node(links: List[Link]):
    return {"received": links, "count": len(links)}