"""
llm_runner.py  — v6
--------------------
Claude Haiku 4.5 기반 7C 백신 주저함 분류기

변경 이력:
  v1  초안 (2026-03-10)
  v2  2026-03-10
      [필수] CSV 경로 수정: f"{split}_processed.csv" → f"{split}.csv"
      [권장] Batch API 모드 추가 (--batch 플래그)
      [권장] tenacity exponential backoff retry (실시간 모드 fallback)
      [권장] 영어 벤치마크에도 rationale 포함 (error analysis용)
      [권장] few-shot 선정 기준 주석 명시
  v3  2026-03-10
      [필수] _print_cost_summary 가격 상수 수정:
             Haiku 3.5 오기 → Haiku 4.5 실제 공시가
             input $0.80 → $1.00, output $4.00 → $5.00,
             cache write $1.00 → $1.25, cache read $0.08 → $0.10
      [필수] load_dotenv(override=True) 추가
      [필수] CAVES_DIR 경로 수정: data\caves 경로 통일
  v4  2026-03-10
      [프롬프트 v1.2.0] C4 정의: rushed development → C1 경고 추가
      [프롬프트 v1.2.0] C7 정의: 악의적 의도 임계값 명시, 강한 분노만으로 C7 불가
      [프롬프트 v1.2.0] Key Distinctions: C2 vs C4, C1 vs C4 negative example 추가
      (근거: 200건 벤치마크 — C4 FP 37건, C7 FP 28건 과잉분류 패턴)
  v5  2026-03-10
      [프롬프트 v1.3.0] C4 정의: "Do NOT" 경고 → 긍정적 신호 중심 완화
      [프롬프트 v1.3.0] C7 few-shot: 극단 음모론(1400628010043195397t) →
                        boundary case(1337526914781679616t, 의도적 은폐) 교체
      (근거: v1.2.0 200건 — C4 recall 급락 0.565→0.348, C7 FP 거의 미변)
  v6  2026-03-10
      [프롬프트 v1.1.0 복원] v1.2.0~v1.3.0 system prompt 변경 전량 revert
      [프롬프트 v1.1.0 복원] C7 few-shot: boundary case → 원본 극단 예시 복원
      (근거: 전체 test set(1846건) 비교 — v1.1.0 macro F1 0.585 > v1.3.0 0.569
       200건 샘플 최적화가 전체 데이터에서 역효과 확인)

모델: claude-haiku-4-5-20251001 (snapshot ID 고정 — 논문 재현성 확보)
     → README 및 논문 Methods에 snapshot ID 명시 필요

Usage:
    # 영어 벤치마크 — 샘플 200건 (프롬프트 탐색용)
    python llm_runner.py --mode en --sample 200

    # 영어 벤치마크 — test set 전체, Batch API
    python llm_runner.py --mode en --split test --batch

    # 한국어 전체 분류, Batch API
    python llm_runner.py --mode ko --batch

    # 한국어 특정 그룹만
    python llm_runner.py --mode ko --group FM_Direct

환경변수 (.env):
    ANTHROPIC_API_KEY=sk-ant-...   ← 필수
    NAVER_CLIENT_ID=...            ← 이 스크립트에서 불필요
    NAVER_CLIENT_SECRET=...
"""

import anthropic
import sqlite3
import json
import time
import argparse
import random
import csv
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

load_dotenv(override=True)

# ── 설정 ──────────────────────────────────────────────────────────────────────

BASE_DIR   = Path(r"C:\infovail-iq")
CAVES_DIR  = Path(r"C:\infovail-iq\data\caves\processed")
NAVER_DB   = BASE_DIR / "data" / "processed" / "naver_posts.db"
OUTPUT_DIR = BASE_DIR / "data" / "exports" / "labeled"

MODEL      = "claude-haiku-4-5-20251001"  # snapshot 고정 (재현성)
MAX_TOKENS = 512   # rationale 포함 여유 확보

# ── 시스템 프롬프트 (캐싱 대상) ───────────────────────────────────────────────

SYSTEM_PROMPT = """You are an expert classifier for vaccine hesitancy research.

Your task is to classify social media posts according to the 7C vaccine hesitancy framework.
Classify each post across the following 5 dimensions (binary: 1=present, 0=absent):

## Dimensions

**C1: Confidence**
Lack of trust in vaccine safety, efficacy, or the system delivering them (health authorities,
pharmaceutical companies, regulatory agencies).
Includes: concerns about side effects, doubts about efficacy, distrust of ingredients,
pharmaceutical company criticism, regulatory agency distrust, rushed development concerns,
distrust based on country of manufacture.

**C2: Complacency**
Low perceived risk of the vaccine-preventable disease, leading to perceiving vaccination
as unnecessary.
Includes: dismissing disease severity ("just a cold"), believing natural immunity is sufficient,
perceiving personal risk as too low to warrant vaccination.

**C4: Calculation**
Active information seeking and weighing of pros and cons before deciding whether to vaccinate.
Includes: explicitly seeking more data before deciding, comparing benefits and risks,
conditional acceptance ("I'll vaccinate when more data is available"), value-based weighing.

**C6: Compliance**
Resistance to compulsory vaccination or social pressure to vaccinate.
Includes: opposition to vaccine mandates or passes, criticism of coercive vaccination policies,
anger at being forced to vaccinate, resistance to discrimination against unvaccinated individuals.

**C7: Conspiracy**
Belief in malicious intent behind vaccines or vaccine policy — beyond simple distrust.
Includes: claims of deliberate concealment, government-pharma collusion, vaccines as population
control or surveillance tools, COVID-19 as a fabricated crisis.

## Key Distinctions

- C1 vs C7: C1 = distrust (incompetence/negligence possible); C7 = malicious intent assumed
  ("they knew and hid it deliberately")
- C2 vs C4: C2 = disease risk dismissed; C4 = actively seeking information to decide
- C1 vs C6: C1 = distrust of vaccine/system; C6 = resistance to coercion (vaccine itself
  may not be the issue)

## Output Format

Respond ONLY with valid JSON. No preamble, no markdown, no explanation outside the JSON.
Always include "rationale" — write only for dimensions scored 1, omit dimensions scored 0.
If all dimensions are 0, use "rationale": {}.

{"C1": 0, "C2": 0, "C4": 0, "C6": 0, "C7": 0, "rationale": {}}"""

# ── Few-shot 예시 ──────────────────────────────────────────────────────────────
#
# 선정 기준 (논문 Methods 기재용):
#   - 5개 활성 차원(C1/C2/C4/C6/C7) × 단일 레이블 예시 1개씩
#     (C4 단독 샘플은 CAVES에 존재하지 않으므로 C1+C4 복합 사용)
#   - 복합 레이블(multi-label) 예시 1개 (C1+C6+C7 — 본 연구 핵심 클러스터)
#   - 총 6개, CAVES train set에서 verbatim 선정 (test set 오염 방지)
#   - 각 예시는 해당 차원을 명확히 드러내는 텍스트 선택
#   - 선정 ID: 1280532929790259208t, 1361141045744967683t,
#              1254882873372524544t, 1355711914811289604t,
#              1400628010043195397t, 1337522336178851840t
#
# ※ 영어: CAVES train set verbatim / 한국어: 7C_CODEBOOK.md 예시 기반 작성
#   → 논문 기여점: "동일 프레임워크로 영어·한국어 다국어 분류 실증"

FEW_SHOT_EN = [
    # C1 단독 — 제약사 불신 (ID: 1280532929790259208t, CAVES: pharma)
    {
        "text": "And taxpayers just gave $ 1.6 billion to Novavax , a company that has brought nothing to market , the LARGEST covid vaccine contract . And best believe they will still charge for it .",
        "label": {"C1": 1, "C2": 0, "C4": 0, "C6": 0, "C7": 0,
                  "rationale": {"C1": "Pharmaceutical company distrust — public funding criticism implies system cannot be trusted to act in public interest."}}
    },
    # C2 단독 — 질병 위험 경시 (ID: 1361141045744967683t, CAVES: unnecessary)
    {
        "text": "@surveyorX Don't get the vaccine . It's 99 % survival rate . I have elderly patients who are surviving Covid .",
        "label": {"C1": 0, "C2": 1, "C4": 0, "C6": 0, "C7": 0,
                  "rationale": {"C2": "Disease risk dismissed via survival rate; even elderly framed as low-risk, vaccination perceived as unnecessary."}}
    },
    # C1+C4 — 검증 불신 + 정보 탐색 (ID: 1254882873372524544t, CAVES: rushed)
    {
        "text": "@ShangoKofi @RealCandaceO They usually take years to fully test and approve a vaccine . You can take this one . I'll wait . Thanks .",
        "label": {"C1": 1, "C2": 0, "C4": 1, "C6": 0, "C7": 0,
                  "rationale": {"C1": "Rushed development concern — insufficient testing period vs historical standards.",
                                "C4": "Explicit decision deferral ('I'll wait') pending more validation — active risk-benefit calculation."}}
    },
    # C6 단독 — 강제 반대 (ID: 1355711914811289604t, CAVES: mandatory)
    {
        "text": "They don ' t have to get the vaccine . They do not get to tell others what to do with their body .",
        "label": {"C1": 0, "C2": 0, "C4": 0, "C6": 1, "C7": 0,
                  "rationale": {"C6": "Resistance to compulsory vaccination; bodily autonomy framing against external coercion."}}
    },
    # C7 단독 — 음모론 (ID: 1400628010043195397t, CAVES: conspiracy)
    {
        "text": "The vaccine wasn ' t created for covid ... covid was created for the vaccine ...",
        "label": {"C1": 0, "C2": 0, "C4": 0, "C6": 0, "C7": 1,
                  "rationale": {"C7": "Conspiracy claim that the pandemic was deliberately engineered to justify vaccination — malicious intent assumed."}}
    },
    # C1+C6+C7 복합 — 본 연구 핵심 클러스터 (ID: 1337522336178851840t, CAVES: conspiracy mandatory side-effect)
    {
        "text": "@GovPritzker @US_FDA @pfizer We didn ' t vote for the Pharmacidal cartel . No DNA - altering toxic Frankenshots . Violation of Nuremberg Code . No COV - IDs and health ' passports . ' We do not consent .",
        "label": {"C1": 1, "C2": 0, "C4": 0, "C6": 1, "C7": 1,
                  "rationale": {"C1": "Vaccine safety concern — 'toxic Frankenshots' and 'DNA-altering' express ingredient/safety distrust.",
                                "C6": "Opposition to vaccine mandates and health passports; 'we do not consent' frames coercion resistance.",
                                "C7": "'Pharmacidal cartel' implies deliberate malicious collusion between government and pharma."}}
    },
]

FEW_SHOT_KO = [
    # C1 단독
    {
        "text": "이물질이 든 백신을 1420만 명한테 그냥 맞혔다고? 식약처는 뭐했냐. 이게 말이 됩니까.",
        "label": {"C1": 1, "C2": 0, "C4": 0, "C6": 0, "C7": 0,
                  "rationale": {"C1": "이물질 포함 백신 안전성 직접 우려, 규제기관(식약처) 불신."}}
    },
    # C2 단독
    {
        "text": "이제 코로나 끝났는데 아직도 맞으라고? 그냥 감기야. 걸려봤자 콧물만 흘리다 낫는다.",
        "label": {"C1": 0, "C2": 1, "C4": 0, "C6": 0, "C7": 0,
                  "rationale": {"C2": "질병 위험 경시(감기 수준), 접종 불필요성 판단."}}
    },
    # C4 단독
    {
        "text": "부작용 데이터가 좀 더 나오면 그때 판단하려고요. 아직 2년도 안 됐잖아요.",
        "label": {"C1": 0, "C2": 0, "C4": 1, "C6": 0, "C7": 0,
                  "rationale": {"C4": "추가 데이터 확보 후 결정 유보 — 명시적 정보 탐색·저울질."}}
    },
    # C6 단독
    {
        "text": "방역 패스는 미접종자 차별이다. 헌법 위반이야. 강제로 맞힐 권리가 어디 있냐.",
        "label": {"C1": 0, "C2": 0, "C4": 0, "C6": 1, "C7": 0,
                  "rationale": {"C6": "방역 패스(강제 접종 정책)에 대한 명시적 반대, 개인 자유 침해 프레임."}}
    },
    # C7 단독
    {
        "text": "제약사가 정부한테 로비해서 빨리 허가 받은 거지. 다 짜고 치는 고스톱. 정은경이 모를 리 없지.",
        "label": {"C1": 0, "C2": 0, "C4": 0, "C6": 0, "C7": 1,
                  "rationale": {"C7": "정부-제약사 결탁 음모 주장, 특정 인물(정은경)의 의도적 행위 지목."}}
    },
    # C1+C6+C7 복합
    {
        "text": "강제로 맞혀놓고 이물질 들어간 백신을 쓴 거잖아요. KDCA가 알면서도 묵인한 게 분명해요.",
        "label": {"C1": 1, "C2": 0, "C4": 0, "C6": 1, "C7": 1,
                  "rationale": {"C1": "이물질 백신 안전성 직접 우려.",
                                "C6": "강제 접종 비판.",
                                "C7": "KDCA의 의도적 묵인 — 악의적 의도 전제."}}
    },
]


def build_few_shot_messages(mode: str) -> list[dict]:
    examples = FEW_SHOT_KO if mode == "ko" else FEW_SHOT_EN
    messages = []
    for ex in examples:
        messages.append({"role": "user", "content": ex["text"]})
        messages.append({"role": "assistant",
                         "content": json.dumps(ex["label"], ensure_ascii=False)})
    return messages


# ── 실시간 분류 (tenacity retry) ──────────────────────────────────────────────

@retry(
    retry=retry_if_exception_type(anthropic.RateLimitError),
    wait=wait_exponential(multiplier=2, min=4, max=60),
    stop=stop_after_attempt(5),
)
def _call_api(client: anthropic.Anthropic, messages: list[dict]) -> anthropic.types.Message:
    return client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=[{
            "type": "text",
            "text": SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"},
        }],
        messages=messages,
    )


def classify_realtime(client: anthropic.Anthropic, text: str, mode: str) -> dict:
    few_shot = build_few_shot_messages(mode)
    few_shot.append({"role": "user", "content": text})

    response = _call_api(client, few_shot)
    raw = response.content[0].text.strip()

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        clean = raw.replace("```json", "").replace("```", "").strip()
        try:
            result = json.loads(clean)
        except json.JSONDecodeError:
            result = {"C1": -1, "C2": -1, "C4": -1, "C6": -1, "C7": -1,
                      "rationale": {}, "parse_error": raw}

    result["_usage"] = {
        "input_tokens":          response.usage.input_tokens,
        "output_tokens":         response.usage.output_tokens,
        "cache_creation_tokens": getattr(response.usage, "cache_creation_input_tokens", 0),
        "cache_read_tokens":     getattr(response.usage, "cache_read_input_tokens", 0),
    }
    return result


# ── Batch API 모드 ─────────────────────────────────────────────────────────────

def build_batch_request(custom_id: str, text: str, mode: str) -> dict:
    few_shot = build_few_shot_messages(mode)
    few_shot.append({"role": "user", "content": text})
    return {
        "custom_id": custom_id,
        "params": {
            "model":      MODEL,
            "max_tokens": MAX_TOKENS,
            "system": [{
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }],
            "messages": few_shot,
        },
    }


def submit_batch(client: anthropic.Anthropic, requests: list[dict]) -> str:
    batch = client.messages.batches.create(requests=requests)
    print(f"[Batch 제출] ID: {batch.id} | {len(requests)}건")
    return batch.id


def poll_batch(client: anthropic.Anthropic, batch_id: str,
               poll_interval: int = 60) -> list:
    print(f"[Batch 폴링] {batch_id}")
    while True:
        batch  = client.messages.batches.retrieve(batch_id)
        status = batch.processing_status
        counts = batch.request_counts
        print(f"  상태: {status} | "
              f"완료: {counts.succeeded} / "
              f"오류: {counts.errored} / "
              f"처리중: {counts.processing}")
        if status == "ended":
            break
        time.sleep(poll_interval)

    return list(client.messages.batches.results(batch_id))


def parse_batch_results(results: list) -> list[dict]:
    parsed = []
    for r in results:
        if r.result.type == "succeeded":
            raw = r.result.message.content[0].text.strip()
            try:
                label = json.loads(raw)
            except json.JSONDecodeError:
                clean = raw.replace("```json", "").replace("```", "").strip()
                try:
                    label = json.loads(clean)
                except json.JSONDecodeError:
                    label = {"C1": -1, "C2": -1, "C4": -1, "C6": -1, "C7": -1,
                             "rationale": {}, "parse_error": raw}
        else:
            label = {"C1": -1, "C2": -1, "C4": -1, "C6": -1, "C7": -1,
                     "rationale": {}, "batch_error": str(r.result.error)}

        label["_custom_id"] = r.custom_id
        parsed.append(label)
    return parsed


# ── 벤치마크 실행 ──────────────────────────────────────────────────────────────

def run_benchmark(client: anthropic.Anthropic, split: str,
                  sample: int | None, use_batch: bool):
    csv_path = CAVES_DIR / f"{split}.csv"   # ← 수정: _processed 제거
    if not csv_path.exists():
        raise FileNotFoundError(f"CAVES 파일 없음: {csv_path}")

    with open(csv_path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if sample:
        random.seed(42)
        rows = random.sample(rows, min(sample, len(rows)))

    print(f"[벤치마크] {split} {len(rows)}건 | Batch={use_batch}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    if use_batch:
        requests = [build_batch_request(row["ID"], row["text"], "en") for row in rows]
        batch_id = submit_batch(client, requests)
        (OUTPUT_DIR / f"caves_{split}_{ts}_batch_id.txt").write_text(batch_id)

        parsed  = parse_batch_results(poll_batch(client, batch_id))
        truth   = {row["ID"]: row for row in rows}
        out_path = OUTPUT_DIR / f"caves_{split}_{ts}_batch.jsonl"

        with open(out_path, "w", encoding="utf-8") as f:
            for p in parsed:
                cid = p.pop("_custom_id")
                row = truth.get(cid, {})
                f.write(json.dumps({
                    "ID":          cid,
                    "pred_C1":     p.get("C1", -1),  "true_C1": int(row.get("C1", 0)),
                    "pred_C2":     p.get("C2", -1),  "true_C2": int(row.get("C2", 0)),
                    "pred_C4":     p.get("C4", -1),  "true_C4": int(row.get("C4", 0)),
                    "pred_C6":     p.get("C6", -1),  "true_C6": int(row.get("C6", 0)),
                    "pred_C7":     p.get("C7", -1),  "true_C7": int(row.get("C7", 0)),
                    "rationale":   p.get("rationale"),
                    "parse_error": p.get("parse_error"),
                    "batch_error": p.get("batch_error"),
                }, ensure_ascii=False) + "\n")

    else:
        total    = {"input": 0, "output": 0, "cache_create": 0, "cache_read": 0}
        out_path = OUTPUT_DIR / f"caves_{split}_{ts}.jsonl"

        with open(out_path, "w", encoding="utf-8") as f:
            for i, row in enumerate(rows, 1):
                result = classify_realtime(client, row["text"], "en")
                usage  = result.pop("_usage", {})
                f.write(json.dumps({
                    "ID":          row["ID"],
                    "pred_C1":     result.get("C1", -1),  "true_C1": int(row.get("C1", 0)),
                    "pred_C2":     result.get("C2", -1),  "true_C2": int(row.get("C2", 0)),
                    "pred_C4":     result.get("C4", -1),  "true_C4": int(row.get("C4", 0)),
                    "pred_C6":     result.get("C6", -1),  "true_C6": int(row.get("C6", 0)),
                    "pred_C7":     result.get("C7", -1),  "true_C7": int(row.get("C7", 0)),
                    "rationale":   result.get("rationale"),
                    "parse_error": result.get("parse_error"),
                }, ensure_ascii=False) + "\n")
                _accumulate(total, usage)
                if i % 50 == 0:
                    print(f"  {i}/{len(rows)} | 캐시 히트: {total['cache_read']} tok")
                time.sleep(0.3)

        _print_cost_summary(total)

    print(f"[완료] {out_path}")


# ── 한국어 분류 실행 ───────────────────────────────────────────────────────────

def run_korean(client: anthropic.Anthropic, group: str | None, use_batch: bool):
    con = sqlite3.connect(NAVER_DB)
    cur = con.cursor()
    if group:
        cur.execute(
            "SELECT post_id, content, keyword_group FROM posts WHERE keyword_group = ?",
            (group,)
        )
    else:
        cur.execute("SELECT post_id, content, keyword_group FROM posts")
    rows = cur.fetchall()
    con.close()

    print(f"[한국어 분류] {len(rows)}건 | Batch={use_batch}"
          + (f" | 그룹: {group}" if group else ""))
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ts     = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = f"_{group}" if group else "_all"

    if use_batch:
        requests = [
            build_batch_request(pid, content or "", "ko")
            for pid, content, _ in rows
        ]
        batch_id = submit_batch(client, requests)
        (OUTPUT_DIR / f"naver{suffix}_{ts}_batch_id.txt").write_text(batch_id)

        parsed    = parse_batch_results(poll_batch(client, batch_id))
        group_map = {pid: kg for pid, _, kg in rows}
        out_path  = OUTPUT_DIR / f"naver{suffix}_{ts}_batch.jsonl"

        with open(out_path, "w", encoding="utf-8") as f:
            for p in parsed:
                pid = p.pop("_custom_id")
                f.write(json.dumps({
                    "post_id":       pid,
                    "keyword_group": group_map.get(pid),
                    "pred_C1":       p.get("C1", -1),
                    "pred_C2":       p.get("C2", -1),
                    "pred_C4":       p.get("C4", -1),
                    "pred_C6":       p.get("C6", -1),
                    "pred_C7":       p.get("C7", -1),
                    "rationale":     p.get("rationale"),
                    "parse_error":   p.get("parse_error"),
                    "batch_error":   p.get("batch_error"),
                }, ensure_ascii=False) + "\n")

    else:
        total    = {"input": 0, "output": 0, "cache_create": 0, "cache_read": 0}
        out_path = OUTPUT_DIR / f"naver{suffix}_{ts}.jsonl"

        with open(out_path, "w", encoding="utf-8") as f:
            for i, (pid, content, kw_group) in enumerate(rows, 1):
                result = classify_realtime(client, content or "", "ko")
                usage  = result.pop("_usage", {})
                f.write(json.dumps({
                    "post_id":       pid,
                    "keyword_group": kw_group,
                    "pred_C1":       result.get("C1", -1),
                    "pred_C2":       result.get("C2", -1),
                    "pred_C4":       result.get("C4", -1),
                    "pred_C6":       result.get("C6", -1),
                    "pred_C7":       result.get("C7", -1),
                    "rationale":     result.get("rationale"),
                    "parse_error":   result.get("parse_error"),
                }, ensure_ascii=False) + "\n")
                _accumulate(total, usage)
                if i % 100 == 0:
                    print(f"  {i}/{len(rows)} | 캐시 히트: {total['cache_read']} tok")
                time.sleep(0.3)

        _print_cost_summary(total)

    print(f"[완료] {out_path}")


# ── 유틸 ──────────────────────────────────────────────────────────────────────

def _accumulate(total: dict, usage: dict):
    total["input"]        += usage.get("input_tokens", 0)
    total["output"]       += usage.get("output_tokens", 0)
    total["cache_create"] += usage.get("cache_creation_tokens", 0)
    total["cache_read"]   += usage.get("cache_read_tokens", 0)


def _print_cost_summary(tokens: dict):
    # Haiku 4.5: input $1.00/1M, output $5.00/1M,
    #            cache write $1.25/1M, cache read $0.10/1M
    ic = tokens["input"]        / 1_000_000 * 1.00
    oc = tokens["output"]       / 1_000_000 * 5.00
    wc = tokens["cache_create"] / 1_000_000 * 1.25
    rc = tokens["cache_read"]   / 1_000_000 * 0.10
    total = ic + oc + wc + rc
    saved = tokens["cache_read"] / 1_000_000 * (1.00 - 0.10)

    print(f"\n[비용 요약]")
    print(f"  입력 토큰:    {tokens['input']:>9,}  →  ${ic:.4f}")
    print(f"  출력 토큰:    {tokens['output']:>9,}  →  ${oc:.4f}")
    print(f"  캐시 생성:    {tokens['cache_create']:>9,}  →  ${wc:.4f}")
    print(f"  캐시 읽기:    {tokens['cache_read']:>9,}  →  ${rc:.4f}")
    print(f"  ──────────────────────────────────")
    print(f"  총 비용:                    ${total:.4f}")
    print(f"  캐싱 절감:                  ${saved:.4f}")


# ── 메인 ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode",   choices=["en", "ko"], required=True)
    parser.add_argument("--split",  default="test", choices=["train", "val", "test"])
    parser.add_argument("--sample", type=int, default=None, help="샘플 수 (프롬프트 탐색용)")
    parser.add_argument("--group",  default=None,
                        help="한국어 그룹 필터 (FM_Direct / Court / Chronic)")
    parser.add_argument("--batch",  action="store_true",
                        help="Anthropic Batch API 사용 (50%% 할인, rate limit 무관)")
    args = parser.parse_args()

    client = anthropic.Anthropic()

    if args.mode == "en":
        run_benchmark(client, args.split, args.sample, args.batch)
    else:
        run_korean(client, args.group, args.batch)


if __name__ == "__main__":
    main()
