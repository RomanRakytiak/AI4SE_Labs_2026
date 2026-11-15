# Task 4 Report

## Design

`retrieve_chunks.py` accepts a coding task description and an integer `n`
(`--top-k`). It converts the description into an embedding using the same
function as Task 3. It then calculates the dot product between the task
embedding and every stored chunk embedding, sorts the chunks by score, and
returns the `n` highest-scoring chunks.

## Justification

The embeddings generated in Task 3 are L2-normalized. For normalized vectors,
the dot product is equivalent to cosine similarity, which measures how closely
the token patterns point in the same direction. This is appropriate for the
chosen embedding representation and avoids adding a separate similarity
library.

The implementation performs a linear scan through the JSON storage. This is
simple, transparent, and sufficient for the 61 chunks in this small
repository. An indexed vector database would be more suitable for a much
larger collection, but would add unnecessary complexity for this assignment.
The `--top-k` option makes the number of retrieved chunks configurable.

## Example

The script can be tested from the `AI4SE_Playground` directory:

```powershell
python rag\retrieve_chunks.py "How are orders priced and calculated?" --top-k 3
```

The command prints the three most relevant chunks, including their similarity
scores and source locations:

```text
0.246599  playground/playground/orders.py:181-196
0.215458  playground/playground/base.py:1-85
0.203529  playground/playground/exceptions.py:1-56
```