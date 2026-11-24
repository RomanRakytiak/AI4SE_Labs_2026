# Assessment by mimo-2.6-flash

# Week 03 Prompting
- Awarded: 4b out of 5b
- Commentary: The student delivered all four deliverables with real artifacts: three well-formed prompting frameworks, six runs of SQL-prediction outputs with timing metadata, an implemented and applied novel metric, and a comparative evaluation report. Task 1 and Task 3 fully satisfy their specifications. Task 2's report stops at comparing inference times/steps and lacks the required quality comparison and visualization, while Task 4 provides solid tables and interpretation but does not actually perform a statistical significance test and offers only a thin explanation of why the prompt differences occur. Note: Metriky.xlsx could not be opened (binary file), so the graphs it reportedly contains were judged only from the surrounding text.

## Task 1
- Awarded: 1b   (max 1b)
- Commentary: Three frameworks (PRIME, ReAct, RTF) were chosen from frompting.com with the exact source section cited for each; neither ROSES nor zero-shot prompting was used. Each file contains the framework template, a concrete prompt tailored to the Task 2 SQL-generation problem, and a rationale with an expectation of behaviour ("why chosen / what to expect"), satisfying both the prompt-file and report requirements. Rationales are brief but explicit and appropriate.

## Task 2
- Awarded: 0.5b   (max 1b)
- Commentary: Full predictions are stored for all three prompts, each run twice in its own folder (155 valid question/predicted_sql rows each), and Výsledky.md identifies the model (GPT-5.6 Luna) and measures inference times and agent steps per run - satisfying the data and timing requirements. However, the report only compares time/steps; it never compares how well the problems were actually solved (accuracy results appear only later in Task 4), and the required visualization is entirely missing from Task 2. Half credit for complete data with only a partial report.

## Task 3
- Awarded: 1b   (max 1b)
- Commentary: The student proposes an original metric (SQL token count per query via a simple regex tokenizer), defends its applicability (penalises unnecessarily long queries), explicitly argues it complements rather than replaces accuracy ("sama o sebe urcite nestaci... moze sluzit ako doplnok"), implements it in evaluate_prediction_length.py, and computes values for all six Task 2 prediction sets with a per-prompt comparison report and interpretation. All required outputs are present; the metric is simple but legitimate and well-motivated.

## Task 4
- Awarded: 1.5b   (max 2b)
- Commentary: Evaluácia.md delivers tables (run 1, run 2, overall averages, accuracy deltas), interpretation of time/accuracy/length trade-offs, and an honest cross-run comparison including a note that only two iterations were possible (credit limit) - graphs are claimed to live in Metriky.xlsx, which could not be viewed here. Two explicit requirements remain unfulfilled: statistical significance is declared undeterminable instead of actually being tested (per-question correctness for 155 questions per run would allow McNemar/bootstrap tests), and the "why" analysis barely considers the prompt wording, model, or coding agent as causal factors, mostly restating numbers and attributing gaps to luck.