from app.db.database import session
from app.models.sales import Sale

class SalesRepository:
    def __init__(self) -> None:
        pass
      
    async def get_all(self):
        try:
            return session.query(Sale).all()
        except Exception as e:
            print(str(e))
            return False
        
    async def get_one(self, id_sale):
        try:
            sale = session.query(Sale).filter(Sale.id == id_sale).first()
            sale = {key: value for key, value in sale.__dict__.items() if not key.startswith('_')}
            return sale
        except Exception as e:
            print(str(e))
            return False
  