from pydantic import BaseModel 
from typing import Literal

class PermissionSchema(BaseModel):
    name:str
    description:str

class PermissionUpdateSchema(PermissionSchema):
    id:int

class PermissionDesactivateSchema(BaseModel):
    id:int
    status:Literal['active','inactive']