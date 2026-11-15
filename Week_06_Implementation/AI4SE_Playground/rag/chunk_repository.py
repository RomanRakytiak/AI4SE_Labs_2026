"""Split a repository's text files into overlapping chunks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_CHUNK_SIZE = 100
DEFAULT_OVERLAP = 10
IGNORED_DIRECTORIES = {".git", "__pycache__", ".pytest_cache", "rag"}
IGNORED_FILES = {"chunks.json"}


def is_text_file(path: Path) -> bool:
    """Return whether a file can reasonably be processed as UTF-8 text."""
    try:
        path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return False
    return True


def chunk_file(
    path: Path,
    repository_root: Path,
    chunk_size: int,
    overlap: int,
) -> list[dict[str, object]]:
    """Create overlapping line-based chunks for one file."""
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    chunks: list[dict[str, object]] = []
    step = chunk_size - overlap

    for start in range(0, len(lines), step):
        chunk_lines = lines[start : start + chunk_size]
        if not chunk_lines:
            break
        chunks.append(
            {
                "id": f"chunk-{len(chunks):04d}",
                "file": path.relative_to(repository_root).as_posix(),
                "start_line": start + 1,
                "end_line": start + len(chunk_lines),
                "content": "".join(chunk_lines),
            }
        )
        if start + chunk_size >= len(lines):
            break

    return chunks


def build_chunks(
    repository_root: Path,
    chunk_size: int,
    overlap: int,
) -> list[dict[str, object]]:
    """Collect chunks from all supported text files in a repository."""
    chunks: list[dict[str, object]] = []
    for path in sorted(repository_root.rglob("*")):
        if not path.is_file():
            continue
        relative_parts = path.relative_to(repository_root).parts
        if any(part in IGNORED_DIRECTORIES for part in relative_parts):
            continue
        if path.name in IGNORED_FILES or not is_text_file(path):
            continue
        chunks.extend(chunk_file(path, repository_root, chunk_size, overlap))

    for index, chunk in enumerate(chunks):
        chunk["id"] = f"chunk-{index:04d}"
    return chunks


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "repository",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository to process (defaults to the parent repository)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "chunks.json",
        help="JSON file to create",
    )
    parser.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK_SIZE)
    parser.add_argument("--overlap", type=int, default=DEFAULT_OVERLAP)
    args = parser.parse_args()

    if args.chunk_size <= 0:
        parser.error("--chunk-size must be positive")
    if args.overlap < 0 or args.overlap >= args.chunk_size:
        parser.error("--overlap must be non-negative and smaller than --chunk-size")

    chunks = build_chunks(args.repository.resolve(), args.chunk_size, args.overlap)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(chunks, indent=2), encoding="utf-8")
    print(f"Wrote {len(chunks)} chunks to {args.output}")


if __name__ == "__main__":
    main()
