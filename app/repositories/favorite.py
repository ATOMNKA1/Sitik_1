from sqlalchemy.orm import Session
from app.models.favorite import Favorite
from app.schemas.favorite import FavoriteCreate

class FavoriteRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_favorite(self, favorite: FavoriteCreate, user_id: int):
        db_favorite = Favorite(user_id=user_id, game_id=favorite.game_id)
        self.db.add(db_favorite)
        self.db.commit()
        self.db.refresh(db_favorite)
        return db_favorite

    def get_favorites(self, user_id: int):
        return self.db.query(Favorite).filter(Favorite.user_id == user_id).all()

    def delete_favorite(self, user_id: int, game_id: int):
        favorite = self.db.query(Favorite).filter(Favorite.user_id == user_id, Favorite.game_id == game_id).first()
        if favorite:
            self.db.delete(favorite)
            self.db.commit()
        return favorite

    def is_favorited(self, user_id: int, game_id: int):
        return self.db.query(Favorite).filter(Favorite.user_id == user_id, Favorite.game_id == game_id).first() is not None