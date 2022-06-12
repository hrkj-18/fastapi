'''Schemas.py'''
from pydantic import BaseModel


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
