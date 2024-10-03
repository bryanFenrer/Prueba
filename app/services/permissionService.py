from app.schemas.response import Response
from app.repository import PermissionRepository

class PermissionService:
    def __init__(self) -> None:
        pass

    async def register(self, input):
        query_exist = await PermissionRepository().get_one_permission(permission=input)

        response: Response = {}
        if query_exist:
            response['status'] = False
            response['status_code'] = 402
            response['message'] = 'Permission exist'
            response['data'] = {}
            return response

        data = await PermissionRepository().register_permission(permission=input)

        if not data:
            response['status'] = False
            response['status_code'] = 402
            response['message'] = 'Permission not register'
            response['data'] = {}
            return response
    
        response['status'] = True
        response['status_code'] = 200
        response['message'] = 'Permission register'
        response['data'] = data
        
        return response
    
    async def get_all_permissions(self):
        query_all = await PermissionRepository().get_all()

        response: Response = {}
        if not query_all:
            response['status'] = False
            response['status_code'] = 402
            response['message'] = 'Any permission active'
            response['data'] = {}
            return response
        
        response['status'] = True
        response['status_code'] = 200
        response['message'] = 'List permissions'
        response['data'] = query_all
        return response
    
    async def update(self, input):

        update =  await PermissionRepository().update(permission=input)
        response: Response = {}
        if not update:
            response['status'] = False
            response['status_code'] = 402
            response['message'] = 'Permission not exist'
            response['data'] = {}
            return response
        
        response['status'] = True
        response['status_code'] = 200
        response['message'] = 'Update permission'
        response['data'] = update
        return response
    
    async def desactivate(self, input):

        desactivate =  await PermissionRepository().desactivate(permission=input)
        response: Response = {}
        if not desactivate:
            response['status'] = False
            response['status_code'] = 402
            response['message'] = 'Permission not exist'
            response['data'] = {}
            return response
        
        response['status'] = True
        response['status_code'] = 200
        response['message'] = 'Permission status changed'
        response['data'] = desactivate
        return response