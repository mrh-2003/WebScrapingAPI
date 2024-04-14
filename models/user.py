from pydantic import BaseModel
from typing import Union

class User(BaseModel):
    username: str
    disabled:  Union[bool, None] = None