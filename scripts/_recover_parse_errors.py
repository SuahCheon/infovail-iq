"""parse_error 복구 스크립트
- JSON 추출 가능 → 복구
- 분류 거부 (백신 무관) → 전 차원 0
- 복구 불가 → -1 유지
"""
import json, re, sys

sys.stdout.reconfigure(encoding="utf-8")

SRC = "data/exports/labeled/naver_all_20260311_040325_batch.jsonl"
DST = "data/exports/labeled/naver_all_20260311_040325_batch_recovered.jsonl"

rows = [json.loads(l) for l in open(SRC, encoding="utf-8") if l.strip()]
print(f"원본: {len(rows)}건")

stats = {"json_recovered": 0, "refusal_zeroed": 0, "unrecoverable": 0, "already_ok": 0}

for r in rows:
    if not r.get("parse_error"):
        stats["already_ok"] += 1
        continue

    raw = r["parse_error"]

    # 1) JSON 추출 시도
    clean = raw.replace("```json", "").replace("```", "")
    m = re.search(r"\{[^{}]*\}", clean, re.DOTALL)
    if m:
        try:
            obj = json.loads(m.group())
            if "C1" in obj:
                for c in ["C1", "C2", "C4", "C6", "C7"]:
                    r[f"pred_{c}"] = obj.get(c, 0)
                r["rationale"] = obj.get("rationale", {})
                r["parse_error"] = None
                r["recovery"] = "json_extracted"
                stats["json_recovered"] += 1
                continue
        except json.JSONDecodeError:
            pass

    # 2) 분류 거부 → 전 차원 0
    refusal_signals = [
        "cannot classify", "not a social media", "not about vaccine",
        "not vaccine", "unrelated", "분류할 수 없", "백신 관련 내용이 아",
        "분류 대상이 아", "분석 불가", "does not contain vaccine",
        "does not appear to be about vaccine", "table of contents",
        "navigation structure", "fragmented", "incomplete",
        "news headline", "not a coherent",
    ]
    raw_lower = raw.lower()
    if any(sig in raw_lower for sig in refusal_signals):
        for c in ["C1", "C2", "C4", "C6", "C7"]:
            r[f"pred_{c}"] = 0
        r["rationale"] = {}
        r["parse_error"] = None
        r["recovery"] = "refusal_zeroed"
        stats["refusal_zeroed"] += 1
        continue

    # 3) 복구 불가
    r["recovery"] = "unrecoverable"
    stats["unrecoverable"] += 1

# 저장
with open(DST, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print(f"\n[복구 결과]")
print(f"  원래 정상:       {stats['already_ok']:>5,}건")
print(f"  JSON 추출 복구:  {stats['json_recovered']:>5,}건")
print(f"  거부 → 0 처리:   {stats['refusal_zeroed']:>5,}건")
print(f"  복구 불가 (-1):  {stats['unrecoverable']:>5,}건")
print(f"  합계:            {sum(stats.values()):>5,}건")

# 최종 검증
recovered = [json.loads(l) for l in open(DST, encoding="utf-8") if l.strip()]
remaining_errors = sum(1 for r in recovered if any(r.get(f"pred_{c}") == -1 for c in ["C1","C2","C4","C6","C7"]))
print(f"\n[최종] 남은 -1 포스트: {remaining_errors}건")

# 차원별 양성 비율 (복구 후)
print(f"\n[복구 후 차원별 양성 비율]")
total = len(recovered)
for c in ["C1", "C2", "C4", "C6", "C7"]:
    col = f"pred_{c}"
    pos = sum(1 for r in recovered if r.get(col) == 1)
    print(f"  {c}: {pos:>5,} ({pos/total*100:.1f}%)")

print(f"\n저장: {DST}")
