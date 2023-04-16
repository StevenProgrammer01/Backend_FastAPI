from typing import Optional
from pydantic import BaseModel
class User(BaseModel):
    id: None
    username: str
    email:str