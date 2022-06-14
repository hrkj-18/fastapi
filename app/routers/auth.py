'''auth.py'''
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])


@router.post(
    '/login',
    status_code=status.HTTP_200_OK,
    response_model=schemas.Token
)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    '''Login'''
    # OAuth2PasswordRequestForm returns username and password
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username
    ).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
