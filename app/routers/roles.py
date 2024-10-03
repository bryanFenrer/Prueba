from fastapi import APIRouter
from app.schemas.roles import RoleSchema, RoleUpdateSchema, RoleDesactivateSchema
from app.schemas.response import Response
from typing import List
from ..services.roleService import RoleService

router_roles = APIRouter(
    prefix ="/roles",
    tags=["Roles"]
)

#Registrar rol de usuario
@router_roles.post('/register')
async def register_role(input:RoleSchema):
    response:Response = await RoleService().register(input)
    return response


#Obtener todos los roles de usuario
@router_roles.get('/get-all')
async def get_all_role():
    response:Response = await RoleService().get_all_roles()
    return response

#Actualizar rol de usuario
@router_roles.put('/update')
async def update_role(input:RoleUpdateSchema):
    response:Response = await RoleService().update(input)
    return response

#Desactivar rol de usuario
@router_roles.delete('/desactivate')
async def desactivate_role(input:RoleDesactivateSchema):
    response:Response = await RoleService().desactivate(input)
    return response