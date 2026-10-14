# PRIME Purpose-Requirements-Instructions-Metrics-Examples

Táto schéma sa nachádza na stránke https://frompting.com/frameworks v sekcii Product & Growth.
Vybral som si túto schému, pretože jej formát pôsobí vhodný na túto úlohu, poskytuje miesto skoro pre všetky informácie.

## Template
[The endpoint or interface, and the ONLY facts available — limits, codes, lifetimes, where credentials come from]

Purpose:      [what it is for AND when NOT to call it — the limit usually implies an architecture]
Requirements: [what they need before the first call, and WHERE to get it]
Instructions: [the call, the parameters, and every response code with its CAUSE and its FIX]
Metrics:      [the numbers they must design around — lifetimes, limits, invalidation]
Examples:     [one working call with its real response, and one ERROR case. Copyable. Placeholders unmistakably placeholders]

[Put the first-time-integrator mistakes NEXT TO the code block, not in a preamble]
[No invented parameters, headers, codes or limits]

## Prompt
In restaurants-schema.csv file you have SQL database schema. In restaurants_dataset.csv file there are on each line a question written in natural language and the expected answer from the database. Your output should be written to restaurants_dataset_predictions.csv file. 

Purpose:      Generate SQL queries that answer the natural-language questions in restaurants_dataset.csv using the database schema defined in restaurants-schema.csv.
The goal is to infer the SQL logic from each question and using the available schema, and using the expected answers as reference.
Do not hardcode expected answers or constants in place of genuine queries or fake queries solely to reproduce the provided answers.
Do not invent tables, columns, relationships, or database capabilities that are unsupported by the schema.

Requirements: Before generating predictions: Read restaurants-schema.csv and identify the available tables, columns, keys, and relationships. Read restaurants_dataset.csv and identify the question and expected answer fields from its csv structure. Determine the SQL dialect from the schema. Preserve the original question text and row order. Use only the provided files available in the execution environment. Do not assume access to additional database files or services. Do not write any other files except the output file with the predictions.

Instructions: Create query predicitons from the questions written in natural language. You should output the predictions in a new csv file called restaurants_dataset_predictions.csv, where the first value is the question you are predicting SQL query for and the second value is the SQL query itself. CSV file must be a valid CSV file. CSV must have filednames as question and predicted_sql.

Metrics:      Do it fast, measure how long it took you to write predictions. Focus on the general SQL schema you are given and not the actual data in the database.

Examples:     one possible entry in the predictions file could this question followed by the predicted query: "What is the best californian in portola valley ?,"SELECT R.ID, R.NAME FROM RESTAURANT R JOIN LOCATION L ON R.ID = L.RESTAURANT_ID WHERE R.FOOD_TYPE = 'Californian' AND L.CITY_NAME = 'Portola Valley' ORDER BY R.RATING DESC LIMIT 1;" 

