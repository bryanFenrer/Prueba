from fastapi import APIRouter
from app.schemas.response import Response
from typing import List
from ..services.manage_permissions import ManagePermissionsService

router_manages = APIRouter(
    prefix ="/manage_Permissions",
    tags=["Manage_Permissions"]
)

#Asignar permiso especial
@router_manages.post('/{id}/assign-permission')
async def assign_permission(id:int):
    response:Response = await ManagePermissionsService().assign(id)
    return response

#Revocar permiso especial
@router_manages.post('/{id}/revoke-permission')
async def revoke_permission(id:int):
    response:Response = await ManagePermissionsService().revoke(id)
    return response