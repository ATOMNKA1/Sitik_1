from sqlalchemy.orm import Session
from app.models.game import Game as GameModel  # Используем SQLAlchemy-модель
from app.schemas.game import GameCreate

class GameRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_game(self, game: GameCreate):
        db_game = GameModel(**game.dict())
        self.db.add(db_game)
        self.db.commit()
        self.db.refresh(db_game)
        return db_game

    def get_games(self, skip: int = 0, limit: int = 10, name: str = None, sort_by: str = None):
        query = self.db.query(GameModel)
        if name:
            query = query.filter(GameModel.name.ilike(f"%{name}%"))
        if sort_by in ["name", "id"]:
            query = query.order_by(getattr(GameModel, sort_by))
        return query.offset(skip).limit(limit).all()

    def get_game_by_id(self, game_id: int):
        return self.db.query(GameModel).filter(GameModel.id == game_id).first()

    def update_game(self, game_id: int, game_update: GameCreate):
        db_game = self.db.query(GameModel).filter(GameModel.id == game_id).first()
        if db_game:
            for key, value in game_update.dict().items():
                setattr(db_game, key, value)
            self.db.commit()
            self.db.refresh(db_game)
        return db_game

    def delete_game(self, game_id: int):
        db_game = self.db.query(GameModel).filter(GameModel.id == game_id).first()
        if db_game:
            self.db.delete(db_game)
            self.db.commit()
        return db_game