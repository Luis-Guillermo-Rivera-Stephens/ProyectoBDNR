import uuid
from typing import Optional
from pydantic import BaseModel, Field
import datetime

"""
admin_id UUID,
username TEXT,
password TEXT,
key text,
creation_date TIMESTAMP,
charge TEXT,
"""

class ADMIN(BaseModel):
    admin_id: str = Field(...)
    username: str = Field(...)
    password: str = Field(...)
    key: str = Field(...)
    creation_date: datetime.datetime = Field(...)
    charge: str = Field(...)


