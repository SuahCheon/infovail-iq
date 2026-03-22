"""
monitor_events.py
-----------------
백신 관련 이벤트 자동 모니터링
- Naver News API로 매일 관련 뉴스 수집
- 이벤트 후보를 SQLite DB에 저장
- EVENT_LOG.md 자동 렌더링

Usage:
    python monitor_events.py
    python monitor_events.py --date 2026-03-10  # 특정 날짜 수집
    python monitor_events.py --render-only       # DB → MD 렌더링만

실행 주기: Windows 작업 스케줄러로 매일 07:00 자동 실행
"""

import sqlite3
import httpx
import os
import argparse
from datetime import date, datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── 설정 ──────────────────────────────────────────────────────────────────────

BASE_DIR    = Path(r"C:\infovail-iq")
DB_PATH     = BASE_DIR / "data" / "processed" / "event_log.db"
MD_PATH     = BASE_DIR / "docs" / "EVENT_LOG.md"
NAVER_URL   = "https://openapi.naver.com/v1/search/news.json"

NAVER_CLIENT_ID     = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

# 모니터링 키워드 (카테고리별)
MONITOR_KEYWORDS = {
    "정치·국회": [
        "백신 국정감사",
        "코로나 백신 국감",
        "백신 청문회",
        "코로나 백신 국회",
    ],
    "사법": [
        "코로나 백신 판결",
        "백신 소송 항소",
        "백신 피해 대법원",
    ],
    "행정·감사": [
        "정은경 청문회",
        "KDCA 백신 감사",
        "질병청 백신 감사",
        "감사원 백신",
    ],
    "피해자단체": [
        "코백회",
        "백신 피해자 집회",
        "백신 피해자 기자회견",
    ],
    "보상·입법": [
        "백신 피해 특별법",
        "백신 피해 보상 기준",
        "코로나 백신 보상 개정",
    ],
}

# 이벤트 중요도 자동 판단 키워드 (제목에 포함 시 high)
HIGH_IMPORTANCE_SIGNALS = [
    "국정감사", "청문회", "판결", "항소", "대법원",
    "경질", "사퇴", "고발", "기소", "특별법",
    "기자회견", "집회", "시위",
    # 이물질 이슈 관련 신호어
    "감사원", "이물", "이물질", "식약처", "질병청",
    "곰팡이", "패싱", "미통보", "은폐", "보도",
]


# ── DB 초기화 ──────────────────────────────────────────────────────────────────

def init_db(db_path: Path):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS events (
            event_id      INTEGER PRIMARY KEY AUTOINCREMENT,
            event_date    DATE NOT NULL,
            category      TEXT NOT NULL,
            keyword       TEXT NOT NULL,
            title         TEXT NOT NULL,
            description   TEXT,
            source        TEXT,
            link          TEXT UNIQUE,
            importance    TEXT DEFAULT 'normal',  -- high / normal
            confirmed     INTEGER DEFAULT 0,       -- 1 = 연구자 확정
            keyword_added TEXT,                    -- 추가된 수집 키워드
            collected_at  DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE INDEX IF NOT EXISTS idx_event_date ON events(event_date);
        CREATE INDEX IF NOT EXISTS idx_confirmed ON events(confirmed);
    """)
    con.commit()
    con.close()


# ── Naver News 수집 ────────────────────────────────────────────────────────────

def fetch_news(keyword: str, target_date: date) -> list[dict]:
    """Naver News API로 키워드 뉴스 수집 (target_date ±1일 범위, pub_date는 실제 발행일 유지)"""
    if not NAVER_CLIENT_ID or not NAVER_CLIENT_SECRET:
        raise ValueError("NAVER_CLIENT_ID / NAVER_CLIENT_SECRET 환경변수 미설정")

    headers = {
        "X-Naver-Client-Id":     NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
    }
    params = {
        "query":  keyword,
        "display": 20,
        "sort":   "date",
    }

    # ±1일 허용 범위
    date_min = target_date - timedelta(days=1)
    date_max = target_date + timedelta(days=1)

    results = []
    try:
        resp = httpx.get(NAVER_URL, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        items = resp.json().get("items", [])

        for item in items:
            # pubDate 파싱 (예: "Mon, 10 Mar 2026 07:00:00 +0900")
            try:
                pub_dt = datetime.strptime(
                    item["pubDate"], "%a, %d %b %Y %H:%M:%S %z"
                )
                pub_date = pub_dt.date()
            except (ValueError, KeyError):
                pub_date = target_date

            # target_date ±1일 범위 필터 (API가 과거 날짜를 부정확하게 주는 경우 대응)
            if not (date_min <= pub_date <= date_max):
                continue

            # HTML 태그 제거
            title = item.get("title", "").replace("<b>", "").replace("</b>", "")
            desc  = item.get("description", "").replace("<b>", "").replace("</b>", "")

            results.append({
                "title":       title,
                "description": desc,
                "source":      item.get("originallink", ""),
                "link":        item.get("link", ""),
                "pub_date":    pub_date,  # 실제 발행일 유지
            })
    except httpx.HTTPError as e:
        print(f"  [경고] '{keyword}' 수집 실패: {e}")

    return results


def judge_importance(title: str) -> str:
    for signal in HIGH_IMPORTANCE_SIGNALS:
        if signal in title:
            return "high"
    return "normal"


# ── DB 저장 ────────────────────────────────────────────────────────────────────

def save_events(db_path: Path, category: str, keyword: str, items: list[dict]) -> int:
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    saved = 0

    for item in items:
        importance = judge_importance(item["title"])
        try:
            cur.execute("""
                INSERT OR IGNORE INTO events
                    (event_date, category, keyword, title, description,
                     source, link, importance)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item["pub_date"].isoformat(),
                category,
                keyword,
                item["title"],
                item["description"],
                item["source"],
                item["link"],
                importance,
            ))
            if cur.rowcount > 0:
                saved += 1
        except sqlite3.Error as e:
            print(f"  [DB 오류] {e}")

    con.commit()
    con.close()
    return saved


# ── MD 렌더링 ──────────────────────────────────────────────────────────────────

def render_markdown(db_path: Path, md_path: Path):
    md_path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # 날짜별 이벤트 조회
    cur.execute("""
        SELECT event_date, category, keyword, title, link, importance, confirmed, keyword_added
        FROM events
        ORDER BY event_date DESC, importance DESC, collected_at DESC
    """)
    rows = cur.fetchall()
    con.close()

    if not rows:
        return

    # 날짜별 그룹핑
    from collections import defaultdict
    by_date: dict = defaultdict(list)
    for row in rows:
        by_date[row[0]].append(row)

    lines = [
        "# Infovail-IQ — 이벤트 로그 (자동 생성)",
        "",
        f"> 마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "> 🔴 = high importance | ⬜ = normal | ✅ = 연구자 확정 | 🔑 = 키워드 추가됨",
        "",
        "---",
        "",
    ]

    for event_date in sorted(by_date.keys(), reverse=True):
        lines.append(f"## {event_date}")
        lines.append("")

        for _, category, keyword, title, link, importance, confirmed, kw_added in by_date[event_date]:
            icon = "🔴" if importance == "high" else "⬜"
            confirmed_mark = " ✅" if confirmed else ""
            kw_mark = f" 🔑`{kw_added}`" if kw_added else ""
            lines.append(
                f"- {icon} **[{category}]** [{title}]({link}){confirmed_mark}{kw_mark}"
            )
            lines.append(f"  *키워드: {keyword}*")
            lines.append("")

        lines.append("---")
        lines.append("")

    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[MD] {md_path} 렌더링 완료 ({len(rows)}건)")


# ── 메인 ──────────────────────────────────────────────────────────────────────

def main(target_date: date, render_only: bool):
    init_db(DB_PATH)

    if render_only:
        render_markdown(DB_PATH, MD_PATH)
        return

    print(f"[모니터링] {target_date} 뉴스 수집 시작")
    print("=" * 60)

    total_new = 0
    total_high = 0

    for category, keywords in MONITOR_KEYWORDS.items():
        for keyword in keywords:
            items = fetch_news(keyword, target_date)
            if items:
                saved = save_events(DB_PATH, category, keyword, items)
                high = sum(1 for i in items if judge_importance(i["title"]) == "high")
                if saved > 0:
                    print(f"  [{category}] '{keyword}': +{saved}건 저장"
                          + (f" (🔴 {high}건 high)" if high else ""))
                total_new += saved
                total_high += high

    print("=" * 60)
    print(f"[완료] 신규 저장: {total_new}건 (high importance: {total_high}건)")

    # MD 렌더링
    render_markdown(DB_PATH, MD_PATH)

    # high importance 항목 요약 출력
    if total_high > 0:
        print()
        print("🔴 [주의] High importance 이벤트 발생 — EVENT_LOG.md 확인 필요")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--date",
        default=str(date.today() - timedelta(days=1)),
        help="수집 대상 날짜 (YYYY-MM-DD, 기본값: 어제)"
    )
    parser.add_argument(
        "--render-only",
        action="store_true",
        help="수집 없이 MD 렌더링만"
    )
    args = parser.parse_args()

    target = date.fromisoformat(args.date)
    main(target, args.render_only)
