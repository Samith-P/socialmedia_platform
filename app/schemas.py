from typing import Optional
from pydantic import BaseModel

class Post(BaseModel):
    title:str
    content:str
    published:bool=True 
class Postget(Post):
    id:int
    user_id:int
    class Config:
        from_attributes = True

class PostCreate(Post):
    pass

#-------------------------------------------------------------User Schema------------------------------------------------------------------------------#

class User(BaseModel):
    email:str
    password:str
class UserCreate(BaseModel):
    id:int
    email:str
    class Config:
        from_attributes = True

class TokenData(BaseModel):
    id: Optional[int]=None 