"""SQLite persistence layer for collected posts and 7C labels.

Schema follows DATA_GOVERNANCE.md §3.2.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

DEFAULT_DB_PATH = Path("data/processed/naver_posts.db")

# ------------------------------------------------------------------
# DDL
# ------------------------------------------------------------------

_SCHEMA_SQL = """\
CREATE TABLE IF NOT EXISTS posts (
    post_id      TEXT PRIMARY KEY,
    channel      TEXT NOT NULL,          -- 'news_comment' | 'cafe' | 'blog'
    content      TEXT NOT NULL,
    author_hash  TEXT NOT NULL,          -- SHA-256
    published_at DATE NOT NULL,
    keyword      TEXT,
    collected_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS labels (
    post_id        TEXT REFERENCES posts(post_id),
    label_type     TEXT NOT NULL,         -- 'llm' | 'manual'
    c1_confidence  INTEGER,              -- 0 or 1
    c2_complacency INTEGER,
    c3_constraints INTEGER,
    c4_calculation INTEGER,
    c5_collective  INTEGER,
    c6_compliance  INTEGER,
    c7_conspiracy  INTEGER,
    na_flag        INTEGER DEFAULT 0,
    labeled_at     DATETIME DEFAULT CURRENT_TIMESTAMP,
    labeler_id     TEXT,                 -- 'llm_v1' | 'coder_A' | 'coder_B'
    PRIMARY KEY (post_id, label_type, labeler_id)
);

CREATE INDEX IF NOT EXISTS idx_posts_channel  ON posts(channel);
CREATE INDEX IF NOT EXISTS idx_posts_keyword  ON posts(keyword);
CREATE INDEX IF NOT EXISTS idx_posts_pub_date ON posts(published_at);
CREATE INDEX IF NOT EXISTS idx_labels_type    ON labels(label_type);
"""


def get_connection(db_path: str | Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Open (or create) the SQLite database and return a connection.

    Enables WAL mode and foreign-key checks.
    """
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    """Create tables and indexes if they don't exist."""
    conn.executescript(_SCHEMA_SQL)
    conn.commit()


# ------------------------------------------------------------------
# Posts CRUD
# ------------------------------------------------------------------

def upsert_post(conn: sqlite3.Connection, post: dict) -> bool:
    """Insert a post or silently skip if the post_id already exists.

    Args:
        conn: Active database connection.
        post: Dict with keys matching the ``posts`` table columns:
              ``post_id``, ``channel``, ``content``, ``author_hash``,
              ``published_at``, ``keyword``.

    Returns:
        ``True`` if a new row was inserted, ``False`` if it already existed.
    """
    sql = """\
    INSERT INTO posts (post_id, channel, content, author_hash, published_at, keyword)
    VALUES (:post_id, :channel, :content, :author_hash, :published_at, :keyword)
    ON CONFLICT(post_id) DO NOTHING
    """
    cur = conn.execute(sql, post)
    conn.commit()
    return cur.rowcount > 0


def upsert_posts(conn: sqlite3.Connection, posts: list[dict]) -> int:
    """Batch-insert posts, skipping duplicates.

    Returns:
        Number of newly inserted rows.
    """
    sql = """\
    INSERT INTO posts (post_id, channel, content, author_hash, published_at, keyword)
    VALUES (:post_id, :channel, :content, :author_hash, :published_at, :keyword)
    ON CONFLICT(post_id) DO NOTHING
    """
    cur = conn.executemany(sql, posts)
    conn.commit()
    return cur.rowcount


def get_posts(
    conn: sqlite3.Connection,
    *,
    channel: str | None = None,
    keyword: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    limit: int = 0,
) -> list[dict]:
    """Query posts with optional filters.

    Date arguments use ``YYYY-MM-DD`` format.
    """
    clauses: list[str] = []
    params: list[object] = []

    if channel:
        clauses.append("channel = ?")
        params.append(channel)
    if keyword:
        clauses.append("keyword = ?")
        params.append(keyword)
    if date_from:
        clauses.append("published_at >= ?")
        params.append(date_from)
    if date_to:
        clauses.append("published_at <= ?")
        params.append(date_to)

    where = (" WHERE " + " AND ".join(clauses)) if clauses else ""
    sql = f"SELECT * FROM posts{where} ORDER BY published_at DESC"
    if limit > 0:
        sql += f" LIMIT {limit}"

    return [dict(row) for row in conn.execute(sql, params)]


def count_posts(conn: sqlite3.Connection) -> list[dict]:
    """Return post counts grouped by channel and keyword."""
    sql = """\
    SELECT channel, keyword, COUNT(*) AS cnt
    FROM posts
    GROUP BY channel, keyword
    ORDER BY cnt DESC
    """
    return [dict(row) for row in conn.execute(sql)]


def get_uncollected_keywords(
    conn: sqlite3.Connection,
    target_keywords: list[str],
) -> list[str]:
    """Return keywords from *target_keywords* that have zero posts in the DB."""
    if not target_keywords:
        return []
    placeholders = ",".join("?" for _ in target_keywords)
    sql = f"""\
    SELECT DISTINCT keyword FROM posts WHERE keyword IN ({placeholders})
    """
    collected = {row["keyword"] for row in conn.execute(sql, target_keywords)}
    return [kw for kw in target_keywords if kw not in collected]


# ------------------------------------------------------------------
# Labels CRUD
# ------------------------------------------------------------------

def insert_label(conn: sqlite3.Connection, label: dict) -> bool:
    """Insert a 7C label row. Skips if duplicate (post_id, label_type, labeler_id).

    Args:
        label: Dict with keys: ``post_id``, ``label_type``, ``labeler_id``,
               ``c1_confidence`` … ``c7_conspiracy``, and optionally ``na_flag``.
    """
    sql = """\
    INSERT INTO labels
        (post_id, label_type, c1_confidence, c2_complacency, c3_constraints,
         c4_calculation, c5_collective, c6_compliance, c7_conspiracy,
         na_flag, labeler_id)
    VALUES
        (:post_id, :label_type, :c1_confidence, :c2_complacency, :c3_constraints,
         :c4_calculation, :c5_collective, :c6_compliance, :c7_conspiracy,
         :na_flag, :labeler_id)
    ON CONFLICT(post_id, label_type, labeler_id) DO UPDATE SET
        c1_confidence  = excluded.c1_confidence,
        c2_complacency = excluded.c2_complacency,
        c3_constraints = excluded.c3_constraints,
        c4_calculation = excluded.c4_calculation,
        c5_collective  = excluded.c5_collective,
        c6_compliance  = excluded.c6_compliance,
        c7_conspiracy  = excluded.c7_conspiracy,
        na_flag        = excluded.na_flag,
        labeled_at     = CURRENT_TIMESTAMP
    """
    defaults = {"na_flag": 0}
    row = {**defaults, **label}
    cur = conn.execute(sql, row)
    conn.commit()
    return cur.rowcount > 0


def get_unlabeled_posts(
    conn: sqlite3.Connection,
    label_type: str = "llm",
    limit: int = 0,
) -> list[dict]:
    """Return posts that have no label of the given *label_type*."""
    sql = """\
    SELECT p.* FROM posts p
    LEFT JOIN labels l ON p.post_id = l.post_id AND l.label_type = ?
    WHERE l.post_id IS NULL
    ORDER BY p.published_at
    """
    if limit > 0:
        sql += f" LIMIT {limit}"
    return [dict(row) for row in conn.execute(sql, (label_type,))]


def get_label_stats(conn: sqlite3.Connection) -> dict:
    """Return summary statistics for the labels table."""
    total_posts = conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    labeled = conn.execute(
        "SELECT COUNT(DISTINCT post_id) FROM labels"
    ).fetchone()[0]
    by_type = {
        row["label_type"]: row["cnt"]
        for row in conn.execute(
            "SELECT label_type, COUNT(*) AS cnt FROM labels GROUP BY label_type"
        )
    }
    return {
        "total_posts": total_posts,
        "labeled_posts": labeled,
        "unlabeled_posts": total_posts - labeled,
        "by_label_type": by_type,
    }
