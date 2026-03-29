"""
fix_negative_preds.py

목적: pred 값이 -1인 레코드를 모두 0으로 교체 → cleaned JSONL 저장
      → 전체 수치 재산출 → stats_final.txt 출력

실행: cd C:\infovail-iq && python scripts\fix_negative_preds.py
"""

import sqlite3, json, math
from pathlib import Path
from collections import defaultdict, Counter
from scipy.stats import fisher_exact

BASE_DIR = Path(__file__).parent.parent
JSONL_PATH  = BASE_DIR / "data/exports/labeled/naver_all_20260322_final_v2.jsonl"
CLEAN_PATH  = BASE_DIR / "data/exports/labeled/naver_all_20260322_final_v3.jsonl"
OUT_PATH    = BASE_DIR / "data/exports/stats_final.txt"
DB_PATH     = BASE_DIR / "data/processed/naver_posts.db"

E1 = '2026-02-23'
E2 = '2026-03-02'
DIMS = ['C1', 'C4', 'C6', 'C7']

def get_period(d):
    d = str(d)[:10]
    return 'Pre-E1' if d < E1 else ('E1->E2' if d < E2 else 'Post-E2')

def or_ci(a, b, c, d):
    try:
        _, p = fisher_exact([[a, b], [c, d]])
        if 0 in (a,b,c,d):
            a,b,c,d = a+0.5, b+0.5, c+0.5, d+0.5
        orv = (a*d)/(b*c)
        se = math.sqrt(1/a+1/b+1/c+1/d)
        return orv, math.exp(math.log(orv)-1.96*se), math.exp(math.log(orv)+1.96*se), p
    except:
        return float('nan'),float('nan'),float('nan'),float('nan')

def fp(p):
    if math.isnan(p): return "N/A"
    return "p<0.001***" if p<0.001 else (f"p={p:.3f}**" if p<0.01 else (f"p={p:.3f}*" if p<0.05 else f"p={p:.3f} ns"))

# ── Step 1: JSONL 정제 ─────────────────────────────────────────────
records = []
neg_count = 0
with open(JSONL_PATH, encoding='utf-8') as f:
    for line in f:
        r = json.loads(line)
        fixed = False
        for dim in DIMS:
            k = f'pred_{dim}'
            if isinstance(r.get(k), int) and r[k] < 0:
                r[k] = 0
                fixed = True
        if fixed:
            neg_count += 1
        records.append(r)

with open(CLEAN_PATH, 'w', encoding='utf-8') as f:
    for r in records:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')

print(f"[Step 1] -1 레코드 {neg_count}건 → 0으로 교체")
print(f"         저장: {CLEAN_PATH.name} ({len(records)}건)")

# ── Step 2: 수치 재산출 ────────────────────────────────────────────
preds = {}
for r in records:
    pid = r['post_id']
    pred = {}
    valid = True
    for dim in DIMS:
        v = r.get(f'pred_{dim}')
        if not isinstance(v, int): valid=False; break
        pred[dim] = v
    if valid: preds[pid] = pred

db = sqlite3.connect(DB_PATH)
cur = db.cursor()
cur.execute("SELECT post_id, published_at, keyword_group FROM posts WHERE published_at IS NOT NULL")
rows = cur.fetchall()
db.close()

stats = defaultdict(lambda: defaultdict(lambda: {
    'total':0, 'matched':0, **{d:0 for d in DIMS}, 'C1_C7':0
}))
for post_id, pub_at, kg in rows:
    period = get_period(pub_at)
    s = stats[kg][period]
    s['total'] += 1
    if post_id in preds:
        s['matched'] += 1
        for dim in DIMS: s[dim] += preds[post_id][dim]
        if preds[post_id]['C1']==1 and preds[post_id]['C7']==1: s['C1_C7'] += 1

# ── Step 3: 출력 ───────────────────────────────────────────────────
lines = []
lines.append("naver_all_20260322_final_v3.jsonl 기준 최종 수치")
lines.append(f"(-1 sentinel {neg_count}건 -> 0 교체 완료)")
lines.append("")

lines.append("=" * 110)
lines.append("SECTION 1: 기간별 양성률")
lines.append("=" * 110)
lines.append(f"{'Group':<12} {'Period':<10} {'N':>6} {'Match':>6}  {'C1%':>6} {'C4%':>6} {'C6%':>6} {'C7%':>6} {'C1+C7%':>8}")
lines.append("-" * 74)
for group in ['FM_Direct','Court','Chronic']:
    for period in ['Pre-E1','E1->E2','Post-E2']:
        s = stats[group][period]
        n=s['total']; m=s['matched']
        if n==0: continue
        pcts = {d: s[d]/n*100 for d in DIMS}
        co = s['C1_C7']/n*100
        lines.append(f"{group:<12} {period:<10} {n:>6} {m:>6}  "
                     f"{pcts['C1']:>5.1f}% {pcts['C4']:>5.1f}% "
                     f"{pcts['C6']:>5.1f}% {pcts['C7']:>5.1f}% {co:>7.1f}%")
    lines.append("-" * 74)

lines.append("")
lines.append("=" * 114)
lines.append("SECTION 2: OR (Pre-E1 vs Post-E2, Fisher's exact)")
lines.append("=" * 114)
lines.append(f"{'Group+Dim':<20} {'Pre n':>6} {'Pre%':>7} {'E1->E2%':>9} {'Post n':>7} {'Post%':>7} {'Delta':>8}  {'OR (95% CI)':<28} {'p'}")
lines.append("-" * 112)
for group in ['FM_Direct','Court','Chronic']:
    pre  = stats[group]['Pre-E1']
    mid  = stats[group]['E1->E2']
    post = stats[group]['Post-E2']
    n_pre=pre['total']; n_mid=mid['total']; n_post=post['total']
    if n_pre==0 or n_post==0: continue
    for dim in DIMS:
        pre_pct  = pre[dim]/n_pre*100
        mid_pct  = mid[dim]/n_mid*100 if n_mid>0 else 0
        post_pct = post[dim]/n_post*100
        delta    = post_pct - pre_pct
        a=post[dim]; b=n_post-a; c=pre[dim]; d=n_pre-c
        orv,ci_lo,ci_hi,p = or_ci(a,b,c,d)
        or_str = f"{orv:.2f} ({ci_lo:.2f}-{ci_hi:.2f})" if not math.isnan(orv) else "N/A"
        label  = f"{group} {dim}"
        lines.append(f"{label:<20} {n_pre:>6} {pre_pct:>6.1f}% {mid_pct:>8.1f}% "
                     f"{n_post:>7} {post_pct:>6.1f}% {delta:>+7.1f}pp  "
                     f"{or_str:<28} {fp(p)}")
    lines.append("-" * 112)

lines.append("")
lines.append("=" * 74)
lines.append("SECTION 3: C1+C7 Co-occurrence")
lines.append("=" * 74)
lines.append(f"{'Group':<12} {'Pre n':>6} {'Pre C1+C7':>10} {'Pre%':>7} {'Post n':>7} {'Post C1+C7':>11} {'Post%':>7} {'Fold':>6}")
lines.append("-" * 74)
for group in ['FM_Direct','Court','Chronic']:
    pre  = stats[group]['Pre-E1']
    post = stats[group]['Post-E2']
    n_pre=pre['total']; n_post=post['total']
    pre_rate  = pre['C1_C7']/n_pre*100   if n_pre>0  else 0
    post_rate = post['C1_C7']/n_post*100 if n_post>0 else 0
    fold = post_rate/pre_rate if pre_rate>0 else float('nan')
    fold_str = f"{fold:.1f}x" if not math.isnan(fold) else "N/A"
    lines.append(f"{group:<12} {n_pre:>6} {pre['C1_C7']:>10} {pre_rate:>6.1f}% "
                 f"{n_post:>7} {post['C1_C7']:>11} {post_rate:>6.1f}% {fold_str:>6}")

lines.append("")
lines.append("=" * 114)
lines.append("SECTION 4: 논문 교체 치트시트 (Discussion + Results 직접 대입용)")
lines.append("=" * 114)
lines.append(f"{'Group+Dim':<20} {'Pre%':>7} {'E1->E2%':>9} {'Post%':>7} {'Delta':>8}  {'OR (95% CI)':<28} {'p'}")
lines.append("-" * 94)
for group in ['FM_Direct','Court','Chronic']:
    pre  = stats[group]['Pre-E1']
    mid  = stats[group]['E1->E2']
    post = stats[group]['Post-E2']
    n_pre=pre['total']; n_mid=mid['total']; n_post=post['total']
    if n_pre==0 or n_post==0: continue
    for dim in DIMS:
        pre_pct  = pre[dim]/n_pre*100
        mid_pct  = mid[dim]/n_mid*100 if n_mid>0 else 0
        post_pct = post[dim]/n_post*100
        delta    = post_pct - pre_pct
        a=post[dim]; b=n_post-a; c=pre[dim]; d=n_pre-c
        orv,ci_lo,ci_hi,p = or_ci(a,b,c,d)
        or_str = f"{orv:.2f} ({ci_lo:.2f}-{ci_hi:.2f})" if not math.isnan(orv) else "N/A"
        label = f"{group} {dim}"
        lines.append(f"{label:<20} {pre_pct:>6.1f}% {mid_pct:>8.1f}% {post_pct:>6.1f}% "
                     f"{delta:>+7.1f}pp  {or_str:<28} {fp(p)}")
    lines.append("-" * 94)

out = "\n".join(lines)
with open(OUT_PATH, 'w', encoding='utf-8') as f:
    f.write(out)

print(f"[Step 3] 저장 완료: {OUT_PATH.name}")
print(out)
