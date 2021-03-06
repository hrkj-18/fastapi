'''vote.py'''
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Response, status, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post(
    '',
    status_code=status.HTTP_201_CREATED
)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    post = db.query(models.Post).get(vote.post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post Not Found"
        )
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()
    if vote.dir:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f'user {current_user.id} has aready voted on post {vote.post_id}'
            )
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {'message': 'sucussefully voted'}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Vote does not exist'
            )
        vote_query.delete(synchronize_session=False)
        db.commit()

        return{'message': 'Vote deleted'}
