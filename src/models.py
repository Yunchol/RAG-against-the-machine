# src/models.py
from pydantic import BaseModel

class Chunk(BaseModel):
    text: str
    file_path: str
    start: int
    end: int
