from pydantic import BaseModel 
#from datetime import datetime
from typing import Optional, Literal

class RoleSchema(BaseModel):
    name:Literal['administrador','manager','ventas']
    description:str

class RoleUpdateSchema(RoleSchema):
    id:int

class RoleDesactivateSchema(BaseModel):
    id:int
    status:Literal['active','inactive']