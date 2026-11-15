# Task 2 Report

## Deliverables

- Chunking script: `Week_06_Implementation/AI4SE_Playground/rag/chunk_repository.py`
- Chunk data: `Week_06_Implementation/AI4SE_Playground/rag/chunks.json`

## Design decisions

The script splits each UTF-8 text file into chunks of 100 lines with an
overlap of 10 lines. A line-based method is appropriate for a small source
repository because it keeps Python functions, tests, and configuration
sections readable instead of cutting text at arbitrary character positions.
The overlap preserves context when a function crosses a chunk boundary.

Each chunk is represented as an object containing a unique identifier, the
relative file path, the first and last line numbers, and the chunk content.
All objects are stored in one ordinary JSON array. This format uses Python's
built-in `json` library, is easy to inspect, and is sufficient for this
repository's size.

The script skips `.git`, Python cache directories, generated `chunks.json`,
and files that cannot be decoded as UTF-8. Chunk size and overlap can be
changed with command-line options.