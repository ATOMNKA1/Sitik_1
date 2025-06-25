from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.game import GameCreate, GameOut, GameUpdate
from app.models.game import Game
from app.utils.auth import get_current_user
from app.models.user import User

router = APIRouter(tags=["Games"])

@router.get("/games", response_model=list[GameOut])
def get_games(
    skip: int = 0,
    limit: int = 10,
    name: str = "",
    db: Session = Depends(get_db)
):
    query = db.query(Game)
    if name:
        query = query.filter(Game.name.ilike(f"%{name}%"))
    return query.offset(skip).limit(limit).all()

@router.get("/games/{id}", response_model=GameOut)
def get_game(id: int, db: Session = Depends(get_db)):
    game = db.query(Game).filter(Game.id == id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Игра не найдена")
    return game

@router.post("/games", response_model=GameOut)
def create_game(
    game: GameCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    db_game = Game(**game.dict())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

@router.put("/games/{id}", response_model=GameOut)
def update_game(
    id: int,
    game: GameUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    db_game = db.query(Game).filter(Game.id == id).first()
    if not db_game:
        raise HTTPException(status_code=404, detail="Игра не найдена")
    for key, value in game.dict(exclude_unset=True).items():
        setattr(db_game, key, value)
    db.commit()
    db.refresh(db_game)
    return db_game

@router.delete("/games/{id}", status_code=204)
def delete_game(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    game = db.query(Game).filter(Game.id == id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Игра не найдена")
    db.delete(game)
    db.commit()
    return None