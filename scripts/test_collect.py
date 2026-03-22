"""Test collection: 1차 키워드 '코로나 백신 이물질', news 채널.

Usage:
    uv run python scripts/test_collect.py
"""

from __future__ import annotations

import hashlib
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pipeline.ingestion.db import get_connection, init_db, upsert_posts, count_posts
from pipeline.ingestion.naver_client import NaverClient

# ------------------------------------------------------------------
# Settings
# ------------------------------------------------------------------
KEYWORD = "코로나 백신 이물질"
CHANNEL = "news"
DATE_FROM = "2026-02-07"
DATE_TO = "2026-03-04"

# Naver API channel name → DB channel name
_CHANNEL_MAP = {"news": "news_comment", "blog": "blog", "cafearticle": "cafe"}

_HTML_RE = re.compile(r"<[^>]+>")


def _strip_html(text: str) -> str:
    return _HTML_RE.sub("", text).strip()


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _to_db_row(item: dict) -> dict:
    """Convert a NaverClient result dict to a DB-ready posts row."""
    # post_id: deterministic hash of link (unique per post)
    post_id = _hash(item["link"])

    # author: blogger_name or cafe_name (whichever is populated)
    raw_author = item.get("blogger_name") or item.get("cafe_name") or "anonymous"
    author_hash = _hash(raw_author)

    # content: title + description (API returns snippets only)
    title = _strip_html(item.get("title", ""))
    desc = _strip_html(item.get("description", ""))
    content = f"{title}\n{desc}".strip()

    # published_at
    pub = item.get("pub_date")
    if isinstance(pub, datetime):
        published_at = pub.strftime("%Y-%m-%d")
    else:
        published_at = DATE_FROM  # fallback

    return {
        "post_id": post_id,
        "channel": _CHANNEL_MAP.get(item["channel"], item["channel"]),
        "content": content,
        "author_hash": author_hash,
        "published_at": published_at,
        "keyword": item.get("keyword", KEYWORD),
    }


def main() -> None:
    # 1. Collect from Naver API
    print(f"Collecting: keyword={KEYWORD!r}  channel={CHANNEL}  {DATE_FROM}~{DATE_TO}")
    with NaverClient() as client:
        results = client.collect(
            keyword=KEYWORD,
            channel=CHANNEL,
            date_from=DATE_FROM,
            date_to=DATE_TO,
        )
    print(f"API returned: {len(results)} items")

    if not results:
        print("No results. Check API credentials or keyword.")
        return

    # 2. Transform → DB rows
    rows = [_to_db_row(item) for item in results]

    # 3. Save to DB
    conn = get_connection()
    init_db(conn)
    inserted = upsert_posts(conn, rows)
    print(f"DB inserted: {inserted} new rows (skipped {len(rows) - inserted} duplicates)")

    # 4. Summary
    print("\n--- DB Summary ---")
    for stat in count_posts(conn):
        print(f"  {stat['channel']:15s}  keyword={stat['keyword']!r:30s}  count={stat['cnt']}")

    conn.close()


if __name__ == "__main__":
    main()
