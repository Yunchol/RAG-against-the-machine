# src/__main__.py
import fire
from src.cli import CLI

def main():
    fire.Fire(CLI)

if __name__ == "__main__":
    main()

#python -m src search "OpenAI compatible server" --k 3

#python -m src index

#python -m src search "子供が怪我をした場合の対処は？" --k 3