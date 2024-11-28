import uuid
from typing import Optional
from pydantic import BaseModel, Field
import datetime

"""
    account_id UUID,
    game_id UUID,
    description TEXT,
    start TIMESTAMP,
    end TIMESTAMP
"""

class LOG(BaseModel):
    account_id: str = Field(default_factory=uuid.uuid4, alias="_account_id")
    game_id: str = Optional[str]
    description: str = Field(...)
    start: datetime.datetime = Field(...)
    end: datetime.datetime = Field(...)



