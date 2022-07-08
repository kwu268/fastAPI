from .. import models, oauth2
from ..schemas import Vote
from ..utils import hash
from fastapi import  Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..databse import get_db


router = APIRouter(
    prefix = "/vote",
    tags = ['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    postQuery = db.query(models.Post).filter(models.Post.id == vote.post_id)
    postFound = postQuery.first()

    if not postFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post does not exist")    
    voteQuery = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    foundVote = voteQuery.first()

    if (vote.dir == 1):
        if foundVote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user: {current_user.id} has already voted this post")
        
        newVote = models.Vote(post_id = vote.post_id, user_id = current_user.id) 
        db.add(newVote)
        db.commit()
        return {"message": "successfully liked"}

    else:
        if not foundVote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

        voteQuery.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully unliked"} 

