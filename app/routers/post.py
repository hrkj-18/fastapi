'''post.py'''
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Response, status, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.Post])
def get_posts(
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    '''Get All Posts'''
    posts = db.query(models.Post).all()
    return posts


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Post
)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    '''Get Post with specified ID'''
    post = db.query(models.Post).get(id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post Not Found"
        )
    return post


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Post
)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    '''Create Post'''
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    '''Delete Post with specified ID'''
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post Not Found"
        )
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.Post
)
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    '''Update Post with specified ID'''
    post_query = db.query(models.Post).filter(models.Post.id == id)
    found_post = post_query.first()
    if found_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post Not Found"
            )
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
