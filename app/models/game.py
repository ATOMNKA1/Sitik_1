from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    system_requirements = Column(Text)
    main_image = Column(String)

    favorites = relationship("Favorite", back_populates="game")
    comments = relationship("Comment", back_populates="game")