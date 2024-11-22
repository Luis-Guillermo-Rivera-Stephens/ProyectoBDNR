import uuid
from typing import Optional
from pydantic import BaseModel, Field
import datetime

"""
    account_id UUID,
    username TEXT,
    password TEXT,
    creation_date TIMESTAMP,
"""

class ACCOUNT(BaseModel):
    account_id: uuid.UUID = Field(default_factory=uuid.uuid4, alias="_account_id")
    username: str = Field(...)
    password: str = Field(...)
    creation_date: datetime.datetime = Field(...)