from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path
import sys

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.common import ANALYTICS_SQL_PATH, DATABASE_PATH  # noqa: E402


def load_statements(path: Path):
    content = path.read_text(encoding="utf-8")
    statements = []
    buffer = []
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("--"):
            continue
        buffer.append(line)
        if stripped.endswith(";"):
            statement = "\n".join(buffer).strip()
            statement = statement[:-1].strip()
            if statement:
                statements.append(statement)
            buffer = []
    if buffer:
        statement = "\n".join(buffer).strip()
        if statement.endswith(";"):
            statement = statement[:-1].strip()
        if statement:
            statements.append(statement)
    return statements


def main():
    parser = argparse.ArgumentParser(description="Execute Week 8 analytics queries")
    parser.add_argument("--db", type=Path, default=DATABASE_PATH)
    parser.add_argument("--sql", type=Path, default=ANALYTICS_SQL_PATH)
    parser.add_argument("--limit", type=int, default=3)
    args = parser.parse_args()

    statements = load_statements(args.sql)
    with sqlite3.connect(args.db) as conn:
        for index, statement in enumerate(statements, 1):
            rows = conn.execute(statement).fetchmany(args.limit)
            columns = [col[0] for col in conn.execute(statement).description]
            print(f"Query {index:02d}: {len(rows)} sample rows")
            print("  columns:", ", ".join(columns))
            for row in rows:
                print("  ", tuple(row))
            print()


if __name__ == "__main__":
    main()

