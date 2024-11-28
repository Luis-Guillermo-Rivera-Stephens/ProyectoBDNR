from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Union
import uuid
import bson 

class Game(BaseModel):
    gameID: str  
    played_counter: int
    time_playing: int
    category: str

class Category(BaseModel):
    category: str
    time_playing: int

class UserInfo(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    userID: Union[uuid.UUID, str] = Field(...)
    TimePlaying: int = Field(...)
    Games: List[Game] = []
    Categories: List[Category] = []