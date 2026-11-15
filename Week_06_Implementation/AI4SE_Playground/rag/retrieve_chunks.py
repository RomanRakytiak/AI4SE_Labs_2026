"""Retrieve the repository chunks most relevant to a task description."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from embed_chunks import embed


DEFAULT_STORAGE = Path(__file__).resolve().parent / "chunk_embeddings.json"


def similarity(first: list[float], second: list[float]) -> float:
    """Calculate the dot product of two normalized vectors."""
    if len(first) != len(second):
        raise ValueError("embeddings must have the same number of dimensions")
    return sum(left * right for left, right in zip(first, second))


def retrieve(
    task: str,
    storage_path: Path = DEFAULT_STORAGE,
    top_k: int = 5,
) -> list[dict[str, object]]:
    """Return up to top_k chunks ranked by similarity to a task."""
    if top_k <= 0:
        raise ValueError("top_k must be positive")

    stored_chunks = json.loads(storage_path.read_text(encoding="utf-8"))
    task_embedding = embed(task)
    ranked = [
        {
            "score": similarity(task_embedding, item["embedding"]),
            "chunk": item["chunk"],
        }
        for item in stored_chunks
    ]
    ranked.sort(key=lambda item: item["score"], reverse=True)
    return ranked[:top_k]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", help="coding task used for retrieval")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--input", type=Path, default=DEFAULT_STORAGE)
    args = parser.parse_args()

    if args.top_k <= 0:
        parser.error("--top-k must be positive")

    for result in retrieve(args.task, args.input, args.top_k):
        chunk = result["chunk"]
        print(
            f'{result["score"]:.6f}  {chunk["file"]}:'
            f'{chunk["start_line"]}-{chunk["end_line"]}'
        )
        print(chunk["content"])
        print("-" * 60)


if __name__ == "__main__":
    main()
