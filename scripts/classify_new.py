"""
classify_new.py
---------------
Classify only unclassified posts (not present in existing labeled JSONL).

Reuses the same prompt, model, and Batch API logic from llm_runner.py v6
(prompt v1.1.0, claude-haiku-4-5-20251001).

Usage:
    # Submit batch job for all unclassified posts
    python scripts/classify_new.py

    # Dry-run: show counts without submitting
    python scripts/classify_new.py --dry-run

    # Custom labeled file to diff against
    python scripts/classify_new.py --existing path/to/file.jsonl
"""

import json
import sqlite3
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
load_dotenv(override=True)

import anthropic
from pipeline.llm_runner import (
    SYSTEM_PROMPT,
    MODEL,
    MAX_TOKENS,
    build_few_shot_messages,
    submit_batch,
    poll_batch,
    parse_batch_results,
    build_batch_request,
)

BASE_DIR   = Path(r"C:\infovail-iq")
NAVER_DB   = BASE_DIR / "data" / "processed" / "naver_posts.db"
OUTPUT_DIR = BASE_DIR / "data" / "exports" / "labeled"
DEFAULT_EXISTING = OUTPUT_DIR / "naver_all_20260311_040325_batch_recovered.jsonl"


def load_classified_ids(labeled_path: Path) -> set[str]:
    ids = set()
    with open(labeled_path, encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            ids.add(row["post_id"])
    return ids


def load_unclassified_posts(db_path: Path, classified_ids: set[str]) -> list[tuple]:
    conn = sqlite3.connect(db_path)
    cur = conn.execute("SELECT post_id, content, keyword_group FROM posts")
    rows = [
        (pid, content, kg)
        for pid, content, kg in cur.fetchall()
        if pid not in classified_ids
    ]
    conn.close()
    return rows


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Classify unclassified posts via Batch API"
    )
    parser.add_argument(
        "--existing", type=Path, default=DEFAULT_EXISTING,
        help=f"Existing labeled JSONL to diff against (default: {DEFAULT_EXISTING.name})",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show counts only, do not submit batch",
    )
    args = parser.parse_args()

    classified_ids = load_classified_ids(args.existing)
    print(f"Already classified: {len(classified_ids)} posts")

    rows = load_unclassified_posts(NAVER_DB, classified_ids)
    print(f"To classify: {len(rows)} posts")

    if not rows:
        print("Nothing to classify.")
        return

    # Breakdown by keyword_group
    from collections import Counter
    group_counts = Counter(kg for _, _, kg in rows)
    for g, c in group_counts.most_common():
        print(f"  {g}: {c}")

    if args.dry_run:
        print("[Dry run] No batch submitted.")
        return

    # Build batch requests
    requests = [
        build_batch_request(pid, content or "", "ko")
        for pid, content, _ in rows
    ]

    client = anthropic.Anthropic()
    batch_id = submit_batch(client, requests)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save batch ID
    id_path = OUTPUT_DIR / f"naver_new_{ts}_batch_id.txt"
    id_path.write_text(batch_id)
    print(f"Batch ID saved: {id_path}")

    # Poll and collect results
    parsed = parse_batch_results(poll_batch(client, batch_id))
    group_map = {pid: kg for pid, _, kg in rows}
    out_path = OUTPUT_DIR / f"naver_new_{ts}_batch.jsonl"

    with open(out_path, "w", encoding="utf-8") as f:
        for p in parsed:
            pid = p.pop("_custom_id")
            f.write(json.dumps({
                "post_id":       pid,
                "keyword_group": group_map.get(pid),
                "pred_C1":       p.get("C1", -1),
                "pred_C2":       p.get("C2", -1),
                "pred_C4":       p.get("C4", -1),
                "pred_C6":       p.get("C6", -1),
                "pred_C7":       p.get("C7", -1),
                "rationale":     p.get("rationale"),
                "parse_error":   p.get("parse_error"),
                "batch_error":   p.get("batch_error"),
            }, ensure_ascii=False) + "\n")

    print(f"[완료] {out_path} ({len(parsed)} posts)")


if __name__ == "__main__":
    main()
