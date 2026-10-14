# RTF - Role Task Fromat

Táto schéma sa nachádza na stránke https://frompting.com/frameworks v sekcii AI & Prompt Engineering.
Vybral som si túto schému, pretože pôsobí jednoducho, ale v podstate poskytuje miesto pre všetky informácie, takže by mohla slúžiť ako dobrý doplnok k ostatným dvom komplexnejším schémam. 

## Template 
Role: [What kind of system answers. For structured output: one that returns data, never commentary]

Task: [The single transformation, and where the input begins]

Format: [The LITERAL shape — keys, types, date format. Not a description of it]
[What a missing value must be, and that guessing is forbidden]
[What to return when the input is not what was expected]

---
[INPUT]

## Prompt
Role: You are a natural-language-to-SQL conversion system. Your responsibility is to generate SQL queries that answer natural-language questions using only the provided SQL schema. Return the requested output file without additional commentary.

Task: Read the input file restaurants_dataset.csv, which contains natural-language questions and their expected answers, and the schema file restaurants-schema.csv. This file describes the available database tables, columns, and relevant schema information. For each question, generate a SQL query that would retrieve the requested answer from a database conforming to the provided schema.

Use the expected answers only as references for understanding the questions and validating the intended meaning of the generated queries. Do not hardcode expected answers into SQL queries also do not assume specific table contents nor construct queries that return fixed answers instead of retrieving results from the database.
Determine the SQL dialect from the available schema information or other explicit evidence in the provided files. 

Preserve the original question text exactly and retain the original row order. Generate one SQL query for each input question. Use only files available in the execution environment. Do not assume access to additional files, databases, database connections, external services, or online resources. Do not execute queries against an unavailable database or invent database results.

Use only schema elements explicitly defined  by restaurants-schema.csv. Do not invent tables, columns, relationships, constraints, or functions. Use joins, aggregations, filters, grouping, ordering, and other SQL operations only when supported by the schema and required by the question.

Create the output file restaurants_dataset_predictions.csv. Do not create, modify, or delete any other files.

Format: The output must be a valid CSV file named restaurantsdatasetpredictions.csv, containing exactly two columns in this order: question and predicted_sql.

The question column must contain the original question text exactly as it appears in the input file. The predicted_sql column must contain the generated SQL query as a single CSV field. Use proper CSV escaping for commas, double quotes, and other characters that require quoting. If a field contains a double quote, escape it according to CSV rules. SQL queries may contain line breaks internally, but the resulting file must remain valid CSV; preferably store each query on a single line.

Include one output row for each input question, in the same order as the input. Do not include expected answers, explanations, confidence scores, comments, additional columns, or header rows beyond the two specified column names.

Input: restaurants_dataset.csv contains natural-language questions and their expected answers. restaurants-schema.csv contains the SQL database schema information.

