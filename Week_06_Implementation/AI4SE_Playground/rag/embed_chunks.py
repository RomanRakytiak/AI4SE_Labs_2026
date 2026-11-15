"""Create deterministic vector embeddings for repository chunks."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path


DEFAULT_DIMENSIONS = 256
TOKEN_PATTERN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def tokens(text: str) -> list[str]:
    """Extract code-friendly word and identifier tokens."""
    return [match.group(0).lower() for match in TOKEN_PATTERN.finditer(text)]


def token_index(token: str, dimensions: int) -> int:
    """Map a token to a stable position in the fixed-size vector."""
    digest = hashlib.sha256(token.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") % dimensions


def embed(text: str, dimensions: int = DEFAULT_DIMENSIONS) -> list[float]:
    """Create an L2-normalized term-frequency vector."""
    if dimensions <= 0:
        raise ValueError("dimensions must be positive")

    vector = [0.0] * dimensions
    word_tokens = tokens(text)
    for token in word_tokens:
        vector[token_index(token, dimensions)] += 1.0

    norm = math.sqrt(sum(value * value for value in vector))
    if norm:
        vector = [round(value / norm, 6) for value in vector]
    return vector


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(__file__).resolve().parent / "chunks.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "chunk_embeddings.json",
    )
    parser.add_argument("--dimensions", type=int, default=DEFAULT_DIMENSIONS)
    args = parser.parse_args()

    if args.dimensions <= 0:
        parser.error("--dimensions must be positive")

    chunks = json.loads(args.input.read_text(encoding="utf-8"))
    embedded_chunks = [
        {
            "chunk": chunk,
            "embedding": embed(chunk["content"], args.dimensions),
        }
        for chunk in chunks
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(embedded_chunks, indent=2), encoding="utf-8")
    print(f"Wrote {len(embedded_chunks)} chunk embeddings to {args.output}")


if __name__ == "__main__":
    main()
