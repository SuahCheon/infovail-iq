# HANDOFF — 다음 세션 시작용

> **작성일**: 2026-03-29 | **기준**: PROJECT_PLAN v0.16.0
> **오늘 완료**: Figure 2/3 재생성(3,010건) + political amplification 해석 수정 + References 완성(11개) + Figure 구조 분석 + Figure 3B→3 본문 수정 + Stage 2 필터 숫자 검증

---

## 1. 다음 세션 최우선 작업

### 🔴 Step 1. ISoP 2026 공식 가이드라인 확인 → abstract format 조정
- ISoP Global Meeting 2026 (Costa Rica) 공식 사이트에서 abstract 제출 가이드라인 확인
- **현재 파일**: `docs/isop2026_abstract_v0_1.md`
- 가이드라인 확인 후 word count, section 구조, submission 포맷 조정
- **마감: 2026-04-20**
- "under review" 상태도 ISoP 규정상 허용 확인됨

### 🟡 Step 2. Figure 1 (pipeline flowchart) 신규 생성
- **배경**: JMIR Infodemiology 관행상 Figure 1부터 순차 번호 요구
- **현재**: 원고에 Figure 2, Figure 3만 있음 (Figure 1 없음)
- **권고**: 3-stage filtering → LLM classification pipeline flowchart를 Figure 1으로 신규 생성
- **스펙**: Section 5 참조 (숫자 검증 완료)
- 생성 시 `manuscript_v0_5_merged.md`의 Methods 2.3 본문 마지막 문장에 "(Figure 1)" 참조 추가 필요
- **대안**: Figure 1 없이 투고도 가능 (editor 지적 리스크 감수). 선택 필요.

### 🟡 Step 3. infovail_essay_v27.docx 생성
- `docs/infovail_essay_v27.md` → .docx 변환
- v26.docx는 plain text (서식 없음) — 새로 생성 필요

### 🟡 Step 4. 원고 최종 통독 교열
- **파일**: `docs/manuscript_v0_5_merged.md` (다운로드: `manuscript_v0_5_merged_figfix.md` 기준)
- 특히 확인:
  - Table 5 CI 값 (stats_recalculated_v4.txt 기준 재검토)
  - Discussion v0.12 수치 잔존 여부
  - Figure 캡션 번호 일치 여부

### 🟢 Step 5. IRB 면제 확인서 수령 후 JMIR 투고
- JMIR Infodemiology 투고 (목표: 4월 초~중)

---

## 2. 오늘 완료된 작업 (2026-03-29)

### Figure 2 재생성 ✅
- **파일**: `outputs/figures/figure2_7C_prevalence_v3_new.png` (300dpi)
- 데이터: `naver_all_20260328_181231_batch.jsonl` + `naver_posts.db`
- 수치 검증: stats_recalculated_v4.txt와 완전 일치

### Figure 3 재생성 ✅
- **파일**: `outputs/figures/figure3_daily_volume_v3_final_update.png` (300dpi)
- Legend n값: hesitancy=2,671 / informational=339 / political=1,409 (확정값 하드코딩)
- 생성 스크립트: `scripts/generate_figures_v3.py` 최종본

### Political amplification 해석 수정 ✅
- Results 3.5 / Discussion 4.5 / Discussion 4.6 (Limitations) 3곳 조정

### References 섹션 완성 ✅ (11개, DOI 포함)

### Figure 구조 분석 + 본문 수정 ✅
- `fig1_timeline.png` 분석: 구버전(5,973건) group-level daily volume — **폐기**
- 본문 `Figure 3B` → `Figure 3` 수정 완료
- **현행 Figure 구성**:
  - Figure 2: `figure2_7C_prevalence_v3_new.png` (3그룹 × 3기간 7C prevalence)
  - Figure 3: `figure3_daily_volume_v3_final_update.png` (daily volume by content type)
  - Figure 1: **없음** → pipeline flowchart 신규 생성 권고 (다음 세션)

### Stage 2 필터 숫자 검증 ✅
- preprocessor.py 코드 확인: 필터 4종이 순차 적용 (mutually exclusive)
- 원고의 "must-have 미포함 3,119" = hard_exclude 92 + no_must_have 3,027을 묶어 표현한 것
- 8,503 − 514(boilerplate) − 92(hard_exclude) − 3,027(no_must_have) = **4,870** ✅

---

## 3. 현재 파일 상태 (투고 직전 기준)

### 원고 파일
| 파일 | 버전 | 상태 |
|------|------|------|
| `docs/manuscript_v0_5_merged.md` | v0.5.0 | ✅ References 완성, Figure 3B→3 수정, political 해석 수정 |
| `docs/abstract_v0_2.md` | v0.2 | ✅ 3,010건 기준 |
| `docs/methods_draft_v0_2.md` | v0.2 | ✅ |
| `docs/results_draft_v0_8.md` | v0.8 | ✅ |
| `docs/discussion_draft_v0_12.md` | v0.12 | ✅ |

### Figure 파일 (제출용)
| Figure | 파일 | 상태 |
|--------|------|------|
| Figure 1 | *없음* | 🔴 pipeline flowchart 신규 생성 권고 |
| Figure 2 | `outputs/figures/figure2_7C_prevalence_v3_new.png` | ✅ 300dpi |
| Figure 3 | `outputs/figures/figure3_daily_volume_v3_final_update.png` | ✅ 300dpi |

### 폐기된 Figure
| 파일 | 폐기 사유 |
|------|-----------|
| `outputs/figures/fig1_timeline.png` | 구버전(5,973건) corpus 기준, 본문 참조 없음, Figure 3와 중복 |
| `outputs/figures/figure2_7C_prevalence_v3.png` | figure2_v3_new로 대체 |
| `outputs/figures/figure3_daily_volume_v3_final.png` | figure3_final_update로 대체 |

---

## 4. 투고 체크리스트

| 항목 | 상태 |
|------|------|
| Figure 2 (300dpi) | ✅ |
| Figure 3 (300dpi, legend 수정, "Figure 3B"→"Figure 3") | ✅ |
| Figure 1 (pipeline flowchart) | 🔴 생성 필요 (또는 없이 투고 결정) |
| References (11개, DOI 포함) | ✅ |
| Political amplification 해석 (Results + Discussion + Limitations) | ✅ |
| 원고 최종 통독 | 🔴 미완료 |
| IRB 면제 확인서 | 🔴 수령 대기 |
| ISoP abstract 가이드라인 확인 + format 조정 | 🔴 미완료 |
| JMIR 투고 | 🔴 IRB 수령 후 |

---

## 5. Figure 1 설계 메모 (다음 세션 참조)

**권고 구성**: 3-stage filtering + LLM classification pipeline flowchart

```
[Naver API 수집]
8,694 posts
     ↓ Stage 1: news channel 제외 (n=191)
8,503 posts
     ↓ Stage 2: 규칙 기반 필터 (순차 적용, mutually exclusive)
         boilerplate 스팸 제거: n=514
         hard-exclude (완전무관 키워드): n=92
         must-have 핵심어 미포함: n=3,027
         제외 소계: n=3,633
4,870 posts
     ↓ Stage 3: LLM semantic filter (claude-haiku-4-5-20251001)
         pro_vaccine 제거: n=12
         irrelevant 제거: n=439
         political → 별도 stratum: n=1,409
3,010 posts (hesitancy n=2,671 + informational n=339)
     ↓ 7C LLM Classification (5 dimensions: C1, C2, C4, C6, C7)
         → Table 5 (prevalence) + Figure 2 (panels a–c) + Figure 3 (volume)
```

**숫자 검증 (2026-03-29, preprocessor.py 코드 확인)**
- Stage 2 필터는 포스트당 첫 번째 탈락 조건에서 멈춤 → 4종 제외 이유가 겹치지 않음
- 8,503 − 514 − 92 − 3,027 = **4,870** ✅
- 원고/PROJECT_PLAN의 "must-have 미포함 3,119" = hard_exclude 92 + no_must_have 3,027 묶음 표현

**생성 도구**: Python matplotlib
**출력 파일**: `outputs/figures/figure1_pipeline.png` (300dpi, 영어, 흰 배경)
**본문 연결**: Methods 2.3절 마지막 문장에 "(Figure 1)" 참조 추가

---

## 6. 핵심 해석 — Political Amplification

**"정치권이 hesitancy를 만든 게 아니라, 지속에 기여했다"**

- Hesitancy 피크: Feb 24 (n=313), Mar 3 (n=306) — E1, E2 직후
- Political 피크: Mar 11 (149건), Mar 16 (180건), Mar 17 (116건) — 2주 시차
- 원고 서술: "did not precede or initiate" + Limitations 6번째 항목에 causal disentanglement 불가 명시

---

## 7. PoC2 설계 메모 (별도 세션)

- 중립 키워드 추가 수집 → 친백신/중립/주저함 분류 레이어
- GitHub Actions 일별 자동 수집 이미 구축됨 (post-Mar 29)

---

## 8. 다음 세션 시작 지시어

**전체 세션 이어서 진행:**
```
PROJECT_PLAN v0.16.0 기준으로 이어서 진행해.
HANDOFF_SESSION_END.md 기준 (2026-03-29):
오늘 완료: Figure 2/3 재생성(300dpi) + political amplification 해석 수정 + References 완성(11개) + Figure 구조 분석(fig1 폐기, Figure 3B→3 수정) + Stage 2 필터 숫자 검증
다음 (우선순위 순):
(1) ISoP 2026 공식 가이드라인 확인 → isop2026_abstract_v0_1.md format 조정 (마감 4/20)
(2) Figure 1 pipeline flowchart 신규 생성 (HANDOFF Section 5 스펙 참조)
(3) infovail_essay_v27.docx 생성
(4) 원고 최종 통독 교열 (manuscript_v0_5_merged_figfix.md 기준)
(5) IRB 면제 확인서 수령 후 JMIR 투고
```

**Figure 1만 바로 생성할 때:**
```
HANDOFF_SESSION_END.md의 Section 5 스펙대로 Figure 1 (pipeline flowchart)을 만들어줘.
출력: C:\infovail-iq\outputs\figures\figure1_pipeline.png (300dpi, 영어, 흰 배경)
스크립트: C:\infovail-iq\scripts\generate_figure1.py로 저장
완료 후 manuscript_v0_5_merged.md Methods 2.3절 마지막 문장에 "(Figure 1)" 참조 추가
```
