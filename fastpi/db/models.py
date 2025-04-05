from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
# from sqlalchemy.orm import relationship
from .databaseConnect import Base


class Fare(Base):
    __tablename__ = "fare"

    id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    location = Column(String)
    price = Column(Integer)
    difficulty = Column(String)
    # player = relationship("FarePlayer", back_populates="fare_id")


class FarePayer(Base):
    __tablename__ = "fareplayer"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    # fare_id = relationship("Fare", back_populates="player")
