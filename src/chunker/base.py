# src/chunker/base.py
from abc import ABC, abstractmethod
from typing import List
from src.models import Chunk

class BaseChunker(ABC):
    def __init__(self, max_size: int = 2000):
        self.max_size = max_size

    @abstractmethod
    def chunk(self, text: str, file_path: str) -> List[Chunk]:
        pass
