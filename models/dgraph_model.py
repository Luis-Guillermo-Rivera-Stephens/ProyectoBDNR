from pydantic import BaseModel
from typing import List

class Categoria(BaseModel):
    _id: str
    name: str

class Juego(BaseModel):
    _id: str
    name: str
    description: str
    category: str
    related_with: List[str]

