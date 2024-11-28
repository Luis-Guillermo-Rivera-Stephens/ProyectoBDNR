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
    account_id: str = Field(...)
    username: str = Field(...)
    password: str = Field(...)
    creation_date: datetime.datetime = Field(...)