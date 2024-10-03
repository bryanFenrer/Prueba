from pydantic import BaseModel 

class Response(BaseModel):
    status:bool = False
    status_code:int 
    message:str = ""
    data:dict = {}