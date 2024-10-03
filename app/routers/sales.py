from fastapi import APIRouter
from app.schemas.roles import RoleSchema, RoleUpdateSchema, RoleDesactivateSchema
from app.schemas.response import Response
from typing import List
from ..services.salesService import SalesService

router_sales = APIRouter(
    prefix ="/sales",
    tags=["Sales"]
)

#Obtener todos los roles de usuario
@router_sales.get('/get-all')
async def get_all_sales():
    response:Response = await SalesService().get_all_sales()
    return response

#Obtener todos los roles de usuario
@router_sales.get('/get-one-sale/{id_sale}')
async def get_one_sale(id_sale:int):
    response:Response = await SalesService().get_one_sale(id_sale)
    return response