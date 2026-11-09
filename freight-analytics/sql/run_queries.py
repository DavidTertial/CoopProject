"""
sql/run_queries.py
Run the named queries in sql/analysis_queries.sql against data/freight.db.

    python sql/run_queries.py        # run all
    python sql/run_queries.py 2 4    # run queries 2 and 4
"""

import os
import re
import sqlite3
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
SQL_FILE = os.path.join(HERE, "analysis_queries.sql")
DB_PATH = os.path.join(HERE, "..", "data", "freight.db")


def load_queries(path: str = SQL_FILE) -> list[tuple[str, str]]:
    text = open(path, encoding="utf-8").read()
    parts = re.split(r"^-- name:\s*(.+)$", text, flags=re.M)
    # parts = [preamble, name1, body1, name2, body2, ...]
    return [(parts[i].strip(), parts[i + 1].strip()) for i in range(1, len(parts), 2)]


def main(selected: list[str]):
    pd.set_option("display.width", 140)
    with sqlite3.connect(DB_PATH) as conn:
        for name, sql in load_queries():
            if selected and name.split(".")[0] not in selected:
                continue
            print(f"\n=== {name}")
            print(pd.read_sql(sql, conn).to_string(index=False))


if __name__ == "__main__":
    main(sys.argv[1:])
