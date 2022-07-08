from .. import models, oauth2
from typing import List, Optional
from ..schemas import Post, PostCreate, PostOut
from ..utils import hash
from fastapi import  Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..databse import get_db
###################################################################################
###############################     POSTS     #####################################
###################################################################################

router = APIRouter(
    prefix ="/posts",
    tags = ['Posts']
)

@router.get("/")
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results

@router.get("/{id}", response_model=Post) 
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not  found")
    return post

###################################################################################

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post: PostCreate, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    #     (post.title, post.content, post.published))
    # newPost = cursor.fetchone()
    # conn.commit()

    #unpacks the post request as a dict so I dont have to type out each field ie. title = post.title, etc  
    print(user.id)
    newPost = models.Post(user_id=user.id, **post.dict())
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost

###################################################################################

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)): 
    # cursor.execute("""DELETE FROM posts WHERE id =  %s RETURNING *""", (str(id)))
    # deletedPost = cursor.fetchone()
    # conn.commit()

    deletePostQuery = db.query(models.Post).filter(models.Post.id == id)
    deletedPost = deletePostQuery.first()
    if deletedPost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post  with {id} does not exist")


    if deletedPost.user_id !=  user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized")

    deletePostQuery.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

###################################################################################

@router.put("/{id}", response_model=Post)
def putPost(id: int, post: PostCreate, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
    #     (post.title, post.content, post.published, str(id)))
    # updatedPost = cursor.fetchone()
    # conn.commit()
    
    updatedPostQuery = db.query(models.Post).filter(models.Post.id == id)
    updatedPost = updatedPostQuery.first()
    
    if updatedPost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post  with {id} does not exist")

    if updatedPost.user_id !=  user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized")

    updatedPostQuery.update(post.dict(), synchronize_session=False)
    db.commit()
    return updatedPostQuery.first()