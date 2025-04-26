from typing import Union, List
from fastapi import APIRouter
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, PlainTextResponse

router = APIRouter()

from mymodels.testclass import Item

items: List[Item] = []




@router.get("/items/{item_name}")
def read_item(item_name: str):

    for i in items:
        if i.name == item_name:
            return i

    item = Item(name=item_name)

    return item



@router.put("/items/{item_name}")
def update_item(item: Item):
    for i in items:
        if i.name == item.name:
            i.price=item.price
            i.is_offer=item.is_offer
            return "updated"
    items.append(item)
    return {"update detail": "added"}




