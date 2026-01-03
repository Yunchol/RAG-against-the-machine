from typing import List
import bm25s
from src.models import Chunk

class BM25SearchEngine:
    def __init__(self, chunks: List[Chunk]):
        self.chunks = chunks

        # ① corpus: List[List[str]]
        self.corpus = [chunk.text.split() for chunk in chunks]

        # ② BM25 を作る
        self.bm25 = bm25s.BM25()

        # ③ corpus を渡して index
        self.bm25.index(self.corpus)

    def search(self, query: str, k: int = 5) -> List[Chunk]:
        # クエリも token 化
        query_tokens = query.split()

        scores = self.bm25.get_scores(query_tokens)

        scored_chunks = list(zip(self.chunks, scores))
        scored_chunks.sort(key=lambda x: x[1], reverse=True)

        return [chunk for chunk, score in scored_chunks[:k]]
