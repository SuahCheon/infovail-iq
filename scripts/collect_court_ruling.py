"""
collect_court_ruling.py
─────────────────────────────────────────────────────────────────
목적: 2026.03.02 SBS 단독 보도 (코로나 백신 심근경색 사망 판결 + 질병청 항소)
      관련 게시물 수집 및 기존 DB 현황 확인

실행: python scripts/collect_court_ruling.py
─────────────────────────────────────────────────────────────────
"""

import sqlite3
import os
import time
import hashlib
import httpx
from datetime import datetime, date
from dotenv import load_dotenv

load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))  # 루트 .env fallback

DB_PATH = "data/processed/naver_posts.db"
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")


def ensure_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            post_id      TEXT PRIMARY KEY,
            channel      TEXT,
            content      TEXT,
            author_hash  TEXT,
            published_at TEXT,
            keyword      TEXT,
            collected_at TEXT
        )
    """)
    conn.commit()


# ── 1단계: 기존 DB 현황 확인 ─────────────────────────────────────

def check_existing(conn):
    print("=" * 60)
    print("■ STEP 1: 기존 DB에서 법원판결 관련 게시물 현황")
    print("=" * 60)

    keywords = [
        "소송", "판결", "항소", "심근경색",
        "코백회", "행정소송", "승소", "유족",
        "사망 인과", "법원"
    ]

    total_related = set()
    for kw in keywords:
        rows = conn.execute(
            "SELECT post_id FROM posts WHERE content LIKE ?",
            (f"%{kw}%",)
        ).fetchall()
        ids = {r[0] for r in rows}
        total_related |= ids
        print(f"  '{kw}': {len(ids)}건")

    total_all = conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    print(f"\n  → 중복 제거 합계: {len(total_related)}건 / 전체 {total_all}건")

    print("\n■ 날짜별 분포 (소송|판결|항소|심근경색 포함 게시물)")
    rows = conn.execute("""
        SELECT date(published_at) as d, channel, COUNT(*) as n
        FROM posts
        WHERE content LIKE '%소송%'
           OR content LIKE '%판결%'
           OR content LIKE '%항소%'
           OR content LIKE '%심근경색%'
        GROUP BY d, channel
        ORDER BY d
    """).fetchall()

    if rows:
        print(f"  {'날짜':<12} {'채널':<15} {'건수':>5}")
        print(f"  {'-'*12} {'-'*15} {'-'*5}")
        for d, ch, n in rows:
            marker = " ← SBS 보도" if d and d >= "2026-03-02" else ""
            print(f"  {d:<12} {ch:<15} {n:>5}{marker}")
    else:
        print("  → 관련 게시물 없음 (추가 수집 필요)")

    print()
    return len(total_related)


# ── 2단계: 추가 수집 ─────────────────────────────────────────────

COURT_KEYWORDS = [
    "코로나 백신 소송",
    "백신 심근경색 판결",
    "코로나 백신 항소",
    "질병청 항소",
    "코백회",
    "백신 피해 법원",
    "코로나 백신 사망 판결",
]

COLLECT_START = "2026-01-01"
COLLECT_END   = "2026-03-21"

CHANNELS = ["blog", "news"]  # cafearticle 제외


def hash_author(nickname: str) -> str:
    return hashlib.sha256(nickname.encode("utf-8")).hexdigest()


def fetch_naver(keyword: str, channel: str, start: str, end: str,
                display: int = 100) -> list[dict]:
    url = f"https://openapi.naver.com/v1/search/{channel}.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
    }

    results = []
    start_idx = 1

    while True:
        params = {
            "query": keyword,
            "display": display,
            "start": start_idx,
            "sort": "date",
        }

        try:
            resp = httpx.get(url, headers=headers, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"    API 오류: {e}")
            break

        items = data.get("items", [])
        if not items:
            break

        for item in items:
            pub_date_str = item.get("pubDate", "") or item.get("postdate", "")
            if not pub_date_str:
                continue

            try:
                if len(pub_date_str) == 8:  # YYYYMMDD (blog)
                    pub_date = date(int(pub_date_str[:4]),
                                    int(pub_date_str[4:6]),
                                    int(pub_date_str[6:8]))
                else:  # RFC 2822 (news)
                    from email.utils import parsedate
                    t = parsedate(pub_date_str)
                    pub_date = date(t[0], t[1], t[2])
            except Exception:
                continue

            if not (date.fromisoformat(start) <= pub_date <= date.fromisoformat(end)):
                if pub_date < date.fromisoformat(start):
                    return results
                continue

            import re
            def strip_html(text):
                return re.sub(r"<[^>]+>", "", text or "").strip()

            content = strip_html(item.get("description", ""))
            title   = strip_html(item.get("title", ""))
            full_text = f"{title} {content}".strip()

            if not full_text:
                continue

            author_raw = item.get("bloggername", "") or item.get("author", "") or "unknown"

            results.append({
                "channel": channel,
                "content": full_text,
                "author_hash": hash_author(author_raw),
                "published_at": pub_date.isoformat(),
                "keyword": keyword,
            })

        start_idx += display
        total = data.get("total", 0)
        if start_idx > min(total, 1000):
            break

        time.sleep(0.5)

    return results


def insert_posts(conn, posts: list[dict]) -> int:
    inserted = 0
    for p in posts:
        post_id = hashlib.sha256(
            f"{p['channel']}{p['content']}{p['published_at']}".encode()
        ).hexdigest()[:16]

        try:
            conn.execute("""
                INSERT INTO posts (post_id, channel, content, author_hash,
                                   published_at, keyword, collected_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                post_id, p["channel"], p["content"], p["author_hash"],
                p["published_at"], p["keyword"],
                datetime.now().isoformat()
            ))
            inserted += 1
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    return inserted


def collect_court_keywords(conn):
    print("=" * 60)
    print("■ STEP 2: 법원판결·항소 관련 키워드 추가 수집")
    print(f"  기간: {COLLECT_START} ~ {COLLECT_END}")
    print("=" * 60)

    total_new = 0
    for keyword in COURT_KEYWORDS:
        kw_new = 0
        for channel in CHANNELS:
            print(f"  수집 중: '{keyword}' × {channel} ...", end=" ", flush=True)
            posts = fetch_naver(keyword, channel, COLLECT_START, COLLECT_END)
            n = insert_posts(conn, posts)
            kw_new += n
            print(f"{len(posts)}건 수집 → {n}건 신규 삽입")
            time.sleep(0.3)
        total_new += kw_new

    print(f"\n  → 총 신규 삽입: {total_new}건")
    return total_new


# ── 3단계: 수집 후 현황 재확인 ───────────────────────────────────

def summary_after(conn):
    print("\n" + "=" * 60)
    print("■ STEP 3: 수집 후 날짜별 분포 (전체 게시물)")
    print("=" * 60)

    rows = conn.execute("""
        SELECT date(published_at) as d, channel, COUNT(*) as n
        FROM posts
        GROUP BY d, channel
        ORDER BY d
    """).fetchall()

    print(f"  {'날짜':<12} {'채널':<15} {'건수':>5}")
    print(f"  {'-'*12} {'-'*15} {'-'*5}")
    for d, ch, n in rows:
        markers = []
        if d and d >= "2026-02-23": markers.append("감사원")
        if d and d >= "2026-03-02": markers.append("SBS보도")
        if d and d >= "2026-03-04": markers.append("코백회")
        tag = " ← " + "+".join(markers) if markers else ""
        print(f"  {d:<12} {ch:<15} {n:>5}{tag}")

    total = conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    print(f"\n  → DB 전체: {total}건")


# ── main ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    if not NAVER_CLIENT_ID or not NAVER_CLIENT_SECRET:
        print("[ERROR] .env에 NAVER_CLIENT_ID / NAVER_CLIENT_SECRET 없음")
        exit(1)

    conn = sqlite3.connect(DB_PATH)
    ensure_table(conn)

    existing_count = check_existing(conn)

    if existing_count < 50:
        print("→ 관련 게시물이 적으므로 추가 수집을 진행합니다.\n")
        new_count = collect_court_keywords(conn)
    else:
        ans = input(f"→ 기존에 {existing_count}건 있음. 그래도 추가 수집할까요? [y/N] ").strip().lower()
        if ans == "y":
            new_count = collect_court_keywords(conn)
        else:
            print("추가 수집 생략.")
            new_count = 0

    summary_after(conn)
    conn.close()

    print("\n[OK] 완료.")
    if new_count > 0:
        print(f"   신규 수집: {new_count}건 — DB에 반영됨.")
    print("   결과를 Claude에 붙여넣어 주시면 분석 진행합니다.")
