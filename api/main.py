from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from database import SessionLocal, engine
from auth import authenticate_user, create_access_token, get_password_hash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import logging

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/token", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Chore endpoints
@app.post("/chores", response_model=schemas.Chore)
async def create_chore(chore: schemas.ChoreCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_chore = models.Chore(**chore.dict())
    db.add(db_chore)
    db.commit()
    db.refresh(db_chore)
    return db_chore

@app.post("/kids/{kid_id}/chores/{chore_id}", response_model=schemas.KidChore)
async def complete_chore(kid_id: int, chore_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_kid_chore = models.KidChore(kid_id=kid_id, chore_id=chore_id)
    db.add(db_kid_chore)
    db.commit()
    db.refresh(db_kid_chore)
    return db_kid_chore

@app.get("/chores", response_model=List[schemas.Chore])
async def read_chores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    chores = db.query(models.Chore).offset(skip).limit(limit).all()
    return chores

@app.get("/chores/{chore_id}", response_model=schemas.Chore)
async def read_chore(chore_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_chore = db.query(models.Chore).filter(models.Chore.id == chore_id).first()
    if db_chore is None:
        raise HTTPException(status_code=404, detail="Chore not found")
    return db_chore

@app.put("/chores/{chore_id}", response_model=schemas.Chore)
async def update_chore(chore_id: int, chore: schemas.ChoreUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_chore = db.query(models.Chore).filter(models.Chore.id == chore_id).first()
    if db_chore is None:
        raise HTTPException(status_code=404, detail="Chore not found")
    
    if chore.kid_id is not None:
        db_kid = db.query(models.Kid).filter(models.Kid.id == chore.kid_id).first()
        if db_kid is None:
            raise HTTPException(status_code=400, detail="Invalid kid_id")
    
    update_data = chore.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_chore, key, value)
    db.commit()
    db.refresh(db_chore)
    return db_chore


@app.delete("/chores/{chore_id}")
async def delete_chore(chore_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_chore = db.query(models.Chore).filter(models.Chore.id == chore_id).first()
    if db_chore is None:
        raise HTTPException(status_code=404, detail="Chore not found")
    db.delete(db_chore)
    db.commit()
    return {"message": "Chore deleted successfully"}

# Reward endpoints
@app.post("/rewards", response_model=schemas.Reward)
async def create_reward(reward: schemas.RewardCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_reward = models.Reward(**reward.dict())
    db.add(db_reward)
    db.commit()
    db.refresh(db_reward)
    return db_reward

@app.get("/rewards", response_model=List[schemas.Reward])
async def read_rewards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    rewards = db.query(models.Reward).offset(skip).limit(limit).all()
    return rewards

# Kid endpoints
@app.post("/kids", response_model=schemas.Kid)
async def create_kid(kid: schemas.KidCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_kid = models.Kid(**kid.dict())
    db.add(db_kid)
    db.commit()
    db.refresh(db_kid)
    return db_kid

@app.get("/kids", response_model=List[schemas.Kid])
async def read_kids(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    kids = db.query(models.Kid).offset(skip).limit(limit).all()
    return kids

@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if the username already exists
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Create a new user with hashed password
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/kids/{kid_id}/rewards", response_model=schemas.KidReward)
async def award_reward_to_kid(kid_id: int, reward_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_kid_reward = models.KidReward(kid_id=kid_id, reward_id=reward_id)
    db.add(db_kid_reward)
    db.commit()
    db.refresh(db_kid_reward)
    return db_kid_reward