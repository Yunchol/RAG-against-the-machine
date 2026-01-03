# src/cli.py
from typing import List
from src.chunker.loader import load_and_chunk_repo
from src.search import BM25SearchEngine
from src.models import Chunk


class CLI:
    def index(self, repo_path: str = "sample_repo"):
        """
        Create chunks from repository.
        """
        chunks = load_and_chunk_repo(repo_path)
        print(f"Indexed {len(chunks)} chunks")

    def search(self, query: str, repo_path: str = "sample_repo", k: int = 5):
        """
        Search relevant chunks.
        """
        chunks = load_and_chunk_repo(repo_path)
        engine = BM25SearchEngine(chunks)

        results: List[Chunk] = engine.search(query, k)

        print(f"\nTop {k} results:\n")
        for c in results:
            print(f"{c.file_path} [{c.start}:{c.end}]")
            print(c.text)
            print("----")
