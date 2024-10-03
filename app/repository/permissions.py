from app.db.database import session
from app.models.permissions import Permission

class PermissionRepository:
    def __init__(self) -> None:
        pass

    async def register_permission(self, permission):
        try:
            permission = permission.dict()
            newPermission = Permission(**permission)
            session.add(newPermission)
            session.commit()
            session.refresh(newPermission)
            
            return newPermission
        except Exception as e:
            print(str(e))
            return False
        
    async def get_one_permission(self, permission):
        try:
            permission = permission.dict()
            return session.query(Permission).filter_by(**permission).first()
        except Exception as e:
            print(str(e))
            return False
        
    async def get_all(self):
        try:
            return session.query(Permission).filter_by(status='active').all()
        except Exception as e:
            print(str(e))
            return False
        
    async def update(self, permission):
        permission = permission.dict()
        try:
            permission_update = session.query(Permission).filter(Permission.id == permission['id'], Permission.status == 'active')

            if not permission_update.first(): 
                return False
 
            permission_update = permission_update.update(permission)           
            session.commit()

            return permission_update
        except Exception as e:
            print(str(e))
            return False
        
    async def desactivate(self, permission):
        permission = permission.dict()
        try:
            permission_desactivate = session.query(Permission).filter(Permission.id == permission['id'])

            if not permission_desactivate.first(): 
                return False
 
            permission_desactivate = permission_desactivate.update(permission)           
            session.commit()

            return permission_desactivate
        except Exception as e:
            print(str(e))
            return False
        
    async def get_id_permission(self):
        try:
            permission = session.query(Permission).filter(Permission.name == 'Especial').first()
            permission = {key: value for key, value in permission.__dict__.items() if not key.startswith('_')}
            return permission['id']
        except Exception as e:
            print(str(e))
            return False