from pydantic import BaseModel

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class CommentOut(CommentBase):
    id: int
    user_id: int
    game_id: int
    username: str  # Новое поле для имени пользователя

    class Config:
        from_attributes = True