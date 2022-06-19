'''user.py'''
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Response, status

from app import oauth2
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.User
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    '''Create User'''

    found_user = db.query(models.User).filter(models.User.email == user.email).first()
    if found_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with the email already exists"
        )
    # hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.User]
)
def get_users(
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    '''Get All Users'''
    users = db.query(models.User).all()
    return users


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.User
)
def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    '''Get User with specified ID'''
    user = db.query(models.User).get(id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found"
        )

    return user


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    '''Delete User with specified ID'''
    user = db.query(models.User).filter(models.User.id == id)
    if user.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found"
        )
    if user.first().id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorised to perform requested action"
        )
    user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.User
)
def update_user(
    id: int,
    updated_user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    '''Update User with specified ID'''
    user_query = db.query(models.User).filter(models.User.id == id)
    found_user = user_query.first()
    if found_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found"
        )
    if found_user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorised to perform requested action"
        )
    user_query.update(updated_user.dict(), synchronize_session=False)
    db.commit()
    return user_query.first()
