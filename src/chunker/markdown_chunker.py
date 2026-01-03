# src/chunker/markdown_chunker.py
from typing import List
from src.models import Chunk
from src.chunker.base import BaseChunker
import re

class MarkdownChunker(BaseChunker):
    def chunk(self, text: str, file_path: str) -> List[Chunk]:
        chunks: List[Chunk] = []
        matches = list(re.finditer(r"^#+ .*$", text, re.MULTILINE))

        if not matches:
            return self._fallback(text, file_path)

        for i, m in enumerate(matches):
            start = m.start()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            chunk_text = text[start:end]

            if len(chunk_text) > self.max_size:
                chunks.extend(self._fallback(chunk_text, file_path, offset=start))
            else:
                chunks.append(
                    Chunk(
                        text=chunk_text,
                        file_path=file_path,
                        start=start,
                        end=end,
                    )
                )

        return chunks

    def _fallback(self, text: str, file_path: str, offset: int = 0) -> List[Chunk]:
        return [
            Chunk(
                text=text[i:i + self.max_size],
                file_path=file_path,
                start=offset + i,
                end=offset + min(i + self.max_size, len(text)),
            )
            for i in range(0, len(text), self.max_size)
        ]
