"""
inspect_baseline.py

목적: 2026-02-07 ~ 2026-02-22 (감사원 발표 전) 기간
      이물질 그룹 게시물의 성격 파악
      1. 키워드별 날짜 분포
      2. 키워드별 샘플 3건씩 본문 출력
      3. "이물질" 텍스트 직접 포함 vs 일반 부작용 담론 구분
"""

import sqlite3
import sys
import io
from pathlib import Path

# Windows cp949 stdout 문제 방지
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DB_PATH = Path("data/processed/naver_posts.db")

BASELINE_START = "2026-02-07"
BASELINE_END   = "2026-02-22"

FOREIGN_MATTER_KEYWORDS = [
    "코로나 백신 이물질",
    "감사원 백신",
    "코로나 백신 곰팡이",
    "코로나 백신 피해",
    "백신 피해 보상",
    "코로나 백신 부작용",
    "백신 피해자 모임",
    "코로나 백신 정부 책임",
    "백신 피해자",
]

# 이물질 직접 언급 여부 판단용
DIRECT_FM_TERMS = ["이물질", "곰팡이", "오염", "이물", "파편"]


def main():
    conn = sqlite3.connect(DB_PATH)

    # -- 1. 키워드별 날짜 분포 ------------------------------------------
    print("=" * 65)
    print("1. 키워드별 건수 (Baseline 2/7~2/22)")
    print("=" * 65)
    print(f"  {'키워드':<22} {'전체':>5}  날짜별 분포")
    print(f"  {'-'*22} {'-'*5}  {'-'*30}")

    baseline_ids = []

    for kw in FOREIGN_MATTER_KEYWORDS:
        rows = conn.execute("""
            SELECT post_id, date(published_at) as d
            FROM posts
            WHERE keyword = ?
              AND published_at BETWEEN ? AND ?
            ORDER BY d
        """, (kw, BASELINE_START, BASELINE_END)).fetchall()

        if not rows:
            print(f"  {kw:<22} {0:>5}")
            continue

        baseline_ids.extend([r[0] for r in rows])

        # 날짜별 카운트
        date_counts = {}
        for _, d in rows:
            date_counts[d] = date_counts.get(d, 0) + 1
        dist = "  ".join(f"{d[5:]}({n})" for d, n in sorted(date_counts.items()))
        print(f"  {kw:<22} {len(rows):>5}  {dist}")

    total_baseline = len(set(baseline_ids))
    print(f"\n  중복 제거 합계: {total_baseline}건")

    # -- 2. 이물질 직접 언급 vs 일반 담론 구분 --------------------------
    print("\n" + "=" * 65)
    print("2. '이물질' 직접 언급 여부 (텍스트 기준)")
    print("=" * 65)

    all_baseline = conn.execute("""
        SELECT post_id, keyword, content, date(published_at)
        FROM posts
        WHERE keyword IN ({})
          AND published_at BETWEEN ? AND ?
        ORDER BY published_at
    """.format(",".join("?" * len(FOREIGN_MATTER_KEYWORDS))),
        FOREIGN_MATTER_KEYWORDS + [BASELINE_START, BASELINE_END]
    ).fetchall()

    direct = [(pid, kw, c, d) for pid, kw, c, d in all_baseline
              if any(t in c for t in DIRECT_FM_TERMS)]
    indirect = [(pid, kw, c, d) for pid, kw, c, d in all_baseline
                if not any(t in c for t in DIRECT_FM_TERMS)]

    print(f"  이물질 직접 언급: {len(direct)}건 / {len(all_baseline)}건 "
          f"({len(direct)/max(len(all_baseline),1)*100:.1f}%)")
    print(f"  일반 부작용/피해 담론: {len(indirect)}건 "
          f"({len(indirect)/max(len(all_baseline),1)*100:.1f}%)")

    # -- 3. 키워드별 샘플 3건씩 본문 출력 --------------------------------
    print("\n" + "=" * 65)
    print("3. 키워드별 샘플 (최대 3건, 본문 150자)")
    print("=" * 65)

    for kw in FOREIGN_MATTER_KEYWORDS:
        samples = conn.execute("""
            SELECT post_id, content, date(published_at)
            FROM posts
            WHERE keyword = ?
              AND published_at BETWEEN ? AND ?
            ORDER BY published_at
            LIMIT 3
        """, (kw, BASELINE_START, BASELINE_END)).fetchall()

        if not samples:
            continue

        print(f"\n  [키워드: {kw}]")
        for pid, content, d in samples:
            direct_flag = "[직접언급]" if any(t in content for t in DIRECT_FM_TERMS) else "[일반담론]"
            print(f"  {d} {direct_flag}")
            print(f"  {content[:150]}")
            print(f"  {'-'*60}")

    # -- 4. 이물질 직접 언급 게시물 날짜별 집계 --------------------------
    if direct:
        print("\n" + "=" * 65)
        print("4. 이물질 직접 언급 게시물 날짜별 분포")
        print("=" * 65)
        date_dist = {}
        for _, _, _, d in direct:
            date_dist[d] = date_dist.get(d, 0) + 1
        for d in sorted(date_dist):
            print(f"  {d}: {date_dist[d]}건")

    conn.close()
    print("\n[OK] 완료.")


if __name__ == "__main__":
    main()
