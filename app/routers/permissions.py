from fastapi import APIRouter
from app.schemas.permissions import PermissionSchema, PermissionUpdateSchema, PermissionDesactivateSchema
from app.schemas.response import Response
from typing import List
from ..services.permissionService import PermissionService

router_permissions = APIRouter(
    prefix ="/permissions",
    tags=["Permissions"]
)

#Registrar permiso
@router_permissions.post('/register')
async def register_permission(input:PermissionSchema):
    response:Response = await PermissionService().register(input)
    return response


#Obtener permiso
@router_permissions.get('/get-all')
async def get_all_permission():
    response:Response = await PermissionService().get_all_permissions()
    return response

#Actualizar permiso
@router_permissions.put('/update')
async def update_permission(input:PermissionUpdateSchema):
    response:Response = await PermissionService().update(input)
    return response

#Desactivar permiso
@router_permissions.delete('/desactivate')
async def desactivate_permission(input:PermissionDesactivateSchema):
    response:Response = await PermissionService().desactivate(input)
    return response