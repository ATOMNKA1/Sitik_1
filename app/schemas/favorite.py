from pydantic import BaseModel
from app.schemas.game import GameOut

class FavoriteBase(BaseModel):
    game_id: int

class FavoriteCreate(FavoriteBase):
    pass

class FavoriteOut(FavoriteBase):
    id: int
    user_id: int
    game: GameOut

    class Config:
        from_attributes = True