"""
diagnose_c4.py — C4 음수값 원인 진단
실행: cd C:\infovail-iq && python scripts\diagnose_c4.py
"""
import json, sqlite3
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).parent.parent
JSONL_PATH = BASE_DIR / "data/exports/labeled/naver_all_20260322_final_v2.jsonl"
DB_PATH = BASE_DIR / "data/processed/naver_posts.db"
E2 = '2026-03-02'

# DB에서 FM_Direct + Chronic Post-E2 post_id 수집
db = sqlite3.connect(DB_PATH)
cur = db.cursor()
cur.execute("SELECT post_id, keyword_group, published_at FROM posts WHERE published_at IS NOT NULL")
target = {r[0]: r[1] for r in cur.fetchall() if str(r[2])[:10] >= E2 and r[1] in ('FM_Direct','Chronic')}
db.close()

# JSONL에서 해당 posts의 pred_C4 확인
c4_vals = Counter()
negative_examples = []

with open(JSONL_PATH, encoding='utf-8') as f:
    for line in f:
        r = json.loads(line)
        pid = r['post_id']
        if pid not in target:
            continue
        v = r.get('pred_C4')
        c4_vals[v] += 1
        if isinstance(v, int) and v < 0:
            negative_examples.append({
                'post_id': pid,
                'group': target[pid],
                'pred_C4': v,
                'pred_C1': r.get('pred_C1'),
                'pred_C7': r.get('pred_C7'),
                'rationale': str(r.get('rationale', ''))[:100]
            })

print("FM_Direct+Chronic Post-E2 pred_C4 값 분포:")
for val, cnt in sorted(c4_vals.items(), key=lambda x: str(x[0])):
    print(f"  pred_C4={val!r}: {cnt}건")

print(f"\n음수 예시 ({len(negative_examples)}건):")
for ex in negative_examples[:10]:
    print(f"  {ex['group']} | C4={ex['pred_C4']} | C1={ex['pred_C1']} C7={ex['pred_C7']}")
    print(f"    rationale: {ex['rationale']}")
