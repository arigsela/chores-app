import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import models

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "3306")
DB_USER = os.environ.get("DB_USER", "your_username")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "your_password")
DB_NAME = os.environ.get("DB_NAME", "your_database")

SQLALCHEMY_DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

Base = declarative_base()

class Kid(Base):
    __tablename__ = "kids"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    age = Column(Integer)

    chores = relationship("Chore", back_populates="kid")
    rewards = relationship("Reward", back_populates="kid")

class Chore(Base):
    __tablename__ = "chores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255))
    points = Column(Integer)
    kid_id = Column(Integer, ForeignKey("kids.id"))

    kid = relationship("Kid", back_populates="chores")

class Reward(Base):
    __tablename__ = "rewards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255))
    points = Column(Integer)
    kid_id = Column(Integer, ForeignKey("kids.id"))

    kid = relationship("Kid", back_populates="rewards")

async def get_async_session():
    async with async_session() as session:
        yield session

async def create_kid(kid: models.Kid):
    async with async_session() as db:
        db_kid = Kid(name=kid.name, age=kid.age)
        db.add(db_kid)
        await db.commit()
        await db.refresh(db_kid)
        return db_kid

async def get_kids(skip: int = 0, limit: int = 100):
    async with async_session() as db:
        result = await db.execute(db.query(Kid).offset(skip).limit(limit))
        return result.scalars().all()

async def get_kid(kid_id: int):
    async with async_session() as db:
        result = await db.execute(db.query(Kid).filter(Kid.id == kid_id))
        return result.scalar()

async def update_kid(kid_id: int, kid: models.Kid):
    async with async_session() as db:
        db_kid = await db.execute(db.query(Kid).filter(Kid.id == kid_id))
        db_kid = db_kid.scalar()
        if db_kid:
            db_kid.name = kid.name
            db_kid.age = kid.age
            await db.commit()
            await db.refresh(db_kid)
        return db_kid

async def delete_kid(kid_id: int):
    async with async_session() as db:
        db_kid = await db.execute(db.query(Kid).filter(Kid.id == kid_id))
        db_kid = db_kid.scalar()
        if db_kid:
            await db.delete(db_kid)
            await db.commit()
        return {"message": "Kid deleted"}

async def create_chore(chore: models.Chore):
    async with async_session() as db:
        db_chore = Chore(**chore.dict())
        db.add(db_chore)
        await db.commit()
        await db.refresh(db_chore)
        return db_chore

async def create_reward(reward: models.Reward):
    async with async_session() as db:
        db_reward = Reward(**reward.dict())
        db.add(db_reward)
        await db.commit()
        await db.refresh(db_reward)
        return db_reward

async def get_chores(skip: int = 0, limit: int = 100):
    async with async_session() as db:
        result = await db.execute(db.query(Chore).offset(skip).limit(limit))
        return result.scalars().all()

async def get_chore(chore_id: int):
    async with async_session() as db:
        result = await db.execute(db.query(Chore).filter(Chore.id == chore_id))
        return result.scalar()

async def update_chore(chore_id: int, chore: models.Chore):
    async with async_session() as db:
        db_chore = await db.execute(db.query(Chore).filter(Chore.id == chore_id))
        db_chore = db_chore.scalar()
        if db_chore:
            db_chore.name = chore.name
            db_chore.description = chore.description
            db_chore.points = chore.points
            db_chore.kid_id = chore.kid_id
            await db.commit()
            await db.refresh(db_chore)
        return db_chore

async def delete_chore(chore_id: int):
    async with async_session() as db:
        db_chore = await db.execute(db.query(Chore).filter(Chore.id == chore_id))
        db_chore = db_chore.scalar()
        if db_chore:
            await db.delete(db_chore)
            await db.commit()
        return db_chore

async def get_rewards(skip: int = 0, limit: int = 100):
    async with async_session() as db:
        result = await db.execute(db.query(Reward).offset(skip).limit(limit))
        return result.scalars().all()

async def get_reward(reward_id: int):
    async with async_session() as db:
        result = await db.execute(db.query(Reward).filter(Reward.id == reward_id))
        return result.scalar()

async def update_reward(reward_id: int, reward: models.Reward):
    async with async_session() as db:
        db_reward = await db.execute(db.query(Reward).filter(Reward.id == reward_id))
        db_reward = db_reward.scalar()
        if db_reward:
            db_reward.name = reward.name
            db_reward.description = reward.description
            db_reward.points = reward.poi            
            await db.commit()
            await db.refresh(db_reward)
        return db_reward

async def delete_reward(reward_id: int):
    async with async_session() as db:
        db_reward = await db.execute(db.query(Reward).filter(Reward.id == reward_id))
        db_reward = db_reward.scalar()
        if db_reward:
            await db.delete(db_reward)
            await db.commit()
        return db_reward