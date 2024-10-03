from app.schemas.response import Response
from app.repository import RolesRepository

class RoleService:
    def __init__(self) -> None:
        pass

    async def register(self, input):
        query_exist = await RolesRepository().get_one_role(role=input)

        response: Response = {}
        if query_exist:
            response['status'] = False
            response['status_code'] = 402
            response['message'] = 'Role exist'
            response['data'] = {}
            return response

        data = await RolesRepository().register_role(role=input)

        if not data:
            response['status'] = False
            response['status_code'] = 402
            response['message'] = 'Role not register'
            response['data'] = {}
            return response
    
        response['status'] = True
        response['status_code'] = 200
        response['message'] = 'Role register'
        response['data'] = data
        
        return response
    
    async def get_all_roles(self):
        query_all = await RolesRepository().get_all()

        response: Response = {}
        if not query_all:
            response['status'] = False
            response['status_code'] = 402
            response['message'] = 'Any role active'
            response['data'] = {}
            return response
        
        response['status'] = True
        response['status_code'] = 200
        response['message'] = 'List roles'
        response['data'] = query_all
        return response
    
    async def update(self, input):

        update =  await RolesRepository().update(role=input)
        response: Response = {}
        if not update:
            response['status'] = False
            response['status_code'] = 402
            response['message'] = 'Role not exist'
            response['data'] = {}
            return response
        
        response['status'] = True
        response['status_code'] = 200
        response['message'] = 'Update role'
        response['data'] = update
        return response
    
    async def desactivate(self, input):

        desactivate =  await RolesRepository().desactivate(role=input)
        response: Response = {}
        if not desactivate:
            response['status'] = False
            response['status_code'] = 402
            response['message'] = 'Role not exist'
            response['data'] = {}
            return response
        
        response['status'] = True
        response['status_code'] = 200
        response['message'] = 'Role status changed'
        response['data'] = desactivate
        return response