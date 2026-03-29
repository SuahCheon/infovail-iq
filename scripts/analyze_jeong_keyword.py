"""
analyze_jeong_keyword.py
------------------------
"정은경 백신" 키워드 수집 게시물 265건 분석
- 다른 키워드와 중복 여부 확인
- FM_Direct / Court / Chronic 3그룹과의 관계
- 시계열 분포 (Baseline / Post-event1 / Post-event2)
Usage:
    python analyze_jeong_keyword.py
    python analyze_jeong_keyword.py --db /path/to/naver_posts.db
"""
import sqlite3
import sys
import io
import argparse
from collections import Counter
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from pipeline.config import DB_PATH

# -- 설정 -------------------------------------------------------------------
DEFAULT_DB = str(DB_PATH)

# 키워드 -> 그룹 매핑
GROUP_MAP = {
    # FM_Direct
    "코로나 백신 이물질": "FM_Direct",
    "코로나 백신 곰팡이": "FM_Direct",
    "감사원 백신":        "FM_Direct",
    "정은경 백신":        "FM_Direct",  # accountability subtype
    # Court
    "코로나 백신 소송":       "Court",
    "백신 심근경색 판결":     "Court",
    "코로나 백신 항소":       "Court",
    "질병청 항소":            "Court",
    "코백회":                 "Court",
    "백신 피해 법원":         "Court",
    "코로나 백신 사망 판결":  "Court",
    # Chronic
    "코로나 백신 피해":         "Chronic",
    "백신 피해 보상":           "Chronic",
    "코로나 백신 부작용":       "Chronic",
    "백신 피해자 모임":         "Chronic",
    "코로나 백신 정부 책임":    "Chronic",
    "백신 피해자":              "Chronic",
    # 분석 대상
    "정은경 백신": "Jeong",
}

# 이벤트 기간 구분
PERIODS = {
    "Baseline":    (date(2026, 2,  7), date(2026, 2, 22)),
    "Post-event1": (date(2026, 2, 23), date(2026, 3,  1)),
    "Post-event2": (date(2026, 3,  2), date(2026, 3, 21)),
}


def get_period(d: date) -> str:
    for name, (start, end) in PERIODS.items():
        if start <= d <= end:
            return name
    return "Outside"


def main(db_path: str):
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    # -- 0. 전체 "정은경 백신" 게시물 목록 ----------------------------------
    cur.execute("""
        SELECT post_id, channel, published_at, keyword
        FROM posts
        WHERE keyword = '정은경 백신'
    """)
    jeong_rows = cur.fetchall()
    jeong_ids = {r["post_id"] for r in jeong_rows}

    print("=" * 60)
    print(f"[0] '정은경 백신' 수집 게시물: {len(jeong_rows)}건")
    print("=" * 60)

    # -- 1. 다른 키워드와 동일 post_id 중복 확인 ----------------------------
    if jeong_ids:
        placeholders = ",".join("?" * len(jeong_ids))
        cur.execute(f"""
            SELECT post_id, keyword
            FROM posts
            WHERE post_id IN ({placeholders})
              AND keyword != '정은경 백신'
        """, list(jeong_ids))
        overlap_rows = cur.fetchall()
    else:
        overlap_rows = []

    overlap_by_id: dict[str, list[str]] = {}
    for r in overlap_rows:
        overlap_by_id.setdefault(r["post_id"], []).append(r["keyword"])

    overlap_count = len(overlap_by_id)
    only_jeong_count = len(jeong_ids) - overlap_count

    print(f"\n[1] 중복 여부 (다른 키워드와 동일 post_id)")
    print(f"    중복 있음 : {overlap_count}건")
    print(f"    정은경 단독: {only_jeong_count}건")

    if overlap_by_id:
        # 겹치는 키워드별 카운트
        overlap_keyword_counter: Counter = Counter()
        for keywords in overlap_by_id.values():
            for kw in keywords:
                overlap_keyword_counter[kw] += 1

        print("\n    겹치는 키워드 분포:")
        for kw, cnt in overlap_keyword_counter.most_common():
            group = GROUP_MAP.get(kw, "Unknown")
            print(f"      [{group:10s}] {kw} : {cnt}건")

    # -- 2. 3그룹 연관성 -- 겹치는 게시물의 그룹 분포 -----------------------
    print(f"\n[2] 3그룹과의 연관성 (중복 post_id 기준)")
    group_overlap: Counter = Counter()
    for keywords in overlap_by_id.values():
        groups = {GROUP_MAP.get(kw, "Unknown") for kw in keywords}
        for g in groups:
            group_overlap[g] += 1

    for group in ["FM_Direct", "Court", "Chronic"]:
        print(f"    {group:12s}: {group_overlap.get(group, 0)}건")

    # -- 3. 시계열 분포 (정은경 전체 게시물 기준) ----------------------------
    print(f"\n[3] 시계열 분포 (정은경 백신 전체 {len(jeong_rows)}건)")
    period_counter: Counter = Counter()
    channel_counter: Counter = Counter()

    for r in jeong_rows:
        try:
            d = date.fromisoformat(r["published_at"])
        except (TypeError, ValueError):
            d = date(2000, 1, 1)
        period_counter[get_period(d)] += 1
        channel_counter[r["channel"]] += 1

    for period in ["Baseline", "Post-event1", "Post-event2", "Outside"]:
        cnt = period_counter.get(period, 0)
        bar = "#" * (cnt // 5) if cnt else ""
        print(f"    {period:12s}: {cnt:4d}건  {bar}")

    print(f"\n[4] 채널 분포")
    for ch, cnt in channel_counter.most_common():
        print(f"    {ch:20s}: {cnt}건")

    # -- 5. 샘플 콘텐츠 (단독 게시물 중 최대 10건) --------------------------
    print(f"\n[5] 콘텐츠 샘플 (정은경 단독 게시물, 최대 10건)")
    solo_ids = list(jeong_ids - set(overlap_by_id.keys()))[:10]

    if solo_ids:
        placeholders = ",".join("?" * len(solo_ids))
        cur.execute(f"""
            SELECT post_id, channel, published_at, content
            FROM posts
            WHERE post_id IN ({placeholders})
              AND keyword = '정은경 백신'
            ORDER BY published_at
        """, solo_ids)
        samples = cur.fetchall()

        for i, r in enumerate(samples, 1):
            content_preview = (r["content"] or "")[:120].replace("\n", " ")
            print(f"\n  [{i}] {r['published_at']} | {r['channel']}")
            print(f"      {content_preview}{'...' if len(r['content'] or '') > 120 else ''}")
    else:
        print("    (단독 게시물 없음 -- 전부 다른 키워드와 중복)")

    con.close()
    print("\n" + "=" * 60)
    print("분석 완료")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default=DEFAULT_DB, help="SQLite DB 경로")
    args = parser.parse_args()
    main(args.db)
