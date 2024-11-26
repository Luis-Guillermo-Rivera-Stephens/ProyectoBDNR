from pydantic import BaseModel, Field
from typing import Optional, List
import uuid

class Game(BaseModel):
    gameID: str = Field(..., alias="_gameID")  
    played_counter: int
    time_playing: int
    category: str

class Category(BaseModel):
    category: str
    time_playing: int

class UserInfo(BaseModel):
    userID: uuid.UUID = Field(...)
    TimePlaying: int
    Games: List[Game] = []
    Categories: List[Category] = []