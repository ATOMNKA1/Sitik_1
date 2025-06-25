from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserOut, UserUpdate
from app.repositories.user import UserRepository
from app.utils.auth import get_current_user
from app.models.user import User

router = APIRouter(tags=["Users"])

@router.get("/users/by-login/{login}", response_model=UserOut)
def get_user_by_login(login: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_repo = UserRepository(db)
    user = user_repo.get_user_by_login(login)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_repo = UserRepository(db)
    user = user_repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@router.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_repo = UserRepository(db)
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    user = user_repo.update_user(user_id, user_update.dict(exclude_unset=True))
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_repo = UserRepository(db)
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    user = user_repo.delete_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return None

@router.get("/users", response_model=list[UserOut])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Требуются права администратора")
    user_repo = UserRepository(db)
    return user_repo.get_users(skip, limit)