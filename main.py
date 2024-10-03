from fastapi import FastAPI 
import uvicorn
from app.db.database import Base, engine
import app.models as models
from app.routers import users, roles, permissions, sales, manage_permissions

def create_tables():
    models.Base.metadata.create_all(bind=engine)

create_tables()
app = FastAPI()
app.include_router(roles.router_roles)
app.include_router(users.router_users)
app.include_router(permissions.router_permissions)
app.include_router(sales.router_sales)
app.include_router(manage_permissions.router_manages)

if __name__=="__main__":
    uvicorn.run("main:app",port=8000, reload=True)