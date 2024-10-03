from pydantic import BaseModel 
#from datetime import datetime
from typing import Optional, Literal

class UserSchema(BaseModel):
    username:str
    password:str
    email:str

class UserUpdateSchema(UserSchema):
    id:int

class UserDesactivateSchema(BaseModel):
    id:int
    status:Literal['active','inactive']