from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.comment import CommentCreate, CommentOut
from app.models.comment import Comment
from app.models.user import User
from app.utils.auth import get_current_user

router = APIRouter(tags=["Comments"])

@router.get("/games/{game_id}/comments", response_model=list[CommentOut])
def get_comments(
    game_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    comments = (db.query(Comment, User.login.label("username"))
                .join(User, User.id == Comment.user_id)
                .filter(Comment.game_id == game_id)
                .offset(skip)
                .limit(limit)
                .all())
    return [{"id": comment.id, "content": comment.content, "user_id": comment.user_id,
             "game_id": comment.game_id, "username": username} for comment, username in comments]

@router.post("/games/{game_id}/comments", response_model=CommentOut)
def create_comment(
    game_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.models.game import Game
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Игра не найдена")
    
    db_comment = Comment(**comment.dict(), game_id=game_id, user_id=current_user.id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    user = db.query(User).filter(User.id == db_comment.user_id).first()
    return {**db_comment.__dict__, "username": user.login}

@router.put("/comments/{id}", response_model=CommentOut)
def update_comment(
    id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_comment = db.query(Comment).filter(Comment.id == id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    if db_comment.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    for key, value in comment.dict().items():
        setattr(db_comment, key, value)
    db.commit()
    db.refresh(db_comment)
    user = db.query(User).filter(User.id == db_comment.user_id).first()
    return {**db_comment.__dict__, "username": user.login}

@router.delete("/comments/{id}", status_code=204)
def delete_comment(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_comment = db.query(Comment).filter(Comment.id == id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    if db_comment.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    db.delete(db_comment)
    db.commit()
    return None