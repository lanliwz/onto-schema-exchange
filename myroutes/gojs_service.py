from typing import Union, List
from fastapi import APIRouter
from fastapi import FastAPI, Response
from sympy import false

from gojs_models.gojs_er_data_model import Node,Link, NodeItem
from fastapi.responses import JSONResponse, PlainTextResponse

from gojs_models.gojs_er_init import *
import re

def remove_js_format(js_code: str) -> str:
    # Remove single-line comments (//)
    js_code = re.sub(r'//.*', '', js_code)
    # Remove multi-line comments (/* ... */)
    js_code = re.sub(r'/\*[\s\S]*?\*/', '', js_code)
    # Remove newlines and excessive whitespace
    js_code = re.sub(r'\s+', ' ', js_code)
    # Remove spaces around symbols
    js_code = re.sub(r'\s*([{}();,:=<>+\-*/&|^%!~\[\]])\s*', r'\1', js_code)
    return js_code.strip()

router = APIRouter()


data_store = {"message": "Hello from FastAPI!", "timestamp": "2025-02-23 12:00:00"}


@router.get("/data", response_class=JSONResponse)
async def get_data():
    return data_store


@router.get("/model/er_model_data.js",response_class=PlainTextResponse)
def get_er_model():
    model_data_array = ModelDataArray(
        nodeDataArray=[
            Node(
                key='Products',
                location=Location(b=250, k=250, h=False),
                items=[
                    NodeItem(name='ProductID', iskey=True, figure='Decision', color='purple'),
                    NodeItem(name='ProductName', iskey=False, figure='Hexagon', color='blue'),
                    NodeItem(name='ItemDescription', iskey=False, figure='Hexagon', color='blue'),
                    NodeItem(name='WholesalePrice', iskey=False, figure='Circle', color='green'),
                    NodeItem(name='ProductPhoto', iskey=False, figure='TriangleUp', color='red'),
                ],
                inheritedItems=[
                    NodeItem(name='SupplierID', iskey=False, figure='Decision', color='purple'),
                    NodeItem(name='CategoryID', iskey=False, figure='Decision', color='purple'),
                ],
            ),
            Node(
                key='Suppliers',
                location=Location(b=500, k=0, h=False),
                items=[
                    NodeItem(name='SupplierID', iskey=True, figure='Decision', color='purple'),
                    NodeItem(name='CompanyName', iskey=False, figure='Hexagon', color='blue'),
                    NodeItem(name='ContactName', iskey=False, figure='Hexagon', color='blue'),
                    NodeItem(name='Address', iskey=False, figure='Hexagon', color='blue'),
                    NodeItem(name='ShippingDistance', iskey=False, figure='Circle', color='green'),
                    NodeItem(name='Logo', iskey=False, figure='TriangleUp', color='red'),
                ]
            ),
            Node(
                key='Categories',
                location=Location(b=0, k=30, h=False),
                items=[
                    NodeItem(name='CategoryID', iskey=True, figure='Decision', color='purple'),
                    NodeItem(name='CategoryName', iskey=False, figure='Hexagon', color='blue'),
                    NodeItem(name='Description', iskey=False, figure='Hexagon', color='blue'),
                    NodeItem(name='Icon', iskey=False, figure='TriangleUp', color='red'),
                ],
                inheritedItems=[
                    NodeItem(name='SupplierID', iskey=False, figure='Decision', color='purple'),
                ],
            ),
            Node(
                key='Order Details',
                location=Location(b=600, k=350, h=False),
                items=[
                    NodeItem(name='OrderID', iskey=True, figure='Decision', color='purple'),
                    NodeItem(name='UnitPrice', iskey=False, figure='Circle', color='green'),
                    NodeItem(name='Quantity', iskey=False, figure='Circle', color='green'),
                    NodeItem(name='Discount', iskey=False, figure='Circle', color='green'),
                ],
                inheritedItems=[
                    NodeItem(name='ProductID', iskey=False, figure='Decision', color='purple'),
                ],
            ),
        ],
        linkDataArray=[
            Link(from_node='Products', to_node='Suppliers', text='0..N', toText='1'),
            Link(from_node='Products', to_node='Categories', text='0..N', toText='1'),
            Link(from_node='Order Details', to_node='Products', text='0..N', toText='1'),
            Link(from_node='Categories', to_node='Suppliers', text='0..N', toText='1'),
        ]

    )
    js = model_data_array.to_javascript()
    model_data=remove_js_format(js)
    # print(model_data)
    return Response(content=model_data, media_type="application/javascript")

@router.get("/model/er_model_template.js",response_class=PlainTextResponse)
def get_er_template():
    js = init()
    js_template = remove_js_format(js)
    # print(js_template)
    return Response(content=js_template, media_type="application/javascript")



@router.post(path="/model/er_nodes",response_class=JSONResponse)
def save_er_model_node(nodes: List[Node]):
    return {"received": nodes, "count": len(nodes)}


@router.post(path="/model/er_links",response_class=JSONResponse)
def save_er_model_node(links: List[Link]):
    return {"received": links, "count": len(links)}