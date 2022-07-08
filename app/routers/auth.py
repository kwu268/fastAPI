from fastapi import APIRouter, Depends, Response, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..databse import get_db
from ..schemas import UserLogin, Token
from .. import models, oauth2
from ..utils import verify


router = APIRouter(tags = ['Authentication'])

@router.post('/login', response_model = Token)
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"credentials invalid")
    
    if not verify(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"credentials invalid")
    
    accessToken = oauth2.createAccessToken(data = {"user_id": user.id})

    return {"access_token": accessToken, "token_type": "bearer"}
    

    
