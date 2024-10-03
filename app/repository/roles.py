from app.db.database import session
from app.models.roles import Role

class RolesRepository:
    def __init__(self) -> None:
        pass

    async def register_role(self, role):
        try:
            role = role.dict()
            newRole = Role(**role)
            session.add(newRole)
            session.commit()
            session.refresh(newRole)
            
            return newRole
        except Exception as e:
            print(str(e))
            return False
        
    async def get_one_role(self, role):
        try:
            role = role.dict()
            return session.query(Role).filter_by(**role).first()
        except Exception as e:
            print(str(e))
            return False
        
    async def get_all(self):
        try:
            return session.query(Role).filter_by(status='active').all()
        except Exception as e:
            print(str(e))
            return False
        
    async def update(self, role):
        role = role.dict()
        try:
            role_update = session.query(Role).filter(Role.id == role['id'], Role.status == 'active')

            if not role_update.first(): 
                return False
 
            role_update = role_update.update(role)           
            session.commit()

            return role_update
        except Exception as e:
            print(str(e))
            return False
        
    async def desactivate(self, role):
        role = role.dict()
        try:
            role_desactivate = session.query(Role).filter(Role.id == role['id'])

            if not role_desactivate.first(): 
                return False
 
            role_desactivate = role_desactivate.update(role)           
            session.commit()

            return role_desactivate
        except Exception as e:
            print(str(e))
            return False
        
    async def get_id_role(self):
        try:
            role = session.query(Role).filter(Role.name == 'ventas').first()
            role = {key: value for key, value in role.__dict__.items() if not key.startswith('_')}
            return role['id']
        except Exception as e:
            print(str(e))
            return False