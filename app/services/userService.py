from app.schemas.response import Response
from app.repository import UserRepository

class  UserService:
    def __init__(self) -> None:
        pass
        
    async def register(self, input):
        query_exist = await UserRepository().get_one_user(user=input)

        response: Response = {}
        if query_exist:
            response['status'] = False 
            response['status_code'] = 402
            response['message'] = 'User exist'
            response['data'] = {}
            return response

        data = await UserRepository().register_user(user=input)

        if not data:
            response['status'] = False
            response['status_code'] = 402
            response['message'] = 'User not register'
            response['data'] = {}
            return response
    
        response['status'] = True
        response['status_code'] = 200
        response['message'] = 'User register'
        response['data'] = data
        
        return response
    
    async def get_all_users(self):
        query_all = await UserRepository().get_all()

        response: Response = {}
        if not query_all:
            response['status'] = False
            response['status_code'] = 402
            response['message'] = 'Any user active'
            response['data'] = {}
            return response
        
        response['status'] = True
        response['status_code'] = 200
        response['message'] = 'List users'
        response['data'] = query_all
        return response
    
    async def update(self, input):

        update =  await UserRepository().update(user=input)
        response: Response = {}
        if not update:
            response['status'] = False
            response['status_code'] = 402
            response['message'] = 'User not exist'
            response['data'] = {}
            return response
        
        response['status'] = True
        response['status_code'] = 200
        response['message'] = 'Update user'
        response['data'] = update
        return response
    
    async def desactivate(self, input):

        desactivate =  await UserRepository().desactivate(user=input)
        response: Response = {}
        if not desactivate:
            response['status'] = False
            response['status_code'] = 402
            response['message'] = 'User not exist'
            response['data'] = {}
            return response
        
        response['status'] = True
        response['status_code'] = 200
        response['message'] = 'User status changed'
        response['data'] = desactivate
        return response