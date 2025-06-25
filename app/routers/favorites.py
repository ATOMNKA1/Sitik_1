from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.favorite import FavoriteCreate, FavoriteOut
from app.models.favorite import Favorite
from app.models.user import User
from app.utils.auth import get_current_user

router = APIRouter(tags=["Favorites"])

@router.get("/favorites", response_model=list[FavoriteOut])
def get_favorites(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Favorite).filter(Favorite.user_id == current_user.id).offset(skip).limit(limit).all()

@router.get("/favorites/is_favorited", response_model=bool)
def is_favorited(
    game_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    favorite = db.query(Favorite).filter(Favorite.user_id == current_user.id, Favorite.game_id == game_id).first()
    return favorite is not None

@router.post("/favorites", response_model=FavoriteOut)
def add_favorite(favorite: FavoriteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_favorite = Favorite(user_id=current_user.id, game_id=favorite.game_id)
    db.add(db_favorite)
    try:
        db.commit()
        db.refresh(db_favorite)
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Не удалось добавить в избранное")
    return db_favorite

@router.delete("/favorites/{game_id}", status_code=204)
def remove_favorite(game_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    favorite = db.query(Favorite).filter(Favorite.user_id == current_user.id, Favorite.game_id == game_id).first()
    if not favorite:
        raise HTTPException(status_code=404, detail="Игра не найдена в избранном")
    db.delete(favorite)
    db.commit()
    return None