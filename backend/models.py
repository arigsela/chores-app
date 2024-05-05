from pydantic import BaseModel
from typing import Optional

class Kid(BaseModel):
    id: Optional[int]
    name: str
    age: int

class Chore(BaseModel):
    id: Optional[int]
    name: str
    description: str
    points: int
    kid_id: Optional[int]

class Reward(BaseModel):
    id: Optional[int]
    name: str
    description: str
    points: int