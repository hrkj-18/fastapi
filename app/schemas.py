'''Schemas.py'''
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    '''Pydantic User Model:
    Used for validation of request coming from Postman'''
    email: EmailStr
    password: str


class User(BaseModel):
    '''Pydantic Post Model:
    Used for sending Post data to Postman'''
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    '''Pydantic Userogin Model:
    Used for validation of request coming from Postman'''
    email: EmailStr
    password: str


class PostBase(BaseModel):
    '''Pydantic Post Model:
    Used for validation of request coming from Postman'''
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    '''Pydantic PostCreate Model:
    Used for validation of request coming from Postman'''
    pass


class Post(PostBase):
    '''Pydantic Post Model: Used for sending Post data to Postman'''
    id: int
    owner_id: int
    owner: User

    class Config:
        orm_mode = True


class Token(BaseModel):
    '''Pydantic Token Model:
    Used for sending Post data to Postman'''
    access_token: str
    token_type: str


class TokenData(BaseModel):
    '''Pydantic Token Model:
    Used for receiving data from internal function'''
    id: Optional[str] = None
