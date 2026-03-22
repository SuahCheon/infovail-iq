"""parse_error 패턴 분석 스크립트"""
import json, re, sys

sys.stdout.reconfigure(encoding="utf-8")

f = "data/exports/labeled/naver_all_20260311_040325_batch.jsonl"
rows = [json.loads(l) for l in open(f, encoding="utf-8") if l.strip()]
errors = [r for r in rows if r.get("parse_error")]
print(f"parse_error 총: {len(errors)}건\n")

# 패턴 분류
refusal = []
json_recoverable = []
markdown_wrap = []
truly_broken = []

for r in errors:
    raw = r["parse_error"]
    if raw.strip().startswith("I ") or raw.strip().startswith("I\n"):
        refusal.append(r)
    elif "```" in raw:
        markdown_wrap.append(r)
    elif "{" in raw and "}" in raw:
        json_recoverable.append(r)
    else:
        truly_broken.append(r)

print(f"[1] 분류 거부 (I cannot...): {len(refusal)}건")
for r in refusal[:3]:
    print(f"  >> {r['parse_error'][:120]}")
print()

print(f"[2] markdown 래핑: {len(markdown_wrap)}건")
for r in markdown_wrap[:3]:
    print(f"  >> {r['parse_error'][:120]}")
print()

print(f"[3] JSON 포함 (복구 시도 가능): {len(json_recoverable)}건")
for r in json_recoverable[:3]:
    print(f"  >> {r['parse_error'][:120]}")
print()

print(f"[4] 기타: {len(truly_broken)}건")
for r in truly_broken[:3]:
    print(f"  >> {r['parse_error'][:120]}")
print()

# 복구 시도
recovered = 0
for r in json_recoverable + markdown_wrap:
    raw = r["parse_error"]
    # markdown 제거
    clean = raw.replace("```json", "").replace("```", "").strip()
    # JSON 블록 추출
    m = re.search(r"\{.*\}", clean, re.DOTALL)
    if m:
        try:
            obj = json.loads(m.group())
            if "C1" in obj:
                recovered += 1
        except json.JSONDecodeError:
            pass

print(f"[복구 가능] JSON 추출 성공: {recovered}건 / {len(json_recoverable) + len(markdown_wrap)}건")

# 거부 사유 분석
print(f"\n[거부 사유 상세]")
reasons = {}
for r in refusal:
    raw = r["parse_error"]
    if "table of contents" in raw.lower() or "navigation" in raw.lower():
        reasons.setdefault("목차/네비게이션 구조", []).append(r["post_id"])
    elif "fragmented" in raw.lower() or "incomplete" in raw.lower():
        reasons.setdefault("단편/불완전 텍스트", []).append(r["post_id"])
    elif "news" in raw.lower() or "headline" in raw.lower() or "article" in raw.lower():
        reasons.setdefault("뉴스 기사/헤드라인", []).append(r["post_id"])
    elif "not a social media" in raw.lower():
        reasons.setdefault("SNS 포스트 아님", []).append(r["post_id"])
    elif "vaccine" in raw.lower() and ("not" in raw.lower() or "unrelated" in raw.lower()):
        reasons.setdefault("백신 무관", []).append(r["post_id"])
    else:
        reasons.setdefault("기타 거부", []).append(r["post_id"])

for k, v in sorted(reasons.items(), key=lambda x: -len(x[1])):
    print(f"  {k}: {len(v)}건")
