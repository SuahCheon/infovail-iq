"""
regroup_analysis.py

목적: 키워드 3그룹 재정의 후 날짜별 분포 재확인
      - 이물질 직접 그룹 (감사원 이벤트)
      - 법원판결 그룹 (SBS 이벤트)
      - 만성 기저불신 그룹 (Baseline 담론)
      - "백신 오염" 제외
"""

import sqlite3
import sys
import io
from pathlib import Path
from datetime import date, timedelta

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DB_PATH = Path("data/processed/naver_posts.db")

# -- 키워드 그룹 재정의 ------------------------------------------------
GROUPS = {
    "FM_Direct": [          # 이물질 직접 (감사원 이벤트) + 책임론
        "코로나 백신 이물질",
        "코로나 백신 곰팡이",
        "감사원 백신",
        "정은경 백신",          # accountability subtype
    ],
    "Court": [              # 법원판결 (SBS 이벤트)
        "코로나 백신 소송",
        "백신 심근경색 판결",
        "코로나 백신 항소",
        "질병청 항소",
        "코백회",
        "백신 피해 법원",
        "코로나 백신 사망 판결",
    ],
    "Chronic": [            # 만성 기저불신
        "코로나 백신 피해",
        "백신 피해 보상",
        "코로나 백신 부작용",
        "백신 피해자 모임",
        "코로나 백신 정부 책임",
        "백신 피해자",
    ],
    # "백신 오염" -> 제외
}

EVENTS = {
    "2026-02-23": "Audit(감사원)",
    "2026-03-02": "SBS보도",
    "2026-03-04": "코백회",
}

START = date(2026, 2, 7)
END   = date(2026, 3, 21)


def get_ids_by_group(conn, keywords):
    ph = ",".join("?" * len(keywords))
    rows = conn.execute(
        f"SELECT post_id FROM posts WHERE keyword IN ({ph})", keywords
    ).fetchall()
    return {r[0] for r in rows}


def get_daily(conn, post_ids):
    if not post_ids:
        return {}
    ph = ",".join("?" * len(post_ids))
    rows = conn.execute(
        f"SELECT date(published_at), COUNT(*) FROM posts "
        f"WHERE post_id IN ({ph}) GROUP BY date(published_at)",
        list(post_ids)
    ).fetchall()
    return {r[0]: r[1] for r in rows}


def date_range(start, end):
    d = start
    while d <= end:
        yield d.isoformat()
        d += timedelta(days=1)


def main():
    conn = sqlite3.connect(DB_PATH)

    # -- 그룹별 ID 수집 -------------------------------------------------
    group_ids = {name: get_ids_by_group(conn, kws)
                 for name, kws in GROUPS.items()}

    # 중복 확인
    print("=" * 65)
    print("1. 그룹별 건수 및 중복")
    print("=" * 65)
    for name, ids in group_ids.items():
        print(f"  {name:<12}: {len(ids):>5}건")

    fm_court  = group_ids["FM_Direct"] & group_ids["Court"]
    fm_chr    = group_ids["FM_Direct"] & group_ids["Chronic"]
    court_chr = group_ids["Court"]     & group_ids["Chronic"]
    print(f"\n  FM_Direct x Court:   {len(fm_court)}건")
    print(f"  FM_Direct x Chronic: {len(fm_chr)}건")
    print(f"  Court x Chronic:     {len(court_chr)}건")

    # -- 날짜별 분포 ----------------------------------------------------
    print("\n" + "=" * 65)
    print("2. 날짜별 분포 (3그룹)")
    print("=" * 65)

    daily = {name: get_daily(conn, ids) for name, ids in group_ids.items()}

    print(f"  {'날짜':<12} {'FM직접':>6}  {'법원':>6}  {'만성':>6}  이벤트")
    print(f"  {'-'*12} {'-'*6}  {'-'*6}  {'-'*6}  {'-'*20}")

    for d in date_range(START, END):
        fm  = daily["FM_Direct"].get(d, 0)
        ct  = daily["Court"].get(d, 0)
        ch  = daily["Chronic"].get(d, 0)
        tag = EVENTS.get(d, "")
        marker = f"<-- {tag}" if tag else ""
        if fm + ct + ch > 0:
            print(f"  {d:<12} {fm:>6}  {ct:>6}  {ch:>6}  {marker}")

    # -- 주차별 요약 ----------------------------------------------------
    print("\n" + "=" * 65)
    print("3. 주차별 요약")
    print("=" * 65)

    weeks = [
        ("Baseline W1",   "2026-02-07", "2026-02-13"),
        ("Baseline W2",   "2026-02-14", "2026-02-22"),
        ("Post-event W1", "2026-02-23", "2026-03-01"),
        ("Post-event W2", "2026-03-02", "2026-03-08"),
        ("Post-event W3", "2026-03-09", "2026-03-15"),
        ("Post-event W4", "2026-03-16", "2026-03-21"),
    ]

    print(f"  {'기간':<16} {'FM직접':>6}  {'법원':>6}  {'만성':>6}  합계")
    print(f"  {'-'*16} {'-'*6}  {'-'*6}  {'-'*6}  {'-'*5}")

    for label, ws, we in weeks:
        counts = {}
        for name, ids in group_ids.items():
            n = conn.execute(
                "SELECT COUNT(*) FROM posts WHERE post_id IN ({}) "
                "AND published_at BETWEEN ? AND ?".format(
                    ",".join("?" * len(ids))
                ),
                list(ids) + [ws, we]
            ).fetchone()[0] if ids else 0
            counts[name] = n
        total = sum(counts.values())
        print(f"  {label:<16} {counts['FM_Direct']:>6}  "
              f"{counts['Court']:>6}  {counts['Chronic']:>6}  {total:>5}")

    conn.close()
    print("\n[OK] 완료.")


if __name__ == "__main__":
    main()
