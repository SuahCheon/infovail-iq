"""Initialise the SQLite database for infovail-iq.

Usage:
    uv run python scripts/setup_db.py              # default path
    uv run python scripts/setup_db.py --db my.db   # custom path
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure project root is on sys.path so `pipeline` is importable.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pipeline.ingestion.db import DEFAULT_DB_PATH, get_connection, init_db


def main() -> None:
    parser = argparse.ArgumentParser(description="Create infovail-iq SQLite DB.")
    parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB_PATH,
        help=f"Database file path (default: {DEFAULT_DB_PATH})",
    )
    args = parser.parse_args()

    conn = get_connection(args.db)
    init_db(conn)

    # Quick sanity check
    tables = [
        row[0]
        for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
    ]
    print(f"DB created at: {args.db.resolve()}")
    print(f"Tables: {', '.join(tables)}")

    conn.close()


if __name__ == "__main__":
    main()
