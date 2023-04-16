from typing import Optional
from pydantic import BaseModel
class User(BaseModel):
    #id: str
    username: str
    email:str
class User2(BaseModel):
    id: str
    username: str
    email:str