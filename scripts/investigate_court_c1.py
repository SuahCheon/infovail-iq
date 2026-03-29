"""
investigate_court_c1.py
-----------------------
Court 그룹 C1 패턴 분석 + 전체 코퍼스 볼륨 교란 변수 비교 (6주 전체)

Usage:
    python scripts/investigate_court_c1.py \
        --db   data/processed/naver_posts.db \
        --pred data/exports/labeled/naver_all_20260323_202551_batch.jsonl
"""

import argparse, json, sqlite3
import pandas as pd
import numpy as np

E1 = pd.Timestamp('2026-02-23')
E2 = pd.Timestamp('2026-03-02')
DATE_START = '2026-02-07'
DATE_END   = '2026-03-21'


def load_data(db_path, pred_path):
    con = sqlite3.connect(db_path)

    court = pd.read_sql("""
        SELECT post_id, keyword_group, published_at, content
        FROM posts
        WHERE is_relevant = 1
          AND published_at IS NOT NULL
          AND keyword_group = 'Court'
    """, con)

    total = pd.read_sql("""
        SELECT published_at, COUNT(*) as total_n
        FROM posts
        WHERE is_relevant = 1
          AND published_at IS NOT NULL
        GROUP BY SUBSTR(published_at, 1, 10)
    """, con)
    con.close()

    court['pub_date'] = pd.to_datetime(court['published_at'].str[:10], errors='coerce')
    court = court.dropna(subset=['pub_date'])
    total['pub_date'] = pd.to_datetime(total['published_at'].str[:10], errors='coerce')

    rows = []
    with open(pred_path, encoding='utf-8') as f:
        for line in f:
            r = json.loads(line.strip())
            rows.append({
                'post_id': str(r['post_id']),
                'C1': max(0, r.get('pred_C1', 0)),
                'C7': max(0, r.get('pred_C7', 0)),
            })
    pred = pd.DataFrame(rows)

    merged = court.merge(pred, on='post_id', how='inner')
    return merged, total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db',   required=True)
    parser.add_argument('--pred', required=True)
    args = parser.parse_args()

    df, total_df = load_data(args.db, args.pred)

    # 6주 전체
    df = df[(df['pub_date'] >= DATE_START) & (df['pub_date'] <= DATE_END)]
    total_df = total_df[
        (total_df['pub_date'] >= DATE_START) &
        (total_df['pub_date'] <= DATE_END)
    ]

    # Court 날짜별 집계
    daily = df.groupby('pub_date').agg(
        court_n=('post_id', 'count'),
        C1_n=('C1', 'sum'),
        C7_n=('C7', 'sum'),
    ).reset_index()
    daily['C1_pct'] = (daily['C1_n'] / daily['court_n'] * 100).round(1)
    daily['C7_pct'] = (daily['C7_n'] / daily['court_n'] * 100).round(1)

    # 전체 코퍼스 볼륨 병합
    daily = daily.merge(total_df, on='pub_date', how='left')

    # 기간 레이블
    def period(d):
        if d < E1: return 'Pre-E1'
        elif d < E2: return 'E1→E2'
        else: return 'Post-E2'
    daily['period'] = daily['pub_date'].apply(period)

    # 전체 출력
    print("=== 6주 전체: Court C1/C7 + 전체 코퍼스 볼륨 ===\n")
    print(f"{'날짜':<12} {'기간':<8} {'전체n':>6} {'Court_n':>8} {'C1(%)':>7} {'C7(%)':>7}")
    print("-" * 58)
    for _, r in daily.sort_values('pub_date').iterrows():
        flag = ' ←' if r['C1_pct'] < 50 and r['period'] == 'Post-E2' else ''
        print(f"{str(r['pub_date'].date()):<12} {r['period']:<8} "
              f"{int(r['total_n']):>6} {int(r['court_n']):>8} "
              f"{r['C1_pct']:>7} {r['C7_pct']:>7}{flag}")

    # 상관관계: 전체 볼륨 vs Court C1%
    corr = daily['total_n'].corr(daily['C1_pct'])
    print(f"\n전체 볼륨 vs Court C1% 상관계수: {corr:.3f}")
    print("(음수 강할수록 → 전체 볼륨 낮은 날 Court C1도 낮음 = 교란 효과)")

    # Post-E2 낮은 C1 날 샘플
    low = daily[(daily['period'] == 'Post-E2') & (daily['C1_pct'] < 50)]
    if len(low) > 0:
        print(f"\n=== Post-E2 C1 < 50% 날짜 포스트 샘플 ===")
        for _, row in low.iterrows():
            day = row['pub_date']
            print(f"\n[{day.date()}] 전체볼륨={int(row['total_n'])}, Court_n={int(row['court_n'])}, C1={row['C1_pct']}%")
            sample = df[(df['pub_date'] == day) & (df['C1'] == 0)].head(3)
            for _, p in sample.iterrows():
                text = str(p['content'] or '')[:100]
                print(f"  C1=0: {text}")

    # 전체 볼륨 낮은 날 (하위 25%) 확인
    q25 = total_df['total_n'].quantile(0.25)
    low_vol_days = total_df[total_df['total_n'] <= q25]['pub_date'].tolist()
    print(f"\n전체 볼륨 하위 25% 기준값: {q25:.0f}건")
    print(f"해당 날짜: {[str(d.date()) for d in sorted(low_vol_days)]}")


if __name__ == '__main__':
    main()
