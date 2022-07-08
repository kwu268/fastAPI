from .. import models
from ..schemas import UserOut, UserCreate
from ..utils import hash
from fastapi import  Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..databse import get_db
###################################################################################
###############################     USERS     #####################################
###################################################################################

router = APIRouter(
    prefix = "/users",
    tags = ['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model = UserOut)
def create_users(user: UserCreate, db: Session = Depends(get_db)):

    #hash the password
    hashedPass = hash(user.password)
    user.password = hashedPass
    newUser = models.User(**user.dict())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser


@router.get("/{id}", response_model = UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} was not  found")
    return user