# Agent Session Summary

## Context

This session completed Tasks 1–5 from the Week 06 implementation lab. The
repository `AI4SE_Labs_2026` was already a Git repository. The cloned
repository was therefore placed inside it as a nested repository:

```text
Week_06_Implementation/AI4SE_Playground/
```

The outer repository's `.git` directory was kept intact. The nested clone's
`.git` directory was later removed so the outer repository can track the
cloned files as ordinary files.

## Task 1: Clone a repository

The repository
`https://github.com/Neltharion59/AI4SE_Playground.git` was cloned by the
agent using PowerShell and Git:

```powershell
git clone https://github.com/Neltharion59/AI4SE_Playground.git `
  "Week_06_Implementation\AI4SE_Playground"
```

The clone was verified with `git rev-parse` and `git remote -v`.

The report was created at:

```text
Week_06_Implementation/Assignments/Task_1/Task_1_report.md
```

The report explains that the agent used the `git clone` command. It was later
updated to record the removal of the nested `.git` directory, as suggested by
the assignment, so the outer repository can track the cloned files normally.

## Task 2: Chunk the repository

The chunking implementation was placed in:

```text
AI4SE_Playground/rag/chunk_repository.py
```

The generated chunk data was stored in:

```text
AI4SE_Playground/rag/chunks.json
```

Design:

- UTF-8 text files are processed recursively.
- Files are split into chunks of 100 lines.
- Neighboring chunks overlap by 10 lines.
- Each chunk stores an identifier, relative file path, start line, end line,
  and content.
- `.git`, cache directories, binary files, and generated RAG data are
  excluded.
- Ordinary JSON is used instead of JSONL because it is easier to inspect and
  is sufficient for this small repository.

The report was created at:

```text
Week_06_Implementation/Assignments/Task_2/Task_2_report.md
```

Initially, the RAG directory was accidentally included in the chunks. The
chunking script was corrected to exclude `rag`, and the chunks and embeddings
were regenerated. The final result contained 59 repository chunks and no
chunks from `rag`.

## Task 3: Create chunk embeddings

The embedding script was placed in:

```text
AI4SE_Playground/rag/embed_chunks.py
```

The chunk-embedding pairs were stored in:

```text
AI4SE_Playground/rag/chunk_embeddings.json
```

Design:

- Words and code identifiers are extracted from each chunk.
- SHA-256 hashing maps each token to one of 256 vector positions.
- Token counts are accumulated in the vector.
- The vector is L2-normalized.
- The original chunk metadata and its embedding remain paired in JSON.

The method is a lightweight local approximation of an embedding. It was
chosen because it is deterministic, requires no API key or model download,
and uses no third-party embedding package. The 256 dimensions keep storage
compact for this repository. L2 normalization puts vectors on a common scale
so they can later be compared using cosine similarity.

The report was created at:

```text
Week_06_Implementation/Assignments/Task_3/Task_3_report.md
```

The generated storage contained 59 embeddings, each with 256 values.

## Task 4: Retrieve relevant chunks

The retrieval script was placed in:

```text
AI4SE_Playground/rag/retrieve_chunks.py
```

The Task 4 script was kept separate and was not rewritten for Task 5.

The script:

1. Accepts a textual task.
2. Embeds the task using the same embedding function as Task 3.
3. Compares the task vector with stored vectors.
4. Uses the dot product of normalized vectors as cosine similarity.
5. Sorts the chunks by score.
6. Returns the requested number of chunks using `--top-k`.

Example:

```powershell
python rag\retrieve_chunks.py `
  "How are orders priced and calculated?" --top-k 3
```

The script returned ranked chunks with scores and source locations. The
results also demonstrated a limitation of simple token hashing: it matches
shared words and identifiers but does not deeply understand meaning.

The report was created at:

```text
Week_06_Implementation/Assignments/Task_4/Task_4_report.md
```

## Task 5: Use RAG to implement missing methods

The input tasks were read from:

```text
Week_06_Implementation/Assignments/missing_code.json
```

The new integration script was placed in:

```text
AI4SE_Playground/rag/solve_tasks.py
```

It imports `retrieve` from Task 4 instead of modifying
`retrieve_chunks.py`.

The script workflow is:

1. Read each missing-method task.
2. Retrieve the top five chunks.
3. Build an RTF prompt.
4. Call an allowed LLM through `ChatOpenAI`.
5. Extract and clean the returned method.
6. Locate the target class and method using Python's AST.
7. Replace the method in the original source file.
8. Run the repository's built-in `unittest` suite.

The prompt uses the RTF structure established earlier in the course:

- **Role**: the model is a careful Python maintainer.
- **Task**: the target file, class, method, docstring, and retrieved context.
- **Format**: return only the complete Python method definition.

LangGraph was not used because this task is one sequential workflow, not a
multi-agent graph. The allowed models are validated by the script. No
explicit temperature is passed because some allowed reasoning models reject a
temperature value. The OpenAI key is read from the
`OPENAI_API_KEY` environment variable and is not stored in the repository.

Example:

```powershell
python rag\solve_tasks.py --model gpt-4o-mini
```

The first version attempted to run `pytest`, but the repository tests use
Python's standard-library `unittest`. The script was corrected to run:

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

The script also initially failed with a model configuration error because
`temperature=0` was sent to a model that only accepts its default
temperature. The explicit temperature setting was removed.

The generated methods correspond to:

- `OrderStatus.is_terminal`
- `InventoryLedger.__contains__`
- `Warehouse.stock_report`
- `OrderStateMachine.transition`
- `OrderLog.by_status`
- `Customer.can_afford`
- `Order.__len__`
- `BulkDiscountPricing.price`
- `EventBus.__contains__`
- `Money.__bool__`

## Task 5 test result

The command output was simplified and saved in:

```text
AI4SE_Playground/rag/log.txt
```

The recorded run:

```text
Ran 481 tests
FAILED (failures=5, errors=10)
```

The 15 failing test cases mapped to three generated methods:

| Generated method | Result |
|---|---|
| `OrderStatus.is_terminal` | 4 failures because the generated method did not preserve `@property`. |
| `InventoryLedger.__contains__` | 1 failure because an SKU at zero quantity was treated as absent. |
| `BulkDiscountPricing.price` | 10 errors because it referenced nonexistent `_minimum_quantity`. |

The other seven generated methods had no failures observed in this run:

- `Warehouse.stock_report`
- `OrderStateMachine.transition`
- `OrderLog.by_status`
- `Customer.can_afford`
- `Order.__len__`
- `EventBus.__contains__`
- `Money.__bool__`

“No failure observed” is not the same as proof of correctness. The full test
suite also covers unchanged repository functionality, so the 466 tests that
did not fail cannot be interpreted as a direct success rate for the generated
methods. The accurate conclusion is that the complete RAG pipeline executed,
but three generated methods require correction or review.

The detailed report is located at:

```text
Week_06_Implementation/Assignments/Task_5/Task_5_report.md
```
