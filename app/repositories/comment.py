from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.schemas.comment import CommentCreate

class CommentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_comment(self, comment: CommentCreate, user_id: int, game_id: int):
        db_comment = Comment(text=comment.text, user_id=user_id, game_id=game_id)
        self.db.add(db_comment)
        self.db.commit()
        self.db.refresh(db_comment)
        return db_comment

    def get_comments_by_game_id(self, game_id: int):
        return self.db.query(Comment).filter(Comment.game_id == game_id).all()

    def update_comment(self, comment_id: int, text: str):
        db_comment = self.db.query(Comment).filter(Comment.id == comment_id).first()
        if db_comment:
            db_comment.text = text
            self.db.commit()
            self.db.refresh(db_comment)
        return db_comment

    def delete_comment(self, comment_id: int):
        db_comment = self.db.query(Comment).filter(Comment.id == comment_id).first()
        if db_comment:
            self.db.delete(db_comment)
            self.db.commit()
        return db_comment