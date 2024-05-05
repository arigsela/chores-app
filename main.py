from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_async_session, engine, Base
import models, database
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        logger.error(f"An error occurred during database creation: {e}")
        raise e
  

@app.post("/kids", response_model=models.Kid)
async def create_kid(kid: models.Kid, db: AsyncSession = Depends(get_async_session)):
    return await database.create_kid(kid)

@app.get("/kids", response_model=List[models.Kid])
async def read_kids(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)):
    return await database.get_kids(skip=skip, limit=limit)

@app.get("/kids/{kid_id}", response_model=models.Kid)
async def read_kid(kid_id: int, db: AsyncSession = Depends(get_async_session)):
    return await database.get_kid(kid_id=kid_id)

@app.put("/kids/{kid_id}", response_model=models.Kid)
async def update_kid(kid_id: int, kid: models.Kid, db: AsyncSession = Depends(get_async_session)):
    return await database.update_kid(kid_id=kid_id, kid=kid)

@app.delete("/kids/{kid_id}")
async def delete_kid(kid_id: int, db: AsyncSession = Depends(get_async_session)):
    return await database.delete_kid(kid_id=kid_id)

@app.post("/chores", response_model=models.Chore)
async def create_chore(chore: models.Chore, db: AsyncSession = Depends(get_async_session)):
    return await database.create_chore(chore=chore)

@app.post("/rewards", response_model=models.Reward)
async def create_reward(reward: models.Reward, db: AsyncSession = Depends(get_async_session)):
    return await database.create_reward(reward=reward)

# Chore endpoints
@app.post("/chores", response_model=models.Chore)
async def create_chore(chore: models.Chore, db: AsyncSession = Depends(get_async_session)):
    return await database.create_chore(chore=chore)

@app.get("/chores", response_model=List[models.Chore])
async def read_chores(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)):
    return await database.get_chores(skip=skip, limit=limit)

@app.get("/chores/{chore_id}", response_model=models.Chore)
async def read_chore(chore_id: int, db: AsyncSession = Depends(get_async_session)):
    chore = await database.get_chore(chore_id=chore_id)
    if chore is None:
        raise HTTPException(status_code=404, detail="Chore not found")
    return chore

@app.put("/chores/{chore_id}", response_model=models.Chore)
async def update_chore(chore_id: int, chore: models.Chore, db: AsyncSession = Depends(get_async_session)):
    updated_chore = await database.update_chore(chore_id=chore_id, chore=chore)
    if updated_chore is None:
        raise HTTPException(status_code=404, detail="Chore not found")
    return updated_chore

@app.delete("/chores/{chore_id}")
async def delete_chore(chore_id: int, db: AsyncSession = Depends(get_async_session)):
    deleted_chore = await database.delete_chore(chore_id=chore_id)
    if deleted_chore is None:
        raise HTTPException(status_code=404, detail="Chore not found")
    return {"message": "Chore deleted successfully"}

# Reward endpoints
@app.post("/rewards", response_model=models.Reward)
async def create_reward(reward: models.Reward, db: AsyncSession = Depends(get_async_session)):
    return await database.create_reward(reward=reward)

@app.get("/rewards", response_model=List[models.Reward])
async def read_rewards(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)):
    return await database.get_rewards(skip=skip, limit=limit)

@app.get("/rewards/{reward_id}", response_model=models.Reward)
async def read_reward(reward_id: int, db: AsyncSession = Depends(get_async_session)):
    reward = await database.get_reward(reward_id=reward_id)
    if reward is None:
        raise HTTPException(status_code=404, detail="Reward not found")
    return reward

@app.put("/rewards/{reward_id}", response_model=models.Reward)
async def update_reward(reward_id: int, reward: models.Reward, db: AsyncSession = Depends(get_async_session)):
    updated_reward = await database.update_reward(reward_id=reward_id, reward=reward)
    if updated_reward is None:
        raise HTTPException(status_code=404, detail="Reward not found")
    return updated_reward

@app.delete("/rewards/{reward_id}")
async def delete_reward(reward_id: int, db: AsyncSession = Depends(get_async_session)):
    deleted_reward = await database.delete_reward(reward_id=reward_id)
    if deleted_reward is None:
        raise HTTPException(status_code=404, detail="Reward not found")
    return {"message": "Reward deleted successfully"}