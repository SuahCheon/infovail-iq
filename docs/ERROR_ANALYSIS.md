# Error Analysis — v1.1.0 Full Test Set (1,846 samples)

> **Date**: 2026-03-10
> **Prompt**: v1.1.0 (최종 채택) | **Model**: claude-haiku-4-5-20251001
> **Output**: `poc1/data/exports/labeled/caves_test_20260310_220438_batch.jsonl`
>
> Note: v1.2.0~v1.3.0 프롬프트 최적화는 전체 test set에서 역효과 확인 후 폐기.
> 본 분석은 최종 채택된 v1.1.0 결과 기준이며, v1.3.0 분석도 참고용으로 병기.

---

## 1. Overall Performance

| Dimension | Precision | Recall | F1    | TP   | FP  | FN  | Support |
|-----------|-----------|--------|-------|------|-----|-----|---------|
| C1        | 0.956     | 0.837  | 0.893 | 1370 | 63  | 266 | 1636    |
| C2        | 0.493     | 0.710  | 0.582 | 103  | 106 | 42  | 145     |
| C4        | 0.320     | 0.508  | 0.393 | 150  | 319 | 145 | 295     |
| C6        | 0.553     | 0.796  | 0.653 | 125  | 101 | 32  | 157     |
| C7        | 0.290     | 0.660  | 0.403 | 142  | 347 | 73  | 215     |
| **Macro** |           |        |**0.585**|    |     |     |         |

---

## 2. C4 (Calculation) Error Analysis

### 2.1 C4 False Negatives (145 cases)

v1.1.0에서 C4 FN은 145건 (v1.3.0의 217건보다 적음 — "rushed=C1 only" 제한 없이
모델이 rushed 트윗의 일부를 자연스럽게 C4로 분류).

**Root Cause: CAVES-to-7C Mapping Divergence**

The CAVES gold standard maps `rushed` to C4 (Calculation), treating concern about
insufficient testing as evidence of risk-benefit weighing. However, many `rushed` tweets
express **distrust** (C1) without explicit decision deferral language:

> "It's NOT a vaccine, the 'jab' is a gene therapy trial which concludes on 31/01/23"
> — Distrust of approval process, no personal decision deferral expressed.

> "Immensely irresponsible of you, Jake, to feed the idea that the Pfizer vaccine
> is going to actually be ready large scale any time soon."
> — Criticism of timeline, no information-seeking intent.

**Discussion framing**: This divergence reflects a legitimate definitional ambiguity
in the 7C framework. Whether "rushed development concern" constitutes active
Calculation (C4) or passive Confidence loss (C1) depends on operationalization.
The model naturally classifies some rushed tweets as C4 (when decision deferral
language is present) and others as C1 only, which is a reasonable interpretation.

Note: v1.2.0~v1.3.0 attempted to explicitly restrict "rushed = C1 only", which
increased C4 FN from 145 to 217 — demonstrating that the model's natural
interpretation was already closer to optimal than the manual restriction.

### 2.2 C4 False Positives (319 cases) — by CAVES category

v1.1.0은 C4 제한 없이 FP 319건 (v1.3.0의 125건보다 많음). 이는 recall-precision
trade-off: v1.1.0은 recall 0.508로 높지만 precision 0.320으로 낮음.

| CAVES Category | Count | Interpretation |
|---------------|-------|----------------|
| side-effect   | ~120  | Rhetorical questions misread as information-seeking |
| ineffective   | ~100  | Conditional language misread as decision deferral |
| pharma        | ~40   | Critical questioning misread |

**Pattern**: The model over-interprets questioning or conditional language in C1 tweets
as C4 information-seeking:

> "Show me the study that proves that." (side-effect)
> — Rhetorical challenge, not genuine information request.

> "I'd rather have the traditional type" (side-effect)
> — Preference statement, not decision deferral pending more data.

> "Let me know when there is a vaccine that prevents transmission" (ineffective)
> — Conditional acceptance, but the condition is vaccine performance, not personal
> information-seeking behavior.

---

## 3. C7 (Conspiracy) Error Analysis

### 3.1 C7 False Positives (347 cases) — by CAVES category

v1.1.0에서 C7 FP=347 (v1.3.0의 320과 큰 차이 없음 — C7 과잉분류는
프롬프트 최적화로 해소 불가능한 구조적 문제).

| CAVES Category | Count (approx) | % of FP | Interpretation |
|---------------|-------|---------|----------------|
| side-effect   | ~140  | ~40%    | Strong anger → conspiracy |
| pharma        | ~110  | ~32%    | Financial motive → conspiracy |
| rushed        | ~55   | ~16%    | Distrust intensity → conspiracy |
| mandatory     | ~40   | ~12%    | Coercion framing → conspiracy |

**Root Cause: C1-C7 Boundary Ambiguity**

The model systematically conflates **strong distrust** (C1) with **conspiracy** (C7).
Three dominant FP patterns:

**Pattern A — Financial motive = conspiracy (pharma, ~100 cases)**
> "They can't make much money from hydroxychloroquine but they can make billions
> from pushing a vaccine — it's just common sense."
>
> Model rationale: "coordinated financial conspiracy to promote vaccines over alternatives"
> Gold: pharma (C1 only) — financial criticism ≠ deliberate conspiracy.

**Pattern B — Strong emotion = conspiracy (side-effect, ~133 cases)**
> Tweets expressing intense anger about adverse events are interpreted as implying
> deliberate harm when the language merely reflects distrust intensity.

**Pattern C — Implied vs. explicit malicious intent (~50 cases)**
> "How can J&J already be working on a vaccine in January???"
>
> Model rationale: "implies coordinated prior knowledge, deliberate concealment"
> Gold: pharma (C1 only) — suspicion is not the same as conspiracy assertion.

**Discussion framing**: The C7 FP problem reveals that the model interprets
*intensity of distrust* as evidence of *conspiracy belief*. The linguistic boundary
between "I don't trust them" (C1) and "they are deliberately deceiving us" (C7)
is often ambiguous in short social media text.

### 3.2 C7 False Negatives (73 cases) — by CAVES category

| CAVES Category | Count | % of FN | Interpretation |
|---------------|-------|---------|----------------|
| **political** | **~60**| **~82%** | Model misses implicit C7 in political criticism |
| conspiracy    | ~13   | ~18%   | Explicit conspiracy missed |

**Root Cause: `political` → C7 Mapping Underdetection**

CAVES maps `political` to C1+C7, but the model classifies most political tweets
as C1 only. Political conspiracy language tends to be **implicit** rather than explicit:

> "How many more times will MPs let a small cabal of Ministers + the PM drag our
> civil liberties through the mud?"
>
> "cabal" implies coordinated malicious intent, but the model requires more
> explicit conspiracy language per our v1.2.0+ threshold instruction.

**Discussion framing**: Political vaccine hesitancy occupies a gray zone between
institutional distrust (C1) and conspiracy belief (C7). The model's stricter
threshold (requiring explicit malicious-intent language) systematically under-detects
C7 in politically-framed tweets where conspiracy is implied through words like
"cabal", "agenda", or "cover-up" without overt conspiracy claims.

---

## 4. Summary of Error Patterns

| Issue | Dimension | Direction | Count | Root Cause |
|-------|-----------|-----------|-------|------------|
| Strong distrust → conspiracy | C7 | FP | 347 | Intensity-threshold confusion |
| Rhetorical questions → C4 | C4 | FP | 319 | Over-sensitive information-seeking detection |
| rushed partial miss | C4 | FN | 145 | Mapping divergence (definitional) |
| Political conspiracy implicit | C7 | FN | 73 | Implicit C7 language in political tweets |

### Key Insight for Discussion

The two largest error sources (C4 FP=319, C7 FP=347) reflect **inherent limitations
of single-pass few-shot classification** for distinguishing adjacent 7C dimensions
(C1↔C4, C1↔C7) in short social media text.

Prompt engineering attempts (v1.2.0~v1.3.0) to address these issues were
counterproductive on the full test set: v1.1.0 macro F1 0.585 > v1.3.0 0.569.
The lesson: **200-sample optimization with a fixed seed can overfit to sample
characteristics and degrade overall performance**.

### Implications for Korean Phase

1. C1↔C7 boundary ambiguity will likely persist in Korean data (강한 분노 vs 음모론)
2. C4 mapping should be re-evaluated: Korean data uses 7C codebook directly,
   avoiding the CAVES→7C mapping issue entirely
3. The `political` category is English-specific (US/UK political context);
   Korean political hesitancy may have different linguistic markers
