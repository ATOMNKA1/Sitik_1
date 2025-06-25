from pydantic import BaseModel

class GameBase(BaseModel):
    name: str
    description: str
    system_requirements: str
    main_image: str

class GameCreate(GameBase):
    pass

class GameUpdate(GameBase):
    name: str | None = None
    description: str | None = None
    system_requirements: str | None = None
    main_image: str | None = None

class GameOut(GameBase):
    id: int

    class Config:
        from_attributes = True