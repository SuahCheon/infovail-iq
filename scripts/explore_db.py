"""
explore_db.py

목적: 통합 DB 탐색
      1. 이벤트 간 담론 교차 분석 (이물질 키워드 <-> 법원 키워드)
      2. 날짜별/채널별 분포
      3. 키워드 그룹별 분포 (이물질 그룹 vs 법원 그룹)
      4. 주차별 요약 (Baseline / Post-event 구분)

실행: python scripts/explore_db.py
"""

import sqlite3
from pathlib import Path

DB_PATH = Path("data/processed/naver_posts.db")

# 키워드 그룹 정의
FOREIGN_MATTER_KEYWORDS = [
    "코로나 백신 이물질", "감사원 백신",
    "코로나 백신 곰팡이", "코로나 백신 피해", "백신 피해 보상",
    "코로나 백신 부작용", "백신 피해자 모임", "코로나 백신 정부 책임",
    "백신 피해자",
]

COURT_KEYWORDS = [
    "코로나 백신 소송", "백신 심근경색 판결", "코로나 백신 항소",
    "질병청 항소", "코백회", "백신 피해 법원", "코로나 백신 사망 판결",
]

# 교차 분석용 텍스트 키워드
FM_TEXT_TERMS   = ["이물질", "곰팡이", "오염", "감사원"]
COURT_TEXT_TERMS = ["소송", "판결", "항소", "심근경색", "코백회", "유족"]

EVENT_DATES = {
    "2026-02-23": "감사원 발표",
    "2026-03-02": "SBS 보도",
    "2026-03-04": "코백회 기자회견",
}


def has_any(text: str, terms: list[str]) -> bool:
    return any(t in text for t in terms)


def main():
    conn = sqlite3.connect(DB_PATH)

    total = conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    print(f"DB 전체: {total}건\n")

    # -- 1. 키워드 그룹별 분포 ------------------------------------------
    print("=" * 60)
    print("1. 키워드 그룹별 분포")
    print("=" * 60)

    fm_ids = set()
    for kw in FOREIGN_MATTER_KEYWORDS:
        for (pid,) in conn.execute(
            "SELECT post_id FROM posts WHERE keyword = ?", (kw,)
        ).fetchall():
            fm_ids.add(pid)

    court_ids = set()
    for kw in COURT_KEYWORDS:
        for (pid,) in conn.execute(
            "SELECT post_id FROM posts WHERE keyword = ?", (kw,)
        ).fetchall():
            court_ids.add(pid)

    overlap_ids = fm_ids & court_ids
    print(f"  이물질 그룹 (수집 키워드 기준): {len(fm_ids)}건")
    print(f"  법원판결 그룹 (수집 키워드 기준): {len(court_ids)}건")
    print(f"  두 그룹 모두 해당 (중복): {len(overlap_ids)}건")

    # -- 2. 담론 교차 분석 -----------------------------------------------
    print("\n" + "=" * 60)
    print("2. 담론 교차 분석 (텍스트 내용 기준)")
    print("=" * 60)

    # 이물질 그룹 게시물 중 법원 용어 포함 비율
    fm_posts = conn.execute(
        "SELECT post_id, content FROM posts WHERE post_id IN ({})".format(
            ",".join("?" * len(fm_ids))
        ), list(fm_ids)
    ).fetchall() if fm_ids else []

    fm_with_court = [(pid, c) for pid, c in fm_posts if has_any(c, COURT_TEXT_TERMS)]
    print(f"\n  [이물질 그룹] 법원 용어 포함:")
    print(f"    {len(fm_with_court)}건 / {len(fm_posts)}건 "
          f"({len(fm_with_court)/max(len(fm_posts),1)*100:.1f}%)")
    if fm_with_court[:3]:
        print("  예시 (최대 3건):")
        for pid, c in fm_with_court[:3]:
            print(f"    [{pid[:8]}] {c[:80]}...")

    # 법원 그룹 게시물 중 이물질 용어 포함 비율
    court_posts = conn.execute(
        "SELECT post_id, content FROM posts WHERE post_id IN ({})".format(
            ",".join("?" * len(court_ids))
        ), list(court_ids)
    ).fetchall() if court_ids else []

    court_with_fm = [(pid, c) for pid, c in court_posts if has_any(c, FM_TEXT_TERMS)]
    print(f"\n  [법원 그룹] 이물질 용어 포함:")
    print(f"    {len(court_with_fm)}건 / {len(court_posts)}건 "
          f"({len(court_with_fm)/max(len(court_posts),1)*100:.1f}%)")
    if court_with_fm[:3]:
        print("  예시 (최대 3건):")
        for pid, c in court_with_fm[:3]:
            print(f"    [{pid[:8]}] {c[:80]}...")

    # -- 3. 날짜별 분포 (이벤트 마커 포함) --------------------------------
    print("\n" + "=" * 60)
    print("3. 날짜별 분포")
    print("=" * 60)
    print(f"  {'날짜':<12} {'전체':>5}  {'이물질그룹':>8}  {'법원그룹':>8}  이벤트")
    print(f"  {'-'*12} {'-'*5}  {'-'*8}  {'-'*8}  {'-'*20}")

    fm_by_date = {}
    for (d, n) in conn.execute("""
        SELECT date(published_at), COUNT(*)
        FROM posts WHERE post_id IN ({})
        GROUP BY date(published_at)
    """.format(",".join("?" * len(fm_ids))), list(fm_ids)).fetchall():
        fm_by_date[d] = n

    court_by_date = {}
    for (d, n) in conn.execute("""
        SELECT date(published_at), COUNT(*)
        FROM posts WHERE post_id IN ({})
        GROUP BY date(published_at)
    """.format(",".join("?" * len(court_ids))), list(court_ids)).fetchall():
        court_by_date[d] = n

    for d, total_n in conn.execute("""
        SELECT date(published_at), COUNT(*)
        FROM posts GROUP BY date(published_at) ORDER BY date(published_at)
    """).fetchall():
        tag = EVENT_DATES.get(d, "")
        fm_n = fm_by_date.get(d, 0)
        ct_n = court_by_date.get(d, 0)
        marker = f"<-- {tag}" if tag else ""
        print(f"  {d:<12} {total_n:>5}  {fm_n:>8}  {ct_n:>8}  {marker}")

    # -- 4. 주차별 요약 ---------------------------------------------------
    print("\n" + "=" * 60)
    print("4. 주차별 요약")
    print("=" * 60)

    weeks = [
        ("Baseline W1",  "2026-02-07", "2026-02-13"),
        ("Baseline W2",  "2026-02-14", "2026-02-22"),
        ("Post-event W1","2026-02-23", "2026-03-01"),
        ("Post-event W2","2026-03-02", "2026-03-08"),
        ("Post-event W3","2026-03-09", "2026-03-15"),
        ("Post-event W4","2026-03-16", "2026-03-21"),
    ]

    print(f"  {'기간':<16} {'전체':>5}  {'이물질':>6}  {'법원':>6}")
    print(f"  {'-'*16} {'-'*5}  {'-'*6}  {'-'*6}")

    for label, start, end in weeks:
        n_total = conn.execute(
            "SELECT COUNT(*) FROM posts WHERE published_at BETWEEN ? AND ?",
            (start, end)
        ).fetchone()[0]

        fm_pids_in_week = [
            pid for pid in fm_ids
            if conn.execute(
                "SELECT 1 FROM posts WHERE post_id=? AND published_at BETWEEN ? AND ?",
                (pid, start, end)
            ).fetchone()
        ]

        court_pids_in_week = [
            pid for pid in court_ids
            if conn.execute(
                "SELECT 1 FROM posts WHERE post_id=? AND published_at BETWEEN ? AND ?",
                (pid, start, end)
            ).fetchone()
        ]

        print(f"  {label:<16} {n_total:>5}  {len(fm_pids_in_week):>6}  {len(court_pids_in_week):>6}")

    conn.close()
    print("\n[OK] 탐색 완료.")


if __name__ == "__main__":
    main()
