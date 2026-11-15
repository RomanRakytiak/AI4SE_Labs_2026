# Task 3 Report

## Deliverables

- Embedding script: `Week_06_Implementation/AI4SE_Playground/rag/embed_chunks.py`
- Chunk-embedding storage: `Week_06_Implementation/AI4SE_Playground/rag/chunk_embeddings.json`

## Design

The script represents each chunk as a list of 256 numbers. It finds words and
code identifiers in the chunk and uses a repeatable SHA-256 hash to assign each
token to one of the 256 positions. When a token appears more often, its
position gets a larger value. The vector is L2-normalized before it is stored.

The embeddings are stored in ordinary JSON. Each entry contains the original
chunk metadata together with its `embedding` array, so every vector remains
paired with the chunk from which it was created.

## Justification

This is a simple local approximation of an embedding: chunks containing
similar words and identifiers receive similar vectors.

This method does not require an internet connection, API key, downloaded AI
model, or third-party Python package. SHA-256 makes the result deterministic,
so the same chunk always produces the same vector. The 256 positions are
sufficient for this small repository while keeping the storage compact.
Different tokens can occasionally share a position, but this is an acceptable
trade-off for this assignment.

L2 normalization puts vectors on the same scale, so a longer chunk does not
appear more important merely because it contains more words. The normalized
vectors can later be compared using cosine similarity.

Ordinary JSON is used because it is readable, uses Python's built-in `json`
library, and keeps each chunk and its embedding together in one data structure.