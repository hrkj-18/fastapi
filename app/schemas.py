'''Schemas.py'''
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    '''Pydantic Post Model: Used for validation of request coming from Postman'''
    title:str
    content:str
    published:bool=True

class PostCreate(PostBase):
    '''Pydantic PostCreate Model: Used for validation of request coming from Postman'''
    pass

class Post(BaseModel):
    '''Pydantic Post Model: Used for sending Post data to Postman'''
    title:str
    content:str
    published:bool

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    '''Pydantic User Model: Used for validation of request coming from Postman'''
    email:EmailStr
    password:str

class User(BaseModel):
    '''Pydantic Post Model: Used for sending Post data to Postman'''
    email:EmailStr

    class Config:
        orm_mode = True