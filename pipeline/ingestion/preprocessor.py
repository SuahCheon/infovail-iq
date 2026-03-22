"""Preprocessing pipeline for raw Naver Search API results.

Transforms raw items from ``NaverClient.collect()`` into DB-ready dicts
conforming to the ``posts`` table schema (see DATA_GOVERNANCE.md §2.1).

Pipeline steps:
  1. HTML tag stripping
  2. Duplicate removal (by ``original_link``)
  3. Nickname → SHA-256 hashing
  4. PII pattern masking (phone, email, Korean resident ID)
"""

from __future__ import annotations

import hashlib
import html
import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# Regex patterns for PII masking
# ------------------------------------------------------------------

# Korean phone numbers: 010-1234-5678, 02-123-4567, 031 1234 5678, etc.
_RE_PHONE = re.compile(
    r"(?<!\d)"                         # not preceded by a digit
    r"(0\d{1,2})"                      # area/mobile prefix
    r"[\s.\-]?"                        # optional separator
    r"(\d{3,4})"                       # middle digits
    r"[\s.\-]?"                        # optional separator
    r"(\d{4})"                         # last 4 digits
    r"(?!\d)"                          # not followed by a digit
)

# Email addresses
_RE_EMAIL = re.compile(
    r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
)

# Korean resident registration number: 6 digits - 7 digits
_RE_KRN_ID = re.compile(
    r"\b(\d{6})\s?[\-]\s?([1-4]\d{6})\b"
)

# HTML tag pattern
_RE_HTML_TAG = re.compile(r"<[^>]+>")


# ------------------------------------------------------------------
# Individual transform functions
# ------------------------------------------------------------------

def strip_html(text: str) -> str:
    """Remove HTML tags and unescape HTML entities."""
    cleaned = _RE_HTML_TAG.sub("", text)
    return html.unescape(cleaned)


def hash_author(nickname: str) -> str:
    """SHA-256 hash a nickname string.

    Returns a fixed placeholder when the nickname is empty so the
    ``NOT NULL`` constraint on ``author_hash`` is always satisfied.
    """
    if not nickname:
        return hashlib.sha256(b"__anonymous__").hexdigest()
    return hashlib.sha256(nickname.encode("utf-8")).hexdigest()


def mask_pii(text: str) -> str:
    """Replace phone numbers, emails, and Korean resident IDs with tokens."""
    text = _RE_KRN_ID.sub("[ID_REDACTED]", text)
    text = _RE_EMAIL.sub("[EMAIL_REDACTED]", text)
    text = _RE_PHONE.sub("[PHONE_REDACTED]", text)
    return text


def deduplicate(items: list[dict], *, key: str = "original_link") -> list[dict]:
    """Remove duplicate items based on *key*, preserving first occurrence."""
    seen: set[str] = set()
    unique: list[dict] = []
    for item in items:
        val = item.get(key, "")
        if val and val in seen:
            continue
        seen.add(val)
        unique.append(item)
    dropped = len(items) - len(unique)
    if dropped:
        logger.info("Deduplicated: dropped %d duplicate items", dropped)
    return unique


# ------------------------------------------------------------------
# Post-ID generation
# ------------------------------------------------------------------

def _make_post_id(channel: str, content: str, pub_date: datetime | None) -> str:
    """Derive a deterministic post_id from content + metadata.

    Using content hash ensures the same post collected twice gets the
    same ID, which lets the DB ``ON CONFLICT`` clause handle duplicates.
    """
    date_str = pub_date.strftime("%Y%m%d") if pub_date else "nodate"
    payload = f"{channel}|{date_str}|{content}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


# ------------------------------------------------------------------
# Main pipeline
# ------------------------------------------------------------------

def preprocess(raw_items: list[dict]) -> list[dict]:
    """Run the full preprocessing pipeline on raw API results.

    Accepts the list of dicts returned by ``NaverClient.collect()`` and
    returns a list of dicts ready for ``db.upsert_posts()``.

    Pipeline order:
      1. Deduplicate by ``original_link``
      2. Strip HTML from ``title`` and ``description``
      3. Mask PII in combined content
      4. Hash author nickname
      5. Build DB-ready dict (URLs are **not** stored — see DATA_GOVERNANCE §1.3)
    """
    items = deduplicate(raw_items)
    results: list[dict] = []

    for item in items:
        title = strip_html(item.get("title", ""))
        description = strip_html(item.get("description", ""))
        content = f"{title}\n{description}".strip()
        content = mask_pii(content)

        channel = item.get("channel", "")
        nickname = item.get("blogger_name") or item.get("cafe_name") or ""
        author_h = hash_author(nickname)

        pub_date: datetime | None = item.get("pub_date")
        if pub_date is None:
            # DB requires NOT NULL; skip items without a parseable date
            continue
        published_at = pub_date.strftime("%Y-%m-%d")

        post_id = _make_post_id(channel, content, pub_date)

        results.append(
            {
                "post_id": post_id,
                "channel": channel,
                "content": content,
                "author_hash": author_h,
                "published_at": published_at,
                "keyword": item.get("keyword", ""),
            }
        )

    logger.info(
        "Preprocessed %d → %d items (dedup + transform)",
        len(raw_items),
        len(results),
    )
    return results
