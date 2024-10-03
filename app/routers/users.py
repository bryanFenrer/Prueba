from fastapi import APIRouter
from app.schemas.users import UserSchema, UserUpdateSchema, UserDesactivateSchema
from app.schemas.response import Response
from typing import List
from ..services.userService import UserService

router_users = APIRouter(
    prefix ="/users",
    tags=["Users"]
)

#Registrar Usuario
@router_users.post('/register')
async def register_user(input:UserSchema):
    response:Response = await UserService().register(input)
    return response

#Obtener todos los roles de usuario
@router_users.get('/get-all')
async def get_all_users():
    response:Response = await UserService().get_all_users()
    return response

#Actualizar rol de usuario
@router_users.put('/update')
async def update_user(input:UserUpdateSchema):
    response:Response = await UserService().update(input)
    return response

#Desactivar rol de usuario
@router_users.delete('/desactivate')
async def desactivate_user(input:UserDesactivateSchema):
    response:Response = await UserService().desactivate(input)
    return response

#Iniciar sesión