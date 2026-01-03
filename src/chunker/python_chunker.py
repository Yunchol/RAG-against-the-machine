# src/chunker/python_chunker.py
import ast
from typing import List
from src.models import Chunk
from src.chunker.base import BaseChunker

class PythonChunker(BaseChunker):
    def chunk(self, text: str, file_path: str) -> List[Chunk]:
        chunks: List[Chunk] = []

        try:
            tree = ast.parse(text)
            lines = text.splitlines(keepends=True)

            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    start = node.lineno - 1
                    end = (node.end_lineno or node.lineno) - 1
                    chunk_text = "".join(lines[start:end + 1])

                    if len(chunk_text) <= self.max_size:
                        chunks.append(
                            Chunk(
                                text=chunk_text,
                                file_path=file_path,
                                start=sum(len(l) for l in lines[:start]),
                                end=sum(len(l) for l in lines[:end + 1]),
                            )
                        )

        except SyntaxError:
            pass  # fallbackへ

        # fallback：2000文字スライス
        if not chunks:
            for i in range(0, len(text), self.max_size):
                chunks.append(
                    Chunk(
                        text=text[i:i + self.max_size],
                        file_path=file_path,
                        start=i,
                        end=min(i + self.max_size, len(text)),
                    )
                )

        return chunks
