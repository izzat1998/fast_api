from _xxsubinterpreters import get_current
from typing import List, Optional

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy import func

from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from .. import schemas, models, oauth2
from ..database import get_db

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
                    limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                                                                                         models.Vote.post_id == models.Post.id,
                                                                                         isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                       current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{pk}",response_model=schemas.PostOut)
def get_post(pk: int, db: Session = Depends(get_db), current_user: int =
Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                                                                                         models.Vote.post_id == models.Post.id,
                                                                                         isouter=True).group_by(
        models.Post.id).filter(models.Post.id == pk).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {pk} not found"
        )
    return post


@router.delete("/{pk}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(pk: int, db: Session = Depends(get_db), current_user: int =
Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == pk)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {pk} not found"
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Post owner {post.owner_id} does not belong to this user",
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{pk}")
def update_post(pk: int, updated_post: schemas.PostBase, db: Session = Depends(get_db), current_user: int =
Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == pk)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {pk} not found"
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Post owner {post.owner_id} does not belong to this user",
        )

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
