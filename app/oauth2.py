from app import models
from .schemas import Token, TokenData
from .databse import get_db
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer 
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login  ')

#SECRET_KEY, 

#algorithm,

#exporiation time  

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRED_MINUTES


def createAccessToken(data: dict):
    toEncode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    toEncode.update({"exp": expire})

    encodedJWT = jwt.encode(toEncode, SECRET_KEY, algorithm = ALGORITHM)

    return encodedJWT

def verifyAccessToklen(token: str, credentials_execption):
    
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_execption
        token_data = TokenData(id=id)

    except JWTError:
        raise credentials_execption

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_execption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Couldnt validate credentials", 
        headers={"WWW-Authenticate": "Bearer"})

    token = verifyAccessToklen(token, credentials_execption)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    print("ID NUMBER: ")

    return user
        
