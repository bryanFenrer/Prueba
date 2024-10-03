from app.schemas.response import Response
from app.repository import SalesRepository

class SalesService:
    def __init__(self) -> None:
        pass

    async def get_all_sales(self):
        query_all = await SalesRepository().get_all()

        response: Response = {}
        if not query_all:
            response['status'] = False
            response['status_code'] = 402
            response['message'] = 'Any sale active'
            response['data'] = {}
            return response
        
        response['status'] = True
        response['status_code'] = 200
        response['message'] = 'List sales'
        response['data'] = query_all
        return response
    
    async def get_one_sale(self, id_sale:int):
        query_one = await SalesRepository().get_one(id_sale)
        response: Response = {}
        if not query_one:
            response['status'] = False
            response['status_code'] = 402
            response['message'] = 'Any sale active'
            response['data'] = {}
            return response
        
        response['status'] = True
        response['status_code'] = 200
        response['message'] = 'Sale found'
        response['data'] = query_one
        return response