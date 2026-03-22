"""Collect all PoC keywords across blog/news/cafearticle channels.

Reads the keyword list from POC_SCENARIO.md §5, runs NaverClient.collect()
for every keyword × channel combination, preprocesses via preprocessor.py,
and stores the results in SQLite.

Usage:
    uv run python scripts/collect_all.py
    uv run python scripts/collect_all.py --dry-run        # API calls only, no DB write
    uv run python scripts/collect_all.py --db custom.db   # custom DB path
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pipeline.ingestion.db import (
    DEFAULT_DB_PATH,
    count_posts,
    get_connection,
    init_db,
    upsert_posts,
)
from pipeline.ingestion.naver_client import Channel, NaverClient
from pipeline.ingestion.preprocessor import preprocess

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# PoC keywords (POC_SCENARIO.md §5)
# ------------------------------------------------------------------

KEYWORDS_PRIMARY = [
    "코로나 백신 이물질",
    "감사원 백신",
    "코로나 백신 곰팡이",
]

KEYWORDS_BASELINE = [
    "코로나 백신 피해",
    "백신 피해 보상",
    "코로나 백신 부작용",
    "백신 피해자 모임",
]

KEYWORDS_POLITICAL = [
    "정은경 백신",
    "코로나 백신 정부 책임",
]

ALL_KEYWORDS = KEYWORDS_PRIMARY + KEYWORDS_BASELINE + KEYWORDS_POLITICAL

CHANNELS: list[Channel] = ["blog", "news"]

# Naver API channel → DB channel name (DATA_GOVERNANCE §3.2)
# cafearticle excluded: Naver Search API does not return date fields for cafe
CHANNEL_MAP = {"news": "news_comment", "blog": "blog"}

DATE_FROM = "2026-02-07"
DATE_TO = "2026-03-04"


# ------------------------------------------------------------------
# Core logic
# ------------------------------------------------------------------

def collect_and_store(
    *,
    db_path: Path = DEFAULT_DB_PATH,
    dry_run: bool = False,
    date_from: str = DATE_FROM,
    date_to: str = DATE_TO,
) -> None:
    """Run the full collection pipeline."""

    # --- DB setup ---
    conn = None
    if not dry_run:
        conn = get_connection(db_path)
        init_db(conn)

    # Track counts for the summary table: {(keyword, channel): count}
    stats: dict[tuple[str, str], int] = {}
    total_api = 0
    total_new = 0

    with NaverClient() as client:
        for keyword in ALL_KEYWORDS:
            for channel in CHANNELS:
                label = f"{keyword}  [{channel}]"
                logger.info("▶ Collecting: %s  (%s ~ %s)", label, date_from, date_to)

                try:
                    raw = client.collect(
                        keyword=keyword,
                        channel=channel,
                        date_from=date_from,
                        date_to=date_to,
                    )
                except Exception:
                    logger.exception("  FAILED: %s", label)
                    stats[(keyword, channel)] = 0
                    continue

                logger.info("  API returned %d items", len(raw))
                total_api += len(raw)

                # --- Preprocess ---
                rows = preprocess(raw)

                # Map API channel name to DB channel name
                db_channel = CHANNEL_MAP[channel]
                for row in rows:
                    row["channel"] = db_channel

                # --- Store ---
                inserted = 0
                if conn and rows:
                    inserted = upsert_posts(conn, rows)
                    logger.info(
                        "  DB: +%d new  (%d skipped)",
                        inserted,
                        len(rows) - inserted,
                    )

                stats[(keyword, channel)] = len(raw)
                total_new += inserted

                # courtesy delay between keyword×channel combos
                time.sleep(0.3)

    # ------------------------------------------------------------------
    # Summary table
    # ------------------------------------------------------------------
    hdr_kw = "Keyword"
    hdr_ch = {ch: CHANNEL_MAP[ch] for ch in CHANNELS}
    col_w = 12

    print("\n" + "=" * 72)
    print("  COLLECTION SUMMARY")
    print(f"  Period : {date_from} ~ {date_to}")
    print(f"  API total : {total_api}  |  DB new rows : {total_new}")
    print("=" * 72)

    # Header
    header = f"{'Keyword':<28s}"
    for ch in CHANNELS:
        header += f"  {hdr_ch[ch]:>{col_w}s}"
    header += f"  {'TOTAL':>{col_w}s}"
    print(header)
    print("-" * len(header))

    # Rows
    grand_totals = {ch: 0 for ch in CHANNELS}
    for keyword in ALL_KEYWORDS:
        row_str = f"{keyword:<28s}"
        row_sum = 0
        for ch in CHANNELS:
            cnt = stats.get((keyword, ch), 0)
            row_str += f"  {cnt:>{col_w}d}"
            row_sum += cnt
            grand_totals[ch] += cnt
        row_str += f"  {row_sum:>{col_w}d}"
        print(row_str)

    # Footer
    print("-" * len(header))
    footer = f"{'TOTAL':<28s}"
    for ch in CHANNELS:
        footer += f"  {grand_totals[ch]:>{col_w}d}"
    footer += f"  {total_api:>{col_w}d}"
    print(footer)
    print("=" * 72)

    # DB-level summary
    if conn:
        print("\n--- DB Status ---")
        for stat in count_posts(conn):
            print(
                f"  {stat['channel']:15s}  "
                f"keyword={stat['keyword']!r:30s}  "
                f"count={stat['cnt']}"
            )
        conn.close()


# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Collect all PoC keywords × channels from Naver."
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB_PATH,
        help=f"SQLite DB path (default: {DEFAULT_DB_PATH})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Collect from API and preprocess but do not write to DB.",
    )
    parser.add_argument(
        "--start-date",
        default=DATE_FROM,
        help=f"Collection start date YYYY-MM-DD (default: {DATE_FROM})",
    )
    parser.add_argument(
        "--end-date",
        default=DATE_TO,
        help=f"Collection end date YYYY-MM-DD (default: {DATE_TO})",
    )
    args = parser.parse_args()
    collect_and_store(
        db_path=args.db,
        dry_run=args.dry_run,
        date_from=args.start_date,
        date_to=args.end_date,
    )


if __name__ == "__main__":
    main()
