from pydantic import BaseModel
from typing import List, Union

class Categoria(BaseModel):
    uid: str
    c_name: str

class Juego(BaseModel):
    uid: str
    j_name: str
    description: str
    category: Union[str, dict]  # Puede ser un UID o un diccionario con "uid"
    related_with: List[Union[str, dict]]  # Lista de UID o diccionarios con "uid"

