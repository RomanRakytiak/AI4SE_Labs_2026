# To run this script, provide a CSV file containing predicted SQL queries.
# The script will count the words in each predicted SQL query and calculate
# the average, minimum, maximum, and total word counts.

import csv
from pathlib import Path
import re

DATA_DIR = Path(__file__).resolve().parent
PREDICTIONS_PATH = DATA_DIR / "restaurants_dataset_predictions.csv"



SQL_TOKEN_PATTERN = re.compile(r"[^\s,;.]+")

def count_words(query):
    return len(SQL_TOKEN_PATTERN.findall(query))


def main():
    csv.field_size_limit(1_000_000_000)

    total_queries = 0
    total_words = 0
    min_words = None
    max_words = 0

    with PREDICTIONS_PATH.open(encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)

        if "predicted_sql" not in (reader.fieldnames or []):
            raise ValueError(
                f"Missing 'predicted_sql' column in {PREDICTIONS_PATH}"
            )

        for line_number, row in enumerate(reader, start=2):
            query = row["predicted_sql"]

            if not query or not query.strip():
                raise ValueError(
                    f"Empty predicted SQL query on line {line_number} "
                    f"of {PREDICTIONS_PATH}"
                )

            word_count = count_words(query)

            total_queries += 1
            total_words += word_count

            if min_words is None or word_count < min_words:
                min_words = word_count

            if word_count > max_words:
                max_words = word_count

    if total_queries == 0:
        raise ValueError(f"No predictions found in {PREDICTIONS_PATH}")

    average_words = total_words / total_queries

    print(f"Total queries: {total_queries}")
    print(f"Total sql tokens: {total_words}")
    print(f"Average sql tokens per query: {average_words:.2f}")
    print(f"Minimum sql tokens per query: {min_words}")
    print(f"Maximum sql tokens per query: {max_words}")


if __name__ == "__main__":
    main()