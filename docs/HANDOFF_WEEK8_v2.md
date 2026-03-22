# Infovail-IQ — HANDOFF Week 8 v2

> **작성일**: 2026-03-20 | **다음 세션**: 2026-03-21 이후
> **현재 Phase**: Phase 3 Week 8 2차

---

## 1. 오늘 세션(2026-03-20) 완료 사항

| 작업 | 결과 |
|------|------|
| Figure 2 생성 | `outputs/figures/figure2_7C_prevalence_v2.png` (300dpi) ✅ |
| E2 프레이밍 확정 | SBS 보도 주, KDCA 항소 부. "vaccine-associated myocardial infarction" 표현 제거 ✅ |
| `discussion_draft_v0_5.md` 저장 | `poc1/docs/discussion_draft_v0_5.md` ✅ |
| `POC_SCENARIO.md` v0.2.1 | 영문 E2 기술 수정 (루트) ✅ |
| `README.md` 업데이트 | Current PoC 섹션 → 두 이벤트 구조 ✅ |
| `CLAUDE_PROJECT_SETUP.md` 갱신 | Phase 3 기준, E2 정의 명시, 7,093건 반영 ✅ |

---

## 2. 확정된 E2 표현 (모든 문서 통일 기준)

**Figure caption용:**
> E2: SBS broadcast on court-recognized causal link between COVID-19 vaccination and myocardial infarction death (Mar 2)

**Discussion 본문용:**
> E2: SBS news broadcast (Mar 2) reporting the court's recognition of a causal link between COVID-19 vaccination and myocardial infarction death, with KDCA's subsequent appeal as secondary context

**discourse specificization 절 핵심 문장:**
> The SBS broadcast (March 2) did not introduce a new allegation — it translated an existing judicial finding into mass-media framing, converting a legal outcome into a publicly legible causal claim: COVID-19 vaccines cause myocardial infarction.

---

## 3. Figure 2 데이터 (확정)

### 3구간 × 그룹별 C1/C4/C6/C7 prevalence (%)

| Group | Dim | Pre-E1 | E1→E2 | Post-E2 | Sig (Pre vs Post) |
|-------|-----|--------|-------|---------|-------------------|
| FM_Direct (n=51/1225/752) | C1 | 21.6 | 75.0 | 68.9 | *** |
| | C4 | 3.9 | 4.2 | 1.7 | ns |
| | C6 | 3.9 | 8.2 | 6.2 | ns |
| | C7 | 21.6 | 23.4 | 25.9 | ns |
| Court (n=1417/276/719) | C1 | 6.0 | 13.0 | 58.6 | *** |
| | C4 | 0.7 | 0.7 | 5.4 | *** |
| | C6 | 4.6 | 3.3 | 2.6 | * |
| | C7 | 39.6 | 12.3 | 14.3 | *** |
| Chronic (n=833/840/980) | C1 | 15.7 | 43.0 | 47.9 | *** |
| | C4 | 3.6 | 5.7 | 5.0 | ns |
| | C6 | 2.6 | 7.0 | 4.1 | ns |
| | C7 | 16.4 | 18.7 | 10.4 | *** |

> * p<0.05, *** p<0.001 (Pre-E1 vs Post-E2; Fisher's exact or χ² test)
> C2 Complacency 제외 (전 그룹 <1%)

---

## 4. 내일(3.21) 즉시 할 일

### 최우선 (논문 critical path)

1. **최종 수집 실행**
   ```
   cd C:\infovail-iq\poc1
   uv run python scripts/collect_all.py --start-date 2026-03-15 --end-date 2026-03-21
   ```
   → 수집 후 7,093건 + 보완분 최종 DB 확정

2. **코더 B 결과 수합**
   → 파일 형식 확인 즉시 `calc_kappa.py` 작성
   → Cohen's kappa ≥ 0.80 확인 → Phase 2 게이트 통과

3. **Gold standard 교차 검증 → 한국어 F1 산출**
   → `evaluation/` 디렉토리 활용

4. **Discussion `[XX]` placeholder 채우기**
   → kappa 값, 한국어 F1 → `discussion_draft_v0_5.md` 업데이트

---

## 5. 현재 파일 위치 요약

| 파일 | 경로 |
|------|------|
| DB (최신) | `poc1/data/processed/naver_posts.db` (7,093건) |
| JSONL (분류결과) | `poc1/data/exports/labeled/naver_all_20260314_merged.jsonl` |
| Figure 2 | `poc1/outputs/figures/figure2_7C_prevalence_v2.png` |
| Discussion draft | `poc1/docs/discussion_draft_v0_5.md` |
| Gold standard | `poc1/evaluation/` (확인 필요) |

---

## 6. Week 8 잔여 체크리스트 상태

```
Week 8 2차:
[ ] 최종 수집 (03-21)                          ← 내일
[ ] 코더 B 결과 수합                            ← 내일
[ ] calc_kappa.py → Cohen's kappa              ← 내일 (코더B 결과 확인 후)
[ ] kappa ≥ 0.80 → Phase 2 게이트 통과         ← 내일
[ ] Gold standard × merged.jsonl 교차검증       ← 내일
[ ] Discussion [XX] placeholder 채우기          ← 내일
[x] Figure 2 완성                               ✅ 오늘

Week 8 추가 (3.21~3.28):
[ ] 3.21~3.28 정치·사법 동향 확인 (Discussion 4.7 추가 여부)
[ ] 민주당 3.24 피해자 단체 간담회 정식 명칭 확인 → BOOK_MEMO
[ ] 특별법 개정안 정식 발의 여부 확인 → BOOK_MEMO
```

---

## 7. 다음 세션 시작 방법

새 세션에서 이 문서를 참조하거나 아래 한 줄로 시작:

> "HANDOFF_WEEK8_v2 기준으로 이어서 진행해. 오늘은 최종 수집 실행하고, 코더 B 결과 받으면 calc_kappa.py 작성할 거야."
