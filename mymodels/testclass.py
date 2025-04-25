from pydantic import BaseModel
from typing import Union


class Item(BaseModel):
    name: str
    price: float = 100
    is_offer: Union[bool, None] = True
    linkDataArray: str
