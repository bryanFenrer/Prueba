from app.db.database import session
from app.models.users import User
from app.repository.roles import RolesRepository
import hashlib

class UserRepository:
    def __init__(self) -> None:
        pass
        
    async def register_user(self, user):
        try:
            user = user.dict()
            password = user['password']
            user['password'] = hashlib.sha256(password.encode()).hexdigest()
            id_role = await RolesRepository().get_id_role()
            user['role_id'] = id_role
            newUser = User(**user)
            session.add(newUser)
            session.commit()
            session.refresh(newUser)
            
            return newUser
        except Exception as e:
            print(str(e))
            return False

    async def get_one_user(self, user):
        try:
            user = user.dict()
            return session.query(User).filter_by(**user).first()
        except Exception as e:
            print(str(e))
            return False
        
    async def get_all(self):
        try:
            return session.query(User).filter_by(status='active').all()
        except Exception as e:
            print(str(e))
            return False
        
    async def update(self, user):
        user = user.dict()
        try:
            user_update = session.query(User).filter(User.id == user['id'], User.status == 'active')

            if not user_update.first(): 
                return False
            
            password = user['password']
            user['password'] = hashlib.sha256(password.encode()).hexdigest()
            id_role = await RolesRepository().get_id_role()
            user['role_id'] = id_role
            user_update = user_update.update(user)           
            session.commit()

            return user_update
        except Exception as e:
            print(str(e))
            return False
        
    async def desactivate(self, user):
        user = user.dict()
        try:
            user_desactivate = session.query(User).filter(User.id == user['id'])

            if not user_desactivate.first(): 
                return False
 
            user_desactivate = user_desactivate.update(user)           
            session.commit()

            return user_desactivate
        except Exception as e:
            print(str(e))
            return False
        
    async def verify_existence(self, id):
        try:
            verify = session.query(User).filter(User.id == id)
            if not verify.first():
                return False
            return verify
        except Exception as e:
            print(str(e))
            return False
        