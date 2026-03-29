"""
verify_prevalence.py

목적: Discussion/Results 기재 수치와 실제 분류 결과 일치 여부 전면 검증
      - naver_all_20260322_final_v2.jsonl (pred 값)
      - naver_posts.db (날짜, 그룹 정보)

출력: 그룹 x 기간 x 차원별 실제 양성률 vs 논문 기재값 비교표
실행: cd C:\infovail-iq && python scripts\verify_prevalence.py
"""

import sqlite3
import json
import sys
import io
from pathlib import Path
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "data/processed/naver_posts.db"
JSONL_PATH = BASE_DIR / "data/exports/labeled/naver_all_20260322_final_v2.jsonl"

# ── 이벤트 기준일 ──────────────────────────────────────────────────
E1 = '2026-02-23'  # BAI 감사 결과 공표
E2 = '2026-03-02'  # SBS 보도 / 심근경색 판결

DIMS = ['C1', 'C4', 'C6', 'C7']

# ── 논문 기재값 (Discussion v0.2.0 + Results v0.1.0) ───────────────
# 형식: (Discussion값, Results값) — None = 미기재
PAPER_VALUES = {
    ('FM_Direct', 'Pre-E1',  'C1'): (21.6, 21.6),
    ('FM_Direct', 'E1->E2',  'C1'): (75.3, 75.3),
    ('FM_Direct', 'Post-E2', 'C1'): (73.2, 69.5),
    ('FM_Direct', 'Post-E2', 'C7'): (25.4, 25.4),
    ('Court',     'Pre-E1',  'C1'): (7.1,  7.1),
    ('Court',     'Pre-E1',  'C7'): (35.1, 35.1),
    ('Court',     'Post-E2', 'C1'): (58.6, 58.6),
    ('Court',     'Post-E2', 'C4'): (5.4,  5.4),
    ('Court',     'Post-E2', 'C6'): (2.6,  2.6),
    ('Court',     'Post-E2', 'C7'): (14.3, 14.3),
    ('Chronic',   'Pre-E1',  'C1'): (16.1, 16.1),
    ('Chronic',   'Post-E2', 'C1'): (48.0, 48.0),
    ('Chronic',   'Post-E2', 'C6'): (4.8,  4.8),
    ('Chronic',   'Post-E2', 'C7'): (10.8, 10.8),
}

def get_period(date_str):
    d = str(date_str)[:10]
    if d < E1:
        return 'Pre-E1'
    elif d < E2:
        return 'E1->E2'
    else:
        return 'Post-E2'

def main():
    # pred 로드
    preds = {}
    parse_errors = 0
    with open(JSONL_PATH, encoding='utf-8') as f:
        for line in f:
            r = json.loads(line)
            pid = r['post_id']
            pred = {}
            valid = True
            for dim in DIMS:
                v = r.get(f'pred_{dim}')
                if not isinstance(v, int):
                    valid = False
                    break
                pred[dim] = v
            if valid:
                preds[pid] = pred
            else:
                parse_errors += 1

    print(f"JSONL 로드: {len(preds)}건 정상, {parse_errors}건 parse 오류 (zero fallback 포함)")

    # DB에서 날짜 + 그룹 로드
    db = sqlite3.connect(DB_PATH)
    cur = db.cursor()
    cur.execute("""
        SELECT post_id, published_at, keyword_group
        FROM posts
        WHERE published_at IS NOT NULL
    """)
    rows = cur.fetchall()
    db.close()

    print(f"DB 로드: {len(rows)}건")

    # 집계
    stats = defaultdict(lambda: {'total': 0, 'matched': 0, **{d: 0 for d in DIMS}})
    unmatched = 0

    for post_id, pub_at, kg in rows:
        period = get_period(pub_at)
        key = (kg, period)
        stats[key]['total'] += 1
        if post_id in preds:
            stats[key]['matched'] += 1
            for dim in DIMS:
                stats[key][dim] += preds[post_id][dim]
        else:
            unmatched += 1

    print(f"DB<->JSONL 미매칭: {unmatched}건\n")

    # 결과 출력
    print("=" * 90)
    print(f"{'Group':<12} {'Period':<10} {'N':>6} {'Match':>6}  {'C1%':>6} {'C4%':>6} {'C6%':>6} {'C7%':>6}")
    print("=" * 90)

    issues = []
    actual_values = {}

    for group in ['FM_Direct', 'Court', 'Chronic']:
        for period in ['Pre-E1', 'E1->E2', 'Post-E2']:
            key = (group, period)
            s = stats[key]
            n = s['total']
            m = s['matched']
            if n == 0:
                continue
            # matched 기준으로 비율 계산 (미매칭 = zero 처리)
            pcts = {d: s[d] / n * 100 for d in DIMS}
            actual_values[key] = pcts
            print(f"{group:<12} {period:<10} {n:>6} {m:>6}  "
                  f"{pcts['C1']:>5.1f}% {pcts['C4']:>5.1f}% "
                  f"{pcts['C6']:>5.1f}% {pcts['C7']:>5.1f}%")

            # 논문 기재값과 비교
            for dim in DIMS:
                paper_key = (group, period, dim)
                if paper_key in PAPER_VALUES:
                    disc_val, res_val = PAPER_VALUES[paper_key]
                    actual = round(pcts[dim], 1)
                    disc_diff = actual - disc_val
                    res_diff = actual - res_val
                    if abs(disc_diff) > 0.5 or abs(res_diff) > 0.5:
                        issues.append({
                            'location': f"{group} {period} {dim}",
                            'actual': actual,
                            'discussion': disc_val,
                            'results': res_val,
                            'disc_diff': disc_diff,
                            'res_diff': res_diff,
                        })
        print("-" * 90)

    # 불일치 요약
    print("\n" + "=" * 90)
    print("불일치 항목 요약 (허용 오차 +-0.5pp 초과)")
    print("=" * 90)
    if issues:
        print(f"{'Location':<30} {'Actual':>8} {'Disc.':>8} {'Res.':>8} {'DeltaDisc':>10} {'DeltaRes':>10}")
        print("-" * 78)
        for iss in sorted(issues, key=lambda x: -max(abs(x['disc_diff']), abs(x['res_diff']))):
            print(f"{iss['location']:<30} {iss['actual']:>7.1f}% "
                  f"{iss['discussion']:>7.1f}% {iss['results']:>7.1f}% "
                  f"{iss['disc_diff']:>+9.1f} {iss['res_diff']:>+9.1f}")
    else:
        print("모든 기재값이 실제값과 일치합니다.")

    print(f"\n총 불일치 항목: {len(issues)}건")
    print("\n※ Delta = Actual - Paper value (양수: 실제가 더 높음, 음수: 실제가 더 낮음)")

if __name__ == '__main__':
    main()
