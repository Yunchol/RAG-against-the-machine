# src/__main__.py
from src.chunker.loader import load_and_chunk_repo
from src.search import BM25SearchEngine

if __name__ == "__main__":
    chunks = load_and_chunk_repo("sample_repo")
    print(f"chunks: {len(chunks)}")

    engine = BM25SearchEngine(chunks)

    results = engine.search("OpenAI compatible server", k=3)

    print("\n=== search results ===")
    for r in results:
        print(r.file_path, r.start, r.end)
        print(r.text)
        print("----")
