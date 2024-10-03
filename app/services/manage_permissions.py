from app.schemas.response import Response
from app.repository import ManagePermissionsRepository

class ManagePermissionsService:
    def __init__(self) -> None:
        pass

    async def assign(self, id):
        assign =  await ManagePermissionsRepository().assign(id)
        response: Response = {}
        if not assign:
            response['status'] = False
            response['status_code'] = 402
            response['message'] = 'User not exist'
            response['data'] = {}
            return response
        if assign == 'active':
            response['status'] = False
            response['status_code'] = 402
            response['message'] = 'Permission already assigned'
            response['data'] = {}
            return response
        response['status'] = True
        response['status_code'] = 200
        response['message'] = 'User permission assigned'
        response['data'] = assign
        return response
    
    async def revoke(self, id):
        revoke = await ManagePermissionsRepository().revoke(id)
        response: Response = {}
        if not revoke:
            response['status'] = False
            response['status_code'] = 402
            response['message'] = 'User not exist'
            response['data'] = {}
            return response
        
        response['status'] = True
        response['status_code'] = 200
        response['message'] = 'User permission revoked'
        response['data'] = revoke
        return response