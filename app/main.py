'''Main.py'''
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, Response, status
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/posts/", response_model=List[schemas.Post])
def get_posts(db:Session = Depends(get_db)):
    '''Get All Posts'''
    posts = db.query(models.Post).all()
    return posts


@app.get("/posts/{id}",status_code=status.HTTP_200_OK, response_model=schemas.Post)
def get_post(id:int, db:Session = Depends(get_db)):
    '''Get Post with specified ID'''
    post = db.query(models.Post).get(id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")
    return post

@app.post("/posts/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post:schemas.PostCreate, db:Session = Depends(get_db)):
    '''Create Post'''
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session = Depends(get_db)):
    '''Delete Post with specified ID'''
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@app.put("/posts/{id}",status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(id:int, updated_post:schemas.PostCreate, db:Session = Depends(get_db)):
    '''Update Post with specified ID'''
    post_query = db.query(models.Post).filter(models.Post.id == id)
    found_post = post_query.first()
    if found_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()
