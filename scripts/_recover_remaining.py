"""남은 72건 unrecoverable → 전 차원 0 처리 (모두 백신 무관 거부)"""
import json, re, sys

sys.stdout.reconfigure(encoding="utf-8")

SRC = "data/exports/labeled/naver_all_20260311_040325_batch_recovered.jsonl"
DST = SRC  # 덮어쓰기

rows = [json.loads(l) for l in open(SRC, encoding="utf-8") if l.strip()]

# unrecoverable 중 JSON 추출 재시도 (중첩 포함)
fixed_json = 0
fixed_zero = 0

for r in rows:
    if r.get("recovery") != "unrecoverable":
        continue

    raw = r.get("parse_error", "")

    # 중첩 JSON 재시도 (줄바꿈 포함)
    m = re.search(r'\{"C1":\s*\d.*?\}', raw, re.DOTALL)
    if m:
        try:
            obj = json.loads(m.group())
            if "C1" in obj:
                for c in ["C1", "C2", "C4", "C6", "C7"]:
                    r[f"pred_{c}"] = obj.get(c, 0)
                r["rationale"] = obj.get("rationale", {})
                r["parse_error"] = None
                r["recovery"] = "json_extracted_v2"
                fixed_json += 1
                continue
        except json.JSONDecodeError:
            pass

    # 나머지: 모두 백신 무관 거부 → 0 처리
    for c in ["C1", "C2", "C4", "C6", "C7"]:
        r[f"pred_{c}"] = 0
    r["rationale"] = {}
    r["parse_error"] = None
    r["recovery"] = "refusal_zeroed_v2"
    fixed_zero += 1

with open(DST, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print(f"[2차 복구]")
print(f"  JSON 추출: {fixed_json}건")
print(f"  거부→0:    {fixed_zero}건")

# 최종 검증
rows2 = [json.loads(l) for l in open(DST, encoding="utf-8") if l.strip()]
remaining = sum(1 for r in rows2 if any(r.get(f"pred_{c}") == -1 for c in ["C1","C2","C4","C6","C7"]))
print(f"\n[최종] 남은 -1: {remaining}건 / {len(rows2)}건")

# recovery 분포
from collections import Counter
dist = Counter(r.get("recovery") for r in rows2)
print(f"\n[recovery 분포]")
for k, v in dist.most_common():
    print(f"  {k or '(정상)':25s}: {v:>5,}건")

# 차원별
print(f"\n[최종 차원별 양성 비율]")
for c in ["C1", "C2", "C4", "C6", "C7"]:
    col = f"pred_{c}"
    pos = sum(1 for r in rows2 if r.get(col) == 1)
    print(f"  {c}: {pos:>5,} / {len(rows2)} ({pos/len(rows2)*100:.1f}%)")
