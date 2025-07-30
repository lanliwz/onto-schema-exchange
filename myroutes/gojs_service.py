from typing import List
from fastapi import APIRouter, Response, WebSocket
import asyncio
import hashlib

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
    except FileNotFoundError:
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
    print("WebSocket connected...")

    file_path = "/Users/weizhang/Downloads/model_data.json"
    check_interval = 2  # seconds
    last_hash = ""

    try:
        while True:
            current_hash = compute_hash(file_path)
            if current_hash and current_hash != last_hash:
                print(f"File changed: {last_hash} -> {current_hash}")
                last_hash = current_hash
                content = get_text(file_path)
                await websocket.send_text(content)
            await asyncio.sleep(check_interval)
    except Exception as e:
        print("WebSocket connection closed or error:", e)
    finally:
        await websocket.close()
        print("WebSocket closed.")


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