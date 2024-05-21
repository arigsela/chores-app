from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Kid(Base):
    __tablename__ = "kids"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    kid_rewards = relationship("KidReward", back_populates="kid")
    kid_chores = relationship("KidChore", back_populates="kid")


class Chore(Base):
    __tablename__ = "chores"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    points = Column(Integer)

class Reward(Base):
    __tablename__ = "rewards"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    points = Column(Integer)
    kid_rewards = relationship("KidReward", back_populates="reward")

    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))
    
class KidReward(Base):
    __tablename__ = "kid_rewards"
    id = Column(Integer, primary_key=True, index=True)
    kid_id = Column(Integer, ForeignKey("kids.id"))
    reward_id = Column(Integer, ForeignKey("rewards.id"))
    awarded_at = Column(DateTime, default=datetime.utcnow)

    kid = relationship("Kid", back_populates="kid_rewards")
    reward = relationship("Reward", back_populates="kid_rewards")

class KidChore(Base):
    __tablename__ = "kid_chores"
    id = Column(Integer, primary_key=True, index=True)
    kid_id = Column(Integer, ForeignKey("kids.id"))
    chore_id = Column(Integer, ForeignKey("chores.id"))
    completed_at = Column(DateTime, default=datetime.utcnow)

    kid = relationship("Kid", back_populates="kid_chores")
    chore = relationship("Chore")