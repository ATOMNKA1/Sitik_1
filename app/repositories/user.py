from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_login(self, login: str) -> User | None:
        return self.db.query(User).filter(User.login == login).first()

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_users(self, skip: int, limit: int) -> list[User]:
        return self.db.query(User).offset(skip).limit(limit).all()

    def create_user(self, user: UserCreate) -> User:
        hashed_password = pwd_context.hash(user.password)
        db_user = User(login=user.login, email=user.email, password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, user_id: int, user_update: dict) -> User | None:
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if db_user:
            for key, value in user_update.items():
                if key == "password":
                    value = pwd_context.hash(value)
                setattr(db_user, key, value)
            self.db.commit()
            self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int) -> User | None:
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
        return db_user

    def check_admin_credentials(self, login: str, password: str) -> User | None:
        if login == "admin" and password == "1234":
            user = self.get_user_by_login(login)
            if user:
                return user
            hashed_password = pwd_context.hash(password)
            db_user = User(login=login, email="admin@example.com", password=hashed_password, is_admin=True)
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        return None