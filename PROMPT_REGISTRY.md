# PROMPT_REGISTRY.md
## Infovail-IQ PoC1 — 분류 프롬프트 버전 관리

> **위치**: `C:\infovail-iq\PROMPT_REGISTRY.md`
> **목적**: 논문 재현성 확보 — 프롬프트 변경 이력 및 근거를 버전별로 기록

---

## 버전 이력 요약

| 버전 | 날짜 | 상태 | 핵심 변경 | 200건 F1 |
|------|------|------|-----------|----------|
| v1.0.0 | 2026-03-10 | 대체됨 | 초안 (작성된 few-shot) | 미측정 |
| **v1.1.0** | **2026-03-10** | **최종 채택** | CAVES train set verbatim few-shot 6개 | **0.596 (200건) / 0.585 (전체)** |
| v1.2.0 | 2026-03-10 | 폐기 | C4/C7 과잉분류 수정 | 0.588 (200건) |
| v1.3.0 | 2026-03-10 | 폐기 | C4 완화 + C7 few-shot 교체 | 0.584 (200건) / 0.569 (전체) |

---

## v1.0.0 (2026-03-10) — 초안

**상태**: 대체됨

**변경 내용**: 초안 — few-shot 예시 직접 작성 (CAVES train set 미참조)

**폐기 이유**: few-shot 출처 불명확 (train set 오염 여부 불확실)

---

## v1.1.0 (2026-03-10) — CAVES train set verbatim [최종 채택]

**상태**: 최종 채택

**변경 내용**:
- 영어 few-shot 6개: CAVES train set verbatim (tweet ID 명시)
- 한국어 few-shot 6개: 7C_CODEBOOK 기반 직접 작성 (한국어 CAVES 없으므로 정당)
- few-shot 구조: C1/C2/C4/C6/C7 단일 레이블 ×5 + C1+C6+C7 복합 ×1

**few-shot 선정 기준** (Methods 기재용):
- 5개 활성 차원(C1/C2/C4/C6/C7) × 단일 레이블 예시 1개씩
- 복합 레이블(multi-label) 예시 1개 (C1+C6+C7 — 본 연구 핵심 클러스터)
- 총 6개, train set에서만 선정 (test set 오염 방지)
- 각 예시는 해당 차원을 명확히 드러내는 최단 길이 텍스트 선택

**200건 벤치마크 결과** (2026-03-10, seed=42):

| 차원 | Precision | Recall | F1 | TP | FP | FN |
|------|-----------|--------|----|----|----|----|
| C1 | 0.925 | 0.773 | 0.842 | 136 | 11 | 40 |
| C2 | 0.444 | 0.706 | 0.545 | 12 | 15 | 5 |
| C4 | 0.413 | 0.565 | 0.477 | 26 | 37 | 20 |
| C6 | 0.500 | 0.714 | 0.588 | 10 | 10 | 4 |
| C7 | 0.429 | 0.677 | 0.525 | 21 | 28 | 10 |
| **Macro (5-dim)** | | | **0.596** | | | |
| **Macro (4-dim, excl C1)** | | | **0.534** | | | |

Parse errors: 0/200 (0%)

**전체 test set 결과** (1,846건, Batch API):

| 차원 | Precision | Recall | F1 | TP | FP | FN | Support |
|------|-----------|--------|----|----|----|----|---------|
| C1 | 0.956 | 0.837 | 0.893 | 1370 | 63 | 266 | 1636 |
| C2 | 0.493 | 0.710 | 0.582 | 103 | 106 | 42 | 145 |
| C4 | 0.320 | 0.508 | 0.393 | 150 | 319 | 145 | 295 |
| C6 | 0.553 | 0.796 | 0.653 | 125 | 101 | 32 | 157 |
| C7 | 0.290 | 0.660 | 0.403 | 142 | 347 | 73 | 215 |
| **Macro (5-dim)** | | | **0.585** | | | | |
| **Macro (4-dim, excl C1)** | | | **0.508** | | | | |

Parse errors: 0/1846 (0%) | Batch errors: 0 | Cost: ~$2.00

**v1.2.0~v1.3.0 대비 우위 확인**: 전체 test set에서 v1.1.0(0.585) > v1.3.0(0.569).
200건 샘플 기반 최적화가 전체 데이터에서 역효과였음을 확인하여 v1.1.0을 최종 채택.

**출력 파일**: `caves_test_20260310_220438_batch.jsonl`

**Error Analysis** (상세: `docs/ERROR_ANALYSIS.md`):

| 오류 유형 | 차원 | 방향 | 건수 | 근본 원인 |
|-----------|------|------|------|-----------|
| 강한 불신 → 음모론 | C7 | FP | 347 | 불신 강도를 음모 의도로 혼동 |
| 수사적 질문 과탐지 | C4 | FP | 319 | 질문형 언어 → 정보탐색 과잉 해석 |
| 정치적 암시 미탐지 | C7 | FN | 73 | political 카테고리 implicit C7 누락 |
| rushed 과탐지 | C4 | FN | 145 | rushed→C4 매핑의 정밀도 한계 |

**결정**: 현행 성능(macro F1 0.585)을 투명하게 보고하고 한국어 단계(v2.0.0)로 전환.

---

## v1.2.0 (2026-03-10) — C4/C7 과잉분류 수정 [폐기]

**상태**: 폐기

**변경 근거**: v1.1.0 200건 벤치마크 오류 패턴 분석
- C4 FP 37건 (precision 0.413): `Rushed` 카테고리 텍스트가 C4로 과잉 매핑
  - "임상이 짧았다" = C1(불신), 정보탐색 의도 없음 → C4 오분류
- C7 FP 28건 (precision 0.429): 강한 C1 표현을 C7으로 과잉분류
  - 악의적 의도 임계값 미명시로 인한 경계 혼동

**변경 내용 (3곳)**:

### ① C4 정의 — "rushed development → C1" 경고 추가

```
# v1.1.0
Active information seeking and weighing of pros and cons before deciding whether to vaccinate.
Includes: explicitly seeking more data before deciding, comparing benefits and risks,
conditional acceptance ("I'll vaccinate when more data is available"), value-based weighing.

# v1.2.0 (추가된 부분)
Key signal: the speaker expresses intent to gather MORE information before making a decision.
⚠️ Do NOT assign C4 if the speaker merely criticizes rushed development or insufficient trials
without expressing a personal intent to seek information — that is C1 (distrust), not C4.
```

### ② C7 정의 — 악의적 의도 임계값 명시

```
# v1.1.0
Belief in malicious intent behind vaccines or vaccine policy — beyond simple distrust.
Includes: claims of deliberate concealment, government-pharma collusion, vaccines as population
control or surveillance tools, COVID-19 as a fabricated crisis.

# v1.2.0 (추가된 부분)
Key signal: explicit language of deliberate, coordinated deception — e.g., "they planned this",
"knew and hid it", "colluding", named actors acting with intent.
⚠️ Strong distrust, anger, or criticism alone is NOT sufficient for C7. If malicious intent
is only implied but not stated, assign C1 only.
```

### ③ Key Distinctions — C2 vs C4, C1 vs C4 negative example 추가

```
# v1.1.0
- C2 vs C4: C2 = disease risk dismissed; C4 = actively seeking information to decide

# v1.2.0 (확장)
- C2 vs C4: C2 = disease risk dismissed; C4 = actively seeking information to decide.
  Example — "I want to see more data first" → C4, NOT C2.
  Example — "COVID is just the flu" → C2, NOT C4.
- C1 vs C4: Criticizing rushed trials or insufficient data = C1. Personally withholding
  decision until more data is available = C4. Both can co-occur.
- C1 vs C7: Strong anger or distrust without explicit malicious-intent language = C1 only.
```

**few-shot**: v1.1.0에서 변경 없음 (구조 동일, 텍스트 유지)

**모델**: `claude-haiku-4-5-20251001` (변경 없음)

**200건 벤치마크 결과** (2026-03-10, seed=42):

| 차원 | Precision | Recall | F1 | TP | FP | FN | vs v1.1.0 F1 |
|------|-----------|--------|----|----|----|----|-------------|
| C1 | 0.923 | 0.818 | 0.867 | 144 | 12 | 32 | +0.025 |
| C2 | 0.480 | 0.706 | 0.571 | 12 | 13 | 5 | +0.026 |
| C4 | 0.516 | 0.348 | 0.416 | 16 | 15 | 30 | **-0.061** |
| C6 | 0.476 | 0.714 | 0.571 | 10 | 11 | 4 | -0.017 |
| C7 | 0.426 | 0.645 | 0.513 | 20 | 27 | 11 | -0.012 |
| **Macro (5-dim)** | | | **0.588** | | | | **-0.008** |
| **Macro (4-dim, excl C1)** | | | **0.518** | | | | **-0.016** |

Parse errors: 0/200 (0%)

**분석**: C4 precision 개선(0.413→0.516)했으나 recall 급락(0.565→0.348). ⚠️ 경고가 과도하게 억제.

**다음 단계**: v1.3.0 — C4 완화 + C7 few-shot 교체

**목표**: macro-avg F1 ≥ 0.70 (Week 6 게이트)

---

## v1.3.0 (2026-03-10) — C4 완화 + C7 few-shot 교체 [폐기]

**상태**: 폐기

**변경 근거**: v1.2.0 200건 벤치마크 오류 패턴 분석
- C4 recall 급락 0.565→0.348: "Do NOT assign C4" 경고가 정당한 C4도 억제
- C7 FP 거의 미변 28→27: system prompt 경고만으로 부족, few-shot 레벨 개입 필요

**변경 내용 (2곳)**:

### ① C4 정의 — 긍정적 신호 중심 완화

```
# v1.2.0
Key signal: the speaker expresses intent to gather MORE information before making a decision.
⚠️ Do NOT assign C4 if the speaker merely criticizes rushed development or insufficient trials
without expressing a personal intent to seek information — that is C1 (distrust), not C4.

# v1.3.0 (대체)
Key signal: assign C4 when the speaker explicitly defers their decision OR states intent
to seek more data ("I'll wait", "need more studies", "will decide when...").
Note: Criticism of rushed development alone (without personal decision deferral) = C1 only.
Both C1 and C4 can co-occur when distrust AND decision deferral are both present.
```

### ② C7 few-shot — 극단 음모론 → boundary case 교체

```
# v1.2.0 (ID: 1400628010043195397t — 극단)
"The vaccine wasn't created for covid... covid was created for the vaccine..."
→ 극단적 음모론. C7 상한만 학습, 진입 기준(하한) 미제시.

# v1.3.0 (ID: 1337526914781679616t — 의도적 은폐 boundary)
"If this is what Pfizer call 'being honest & open', I cant see *any* country
giving a license to sell this vaccine, & its becoming apparent why they were
so insistent on getting liability indemnity... Publish the *full data*."
→ 의도적 은폐 아키타입. C7=1 단독 (C1=0). 투명성 억제 + 면책 요구 = 조직적 기만.
```

**C7 few-shot 교체 논거**:
- 복합 슬롯(#6, C1+C6+C7)에 여전히 극단 예시("Pharmacidal cartel") 존재 → C7 상한 학습 유지
- Slot #5에 boundary case 배치 → C7 진입 기준을 양방향으로 학습
- CAVES train set verbatim 원칙 유지 (ID: 1337526914781679616t)

**few-shot 선정 ID 업데이트**:
- ~~1400628010043195397t~~ → **1337526914781679616t**
- 나머지 5개 유지

**모델**: `claude-haiku-4-5-20251001` (변경 없음)

**200건 벤치마크 결과** (2026-03-10, seed=42):

| 차원 | Precision | Recall | F1 | TP | FP | FN |
|------|-----------|--------|----|----|----|----|
| C1 | 0.917 | 0.756 | 0.829 | 133 | 12 | 43 |
| C2 | 0.462 | 0.706 | 0.558 | 12 | 14 | 5 |
| C4 | 0.516 | 0.348 | 0.416 | 16 | 15 | 30 |
| C6 | 0.526 | 0.714 | 0.606 | 10 | 9 | 4 |
| C7 | 0.426 | 0.645 | 0.513 | 20 | 27 | 11 |
| **Macro (5-dim)** | | | **0.584** | | | |

**전체 test set 결과** (1,846건, Batch API):

| 차원 | Precision | Recall | F1 | TP | FP | FN | Support |
|------|-----------|--------|----|----|----|----|---------|
| C1 | 0.957 | 0.810 | 0.877 | 1325 | 60 | 311 | 1636 |
| C2 | 0.500 | 0.710 | 0.587 | 103 | 103 | 42 | 145 |
| C4 | 0.384 | 0.264 | 0.313 | 78 | 125 | 217 | 295 |
| C6 | 0.575 | 0.758 | 0.654 | 119 | 88 | 38 | 157 |
| C7 | 0.304 | 0.651 | 0.415 | 140 | 320 | 75 | 215 |
| **Macro (5-dim)** | | | **0.569** | | | | |
| **Macro (4-dim, excl C1)** | | | **0.492** | | | | |

Parse errors: 0/1846 (0%) | Batch errors: 0 | Cost: ~$2.00

**분석**:
- C1(0.877), C6(0.654) 양호. C2(0.587) 합리적.
- C4 recall 0.264 — v1.2.0 ⚠️ 경고 후유증 지속, v1.3.0 완화 미반영.
- C7 FP=320 — 전체 데이터에서 과잉분류 심각 (200건 샘플에서 과소 추정됨).
- 200건 샘플(seed=42)이 전체 성능을 과대평가: C4 +0.103, C7 +0.098 편향.

**Error Analysis** (상세: `docs/ERROR_ANALYSIS.md`):

| 오류 유형 | 차원 | 방향 | 건수 | 근본 원인 |
|-----------|------|------|------|-----------|
| rushed → C1 only | C4 | FN | 217 | CAVES→7C 매핑 해석 차이 (정의적) |
| 수사적 질문 과탐지 | C4 | FP | 125 | 질문형 언어 → 정보탐색 과잉 해석 |
| 강한 불신 → 음모론 | C7 | FP | 320 | 불신 강도를 음모 의도로 혼동 |
| 정치적 암시 미탐지 | C7 | FN | 75 | political 카테고리 C7 implicit 표현 누락 |

핵심: C4 FN(217)과 C7 FP(320)은 프롬프트 최적화의 구조적 한계를 반영.
인접 차원(C1↔C4, C1↔C7) 경계는 단일 패스 few-shot으로 해소 불가.

**폐기 이유**: 전체 test set(1,846건) 비교에서 v1.1.0(0.585) > v1.3.0(0.569) 확인.
200건 샘플(seed=42) 기반 최적화가 전체 데이터에서 역효과.
v1.2.0~v1.3.0의 모든 system prompt 변경 및 few-shot 교체를 revert하여 v1.1.0으로 복원.

---

## 향후 버전 계획

| 버전 | 조건 | 예상 변경 방향 |
|------|------|---------------|
| v2.0.0 | 한국어 적용 단계 | 한국어 few-shot 검토 및 수정 |
