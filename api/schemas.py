from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class KidBase(BaseModel):
    name: str

class KidCreate(KidBase):
    pass

class Kid(KidBase):
    id: int
    chores: List["Chore"] = []
    rewards: List["Reward"] = []

    class Config:
        from_attributes = True

class ChoreBase(BaseModel):
    name: str
    points: int

class ChoreCreate(ChoreBase):
    pass

class Chore(ChoreBase):
    id: int

    class Config:
        from_attributes = True
        
class ChoreUpdate(BaseModel):
    name: Optional[str]
    points: Optional[int]
    kid_id: Optional[int]

    class Config:
        from_attributes = True

class KidChoreBase(BaseModel):
    kid_id: int
    chore_id: int

class KidChoreCreate(KidChoreBase):
    pass

class KidChore(KidChoreBase):
    id: int
    completed_at: datetime

    class Config:
        from_attributes = True

class RewardBase(BaseModel):
    name: str
    points: int

class RewardCreate(RewardBase):
    pass

class Reward(RewardBase):
    id: int

    class Config:
        from_attributes = True
        
class KidReward(BaseModel):
    id: int
    kid_id: int
    reward_id: int
    awarded_at: datetime

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True
        
class Token(BaseModel):
    access_token: str
    token_type: str

Kid.update_forward_refs()