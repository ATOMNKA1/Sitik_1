from pydantic import BaseModel, EmailStr, validator
from typing import Optional

class UserCreate(BaseModel):
    login: str
    email: EmailStr  # Валидация формата email
    password: str

    @validator("password")
    def password_length(cls, v):
        if len(v) < 8:
            raise ValueError("Пароль должен быть не короче 8 символов")
        return v

class UserUpdate(BaseModel):
    login: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    @validator("password")
    def password_length(cls, v):
        if v and len(v) < 8:
            raise ValueError("Пароль должен быть не короче 8 символов")
        return v

class UserOut(BaseModel):
    id: int
    login: str
    email: str
    is_admin: bool  # Добавляем поле для отображения админ-статуса

    class Config:
        from_attributes = True