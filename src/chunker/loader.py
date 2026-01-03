# src/chunker/loader.py
from pathlib import Path
from typing import List
from src.models import Chunk
from src.chunker.python_chunker import PythonChunker
from src.chunker.markdown_chunker import MarkdownChunker

def load_and_chunk_repo(repo_path: str, max_size: int = 2000) -> List[Chunk]:
    repo = Path(repo_path)
    chunks: List[Chunk] = []

    py_chunker = PythonChunker(max_size)
    md_chunker = MarkdownChunker(max_size)

    for file in repo.rglob("*"):
        if file.suffix not in {".py", ".md"}:
            continue

        try:
            text = file.read_text(encoding="utf-8")
        except Exception:
            continue

        if file.suffix == ".py":
            chunks.extend(py_chunker.chunk(text, str(file)))
        else:
            chunks.extend(md_chunker.chunk(text, str(file)))

    return chunks
