# REACT - Reason-Act-Observe

Táto schéma sa nachádza na stránke https://frompting.com/frameworks v sekcii Reasoning & Analysis.
Vybral som si túto schému, pretože by sa možno dala využiť na iterovanie pri predikovaní SQL dotazov, ak má SQL dotaz chybu tak vytvorí novú predikciu inak sa posunie na ďalšiu otázku.

## Template
[The task, and that it runs as a Thought / Action / Observation loop]

TOOLS: [Every tool with its signature, and that this list is COMPLETE]
[What the agent does NOT have — no memory, no interactive browsing]

LOOP: [One Thought, one Action, then STOP and wait. Never two Actions in a cycle]
[A fenced sample of one cycle]

RULES: [NEVER write an Observation yourself — they come from the tool runner. An invented one is indistinguishable from a real one and everything after it is fabricated]
[No summarising a page that was not fetched. Cite the source of every figure]

STOP WHEN: [success condition] / [hard cycle cap] / [when to ask instead of guessing]

## Prompt
Generate SQL queries for questions in restaurantsdataset.csv using restaurants-schema.csv. Save predictions to restaurantsdataset_predictions.csv. Use expected answers as references, never hardcode them or invent schema elements.

TOOLS: Use only tools provided by the execution environment and their documented signatures. Do not assume access to other files, databases, or services. Use SQL schema restaurants-schema.csv and do not assume any specific data in the tables.

LOOP: Start by taking a question in natural language from the dataset. Create prediction of SQL query that fits. Look at the expeccted answer and and prediciton. Repeat the cycle or move to tne next question in the file. 

Sample of the loop: Find the question - "What is the best californian in portola valley ?"
Predicted query: - "SELECT R.ID, R.NAME FROM RESTAURANT R JOIN LOCATION L ON R.ID = L.RESTAURANT_ID WHERE R.FOOD_TYPE = 'Californian' AND L.CITY_NAME = 'Portola Valley' ORDER BY R.RATING DESC LIMIT 1;" 
Look at the expected answer - "[[3, ""portola park""]]"
Query looks correct - continue with the next question.


RULES: Read both CSV files and identify their structure, schema, relationships, and SQL dialect. Generate one genuine SQL query per question using only supported tables and columns. Preserve question text and row order. Write a valid CSV with exactly two fields per row, original question and predicted SQL query. Write no other files except the output. Never fabricate observations nor claim actions succeeded without evidence. Do not overthink the questions, keep them simple and move on to next one quickly. CSV must have filednames as question and predicted_sql.

STOP WHEN: Success means the output file is written. If blocked by missing information or tool limitations, report the actual issue rather than guessing. Do not invent a cycle limit. Create only output file restaurants_dataset_predictions.csv.

