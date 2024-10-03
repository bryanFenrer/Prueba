from app.db.database import session
from app.models.userPermissions import UserPermission
from app.repository.permissions import PermissionRepository
from app.repository.users import UserRepository

class ManagePermissionsRepository:
    def __init__(self) -> None:
        pass

    async def assign(self, id):
        try:
            data = {}
            user_exist = await UserRepository().verify_existence(id)
            if not user_exist:
                return False
            id_permission = await PermissionRepository().get_id_permission()
            if not id_permission:
                return False
            relation = session.query(UserPermission).filter(UserPermission.user_id == id, UserPermission.permission_id == id_permission, UserPermission.status == 'active')
            if relation:
                return 'active'
            relation = session.query(UserPermission).filter(UserPermission.user_id == id, UserPermission.permission_id == id_permission, UserPermission.status == 'inactive')
            if not relation:
                data['user_id'] = id
                data['permission_id'] = id_permission
                data = UserPermission(**data)
                session.add(data)
                session.commit()
                return data
            if relation:
                data['status'] = 'active'
                data = relation.update(data)           
                session.commit()
                return data

        except Exception as e:
            print(str(e))
            return False
    
    async def revoke(self, id):
        try:
            data = {}
            user_exist = session.query(UserPermission).filter(UserPermission.user_id == id)

            if not user_exist.first(): 
                return False
            data['status'] = 'inactive'
            user_exist = user_exist.update(data)           
            session.commit()

            return user_exist
        except Exception as e:
            print(str(e))
            return False