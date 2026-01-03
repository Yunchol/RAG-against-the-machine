# src/__main__.py
from src.chunker.loader import load_and_chunk_repo

if __name__ == "__main__":
    chunks = load_and_chunk_repo("sample_repo")
    print(f"chunks: {len(chunks)}")

    for c in chunks:
        print(c)
        print()
