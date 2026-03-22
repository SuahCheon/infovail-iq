# Infovail-IQ PoC1 실행계획

> **Version**: 0.5.0 | **Date**: 2026-03-04 | **Author**: Suah Cheon, MD
> **변경 이력**: v0.1.0 (2026-03-04) 초안 → v0.2.0 (2026-03-04) 7C 프레임워크 전환, 12주 타임라인 재설계 → v0.3.0 (2026-03-04) 날짜 통일(이벤트 2026.02.23), Stage 1 방법론 정교화, Background 초안 완성 반영, 한국 보상 역설 데이터 추가 → v0.4.0 (2026-03-04) Phase 1 문서 산출물 완성 반영 (7C_CODEBOOK, ETHICS_STATEMENT, DATA_GOVERNANCE, MAPPING_REVIEW_FORM, IRB 신청 서류), 리스크 대응 방안 업데이트 → v0.5.0 (2026-03-04) Week 1 코드 트랙 완료 반영 (naver_client.py, db.py, setup_db.py, 테스트 수집 166건 확인), GitHub repo 연동 완료

---

## 0. 변경 이력

### v0.4.0 → v0.5.0 주요 변경사항

| 항목 | v0.4.0 | v0.5.0 | 변경 근거 |
|------|--------|--------|-----------|
| naver_client.py | 🔴 미작성 | **✅ 완성** | blog/news/cafe 3채널, 날짜 필터, 페이지네이션 |
| db.py + setup_db.py | 🔴 미작성 | **✅ 완성** | DATA_GOVERNANCE.md 스키마 기반 SQLite |
| 테스트 수집 | 미실행 | **✅ 166건 확인** | "코로나 백신 이물질" × news, 2026-02-23~03-04 |
| GitHub repo | 미연동 | **✅ 연동 완료** | https://github.com/SuahCheon/infovail-iq |
| 데이터 수집 파이프라인 | 🔴 | **🟡 진행 중** | preprocessor.py 미작성 |

### v0.3.0 → v0.4.0 주요 변경사항

| 항목 | v0.3.0 | v0.4.0 | 변경 근거 |
|------|--------|--------|-----------|
| 7C_CODEBOOK | 🔴 미작성 | **✅ 완성** (md + docx, v1.0.0) | Phase 1 Track B 완료 |
| MAPPING_REVIEW_FORM | 미계획 | **✅ 완성** (docx) | 공저자 독립 검토 양식 — Stage 1 착수 준비 |
| ETHICS_STATEMENT | 🔴 미작성 | **✅ 완성** (md, IRB 신청 진행 중) | 데이터 수집 전 필수 요건 충족 |
| DATA_GOVERNANCE | 🔴 미작성 | **✅ 완성** (md) | 데이터 수집 전 필수 요건 충족 |
| IRB 신청 서류 | 미계획 | **✅ 완성** (연구개요.docx + 온라인신청 입력용 md) | JMIR 투고 요건 — KDCA 온라인 시스템 제출 예정 |
| IRB 리스크 대응 | "사전 확인" | **신청 서류 준비 완료** → 면제 불인정 시 full IRB | 실질적 진행 상황 반영 |

### v0.2.0 → v0.3.0 주요 변경사항

| 항목 | v0.2.0 | v0.3.0 | 변경 근거 |
|------|--------|--------|-----------|
| 이벤트 날짜 | 2025.02.21 (오류) | **2026.02.23** | 감사원 감사 결과 실제 공개일 확인 (검색 검증) |
| 데이터 수집 기간 | 2025.02.07~03.21 | **2026.02.07~03.21** | 이벤트 날짜 수정에 따른 연동 |
| Stage 1 방법론 | "2인 독립 검토" 약식 서술 | **Deductive content analysis 기반 체계적 대응 + 독립 검토** 정교화 | background_draft.docx 작성 과정에서 확정 |
| Background 초안 | 미작성 | **✅ 완성** (6개 섹션, Table 1 국제비교, Table 2 매핑) | 금일 작성 완료 |
| 한국 보상 역설 | 미반영 | **9개국 국제비교 데이터 추가** (접종 10만건당 보상 인정 건수) | Chu et al. 2025, KDCA 내부자료 기반 |

### v0.1.0 → v0.2.0 주요 변경사항

| 항목 | v0.1.0 | v0.2.0 | 변경 근거 |
|------|--------|--------|-----------|
| 분류 프레임워크 | CAVES 7유형 단독 | **7C** (Geiger 2021) + CAVES→7C 매핑 | Conspiracy 차원 필수 (이물질 이슈), 이론적 근거 강화 |
| 방법론 | LLM 분류 직접 적용 | **3단계 파이프라인** (매핑검증→벤치마크→한국어적용) | 학술적 엄밀성 확보 |
| 데이터 수집 기간 | 2025.09~2026.03 (약 6개월) | **2026.02.07~03.21** (6주) | BAI 감사 전후 집중 분석 |
| 이벤트 초점 | 감사 결과 발표 (2026.02.23) | **BAI 감사 결과 발표 (2026.02.23)** | 실제 사건 시점 확인 |
| 분류 대상 | CAVES A~G | **7C**: Confidence, Complacency, Constraints, Calculation, Collective responsibility, Compliance, Conspiracy |
| 매핑 검증 | 없음 | **2인 독립 검토 + Cohen's kappa** | 공저자 확보 완료 |
| 타임라인 | 4주 집중 | **12주** (3월~5월) | 업무 병행 현실 반영 |
| 실행 구조 | 순차 (수집→분류→분석) | **병렬 트랙** (데이터 수집 ∥ 매핑검증) | 데이터 소실 리스크 대응 |

---

## 1. 연구 개요

### 1.1 연구 질문

COVID-19 백신 이물질 이슈(2026.02.23 BAI 감사 결과 발표) 전후, 한국 온라인 커뮤니티에서 백신 주저함(vaccine hesitancy) 의견의 7C 유형별 분포와 다이나믹스는 어떻게 변화하는가?

### 1.2 연구 목적

1. CAVES 실증 분류 카테고리와 7C 이론 프레임워크 간 체계적 매핑 수립 및 검증
2. LLM 기반 다차원 백신 주저함 분류기의 영어 벤치마크 성능 확인
3. 검증된 분류기의 한국어 소셜미디어 데이터 적용 및 교차 검증
4. 이벤트 전후 7C 유형별 시계열 다이나믹스 및 채널별 차이 실증 분석

### 1.3 핵심 가설

BAI 감사 결과(촉발 사건) 이후 Confidence(안전성·효과성 불신)와 Conspiracy가 급증하며, 이것이 기존에 축적된 Compliance(강제접종 반대) 담론과 **공동출현(co-occurrence)**하는 패턴이 관찰될 것이다.

---

## 2. 이론 프레임워크

### 2.1 7C 모델 (Geiger et al., 2021)

WHO/SAGE 계열 발전 경로: 3C (2014) → 5C (Betsch et al., 2018) → **7C** (Geiger et al., 2021)

| 차원 | 정의 | 이 연구에서의 예상 담론 |
|------|------|-------------------------|
| **Confidence** | 백신 안전성·효과성·시스템 신뢰 | "이물질 백신 1,420만 회분" / "보상 기준이 너무 엄격" |
| **Complacency** | 질병 위험 낮음 인식 | "코로나 끝났는데 아직도 백신?" |
| **Constraints** | 물리적·구조적 접근 장벽 | (이 사건에서 상대적 약함) |
| **Calculation** | 위험-편익 정보 탐색·저울질 | "접종해도 걸리는데 뭐하러" |
| **Collective responsibility** | 집단 보호 동기 | (반대 의견에서 약화 예상) |
| **Compliance** | 사회적 압력·강제 반대 | "정부가 접종 강요해놓고 피해는 외면" |
| **Conspiracy** | 음모론적 해석 | "제약사와 정부가 결탁" / "의도적 은폐" |

### 2.2 CAVES→7C 매핑 (Stage 1 검증 대상)

| CAVES 카테고리 (Poddar 2022) | 7C 매핑 | 매핑 근거 |
|------------------------------|---------|-----------|
| Side-effect | Confidence | 안전성 불신 |
| Ineffective | Confidence | 효과성 불신 |
| Rushed | Confidence + Calculation | 검증 불신 + 위험 저울질 |
| Ingredients | Confidence | 성분 안전성 불신 |
| Pharma | Confidence | 제약사/시스템 불신 |
| Conspiracy | Conspiracy | 음모론 |
| Political | Confidence + Conspiracy | 정책결정자 불신 + 음모 |
| Mandatory | Compliance | 강제접종 반대 |
| Unnecessary | Complacency | 낮은 위험 인식 |
| Country | Confidence | 제조국 불신 |
| Religious | Calculation | 가치 기반 판단 |

> **검증 방법**: 두 프레임워크의 조작적 정의(Poddar 2022; Betsch 2018)를 비교하여 초기 매핑(위 표)을 생성. 2인(수아 + 공저자)이 독립적으로 각 매핑에 대해 동의(agree)/수정(modify)/거부(reject)를 기록. Cohen's kappa로 일치도 측정, 불일치 항목은 합의 논의를 통해 최종 확정.

---

## 3. 3단계 방법론 파이프라인

```
Stage 1: 매핑 검증          Stage 2: LLM 벤치마크       Stage 3: 한국어 적용
─────────────────          ──────────────────         ──────────────────
CAVES 11개 카테고리         CAVES 영어 데이터셋         네이버 3채널 한국어
    ↕ 매핑                  (~10K 트윗)                2026.2.7~3.21
7C 7개 차원                 LLM 자동 분류              검증된 LLM 적용
    ↓                          ↓                          ↓
2인 독립 검토               P/R/F1 per category        일부 수동 코딩
Cohen's kappa              macro-avg F1               교차 검증
합의 도출                   벤치마크 보고서             시계열 + 공동출현
```

### Stage 1: CAVES→7C 매핑 검증

- **입력**: CAVES 11개 카테고리 정의 (Poddar et al., 2022, SIGIR) + 7C 차원 정의 (Betsch et al., 2018; Geiger et al., 2021)
- **방법**: Deductive content analysis 기반 체계적 대응. 두 프레임워크의 조작적 정의를 비교하여 초기 매핑을 생성한 후, 2인(수아 + 공저자)이 독립적으로 각 매핑에 대해 동의(agree)/수정(modify)/거부(reject)를 기록. 수정 시 대안 매핑과 근거를 함께 기록.
- **평가**: Cohen's kappa로 2인 간 일치도 측정. 불일치 항목은 합의 논의를 통해 최종 매핑 확정.
- **산출물**: 검증된 매핑 테이블 + Cohen's kappa 값 + 불일치 항목 합의 근거
- **선행 조건**: 공저자 확보 ✅

### Stage 2: LLM 분류기 벤치마크 (영어)

- **입력**: CAVES 데이터셋 (Poddar et al., 2022; 영어 트윗 ~10K, human annotation, 11개 카테고리 다중레이블)
- **방법**: LLM(PH-LLM-3B 또는 대안 모델)으로 CAVES 카테고리 자동 분류 → Stage 1 매핑으로 7C 차원 변환
- **평가**: Precision, Recall, F1-score per category, macro-average F1
- **산출물**: "영어 벤치마크에서 검증된 분류 성능" 보고서
- **선행 조건**: CAVES 데이터셋 확보, 모델 선정

### Stage 3: 한국어 네이버 데이터 적용

- **입력**: 네이버 3채널(뉴스 댓글, 카페, 블로그) 수집 데이터 (2026.02.07~03.21, 6주)
- **방법**: Stage 2에서 검증된 LLM으로 한국어 분류 → 일부(~100건) 수동 코딩으로 교차 검증
- **분석**: 7C 유형별 시계열 추이, 채널별 유형 분포 차이, Co-occurrence network
- **산출물**: 논문 Results 섹션 + Figure/Table

---

## 4. 데이터 수집 설계

### 4.1 수집 범위

| 구분 | 기간 | 목적 |
|------|------|------|
| **Baseline** | 2026.02.07 ~ 02.22 (16일) | 이벤트 전 기저 담론 수준 |
| **Post-event** | 2026.02.23 ~ 03.21 (27일, ~4주) | BAI 감사 발표 후 변화 추적 |

### 4.2 수집 채널

| 채널 | 특성 | 수집 방법 |
|------|------|-----------|
| Naver News 댓글 | 뉴스 소비자 즉각 반응, 짧은 텍스트 | Naver Search API |
| Naver Cafe | 커뮤니티 기반 심층 토론 | Naver Search API |
| Naver Blog | 개인 의견 장문 서술 | Naver Search API |

### 4.3 검색 키워드

**1차 (핵심)**: 코로나 백신 이물질, 백신 오염, 감사원 백신, 코로나 백신 곰팡이

**2차 (기저 불신)**: 코로나 백신 피해, 백신 피해 보상, 코로나 백신 부작용, 백신 피해자 모임

**3차 (정치적 담론)**: 코로나 백신 정부 책임

### 4.4 데이터 관리

- PII 비식별화: 닉네임 해시 처리
- 저장: SQLite (로컬)
- 네이버 이용약관 준수: 공개 게시물만 수집
- 보관 기간: 논문 게재 후 3년 → 폐기

---

## 5. 프로젝트 구조

```
infovail-iq/
├── README.md
├── PROJECT_PLAN.md                    # 📌 본 문서
├── LICENSE                            # MIT
├── .env.example
├── pyproject.toml
│
├── docs/
│   ├── architecture.mermaid
│   ├── POC_SCENARIO.md                # ✅ 작성 완료
│   ├── ETHICS_STATEMENT.md            # 🔴 필수
│   ├── DATA_GOVERNANCE.md             # 🔴 필수
│   ├── PROMPT_REGISTRY.md             # 🔴 필수
│   ├── EVALUATION_PROTOCOL.md         # 🔴 필수
│   ├── 7C_CODEBOOK.md                 # 🔴 필수 — 7C 차원 조작적 정의 + CAVES 매핑
│   ├── WEEKLY_BRIEFING_TEMPLATE.md    # 🟡 권장
│   └── RETROSPECTIVE_FRAMEWORK.md    # 🟡 권장
│
├── pipeline/
│   ├── __init__.py
│   ├── config.py
│   ├── ingestion/                     # Layer 1a: 데이터 수집
│   │   ├── naver_client.py
│   │   ├── preprocessor.py
│   │   └── db.py
│   │
│   ├── classification/                # Layer 1b: LLM 분류
│   │   ├── llm_runner.py
│   │   ├── prompts/
│   │   │   ├── caves_classifier.txt   # CAVES 카테고리 분류 프롬프트
│   │   │   ├── 7c_mapper.txt          # CAVES→7C 변환 로직
│   │   │   └── sentiment.txt
│   │   └── labeler.py
│   │
│   ├── analytics/                     # Layer 2-3: 분석
│   │   ├── cooccurrence.py            # 7C 차원 간 공동출현 분석
│   │   ├── temporal.py                # 시계열 트렌드 & 이벤트 영향
│   │   └── indicators.py
│   │
│   └── export.py
│
├── evaluation/
│   ├── stage1_mapping/                # Stage 1: CAVES→7C 매핑 검증
│   │   ├── independent_reviews/       # 2인 독립 검토 결과
│   │   └── kappa_analysis.py
│   │
│   ├── stage2_benchmark/              # Stage 2: 영어 벤치마크
│   │   ├── caves_dataset/             # CAVES 데이터셋 (Poddar 2022)
│   │   ├── classification_report.py
│   │   └── confusion_matrix.py
│   │
│   └── stage3_korean/                 # Stage 3: 한국어 교차 검증
│       ├── gold_standard/             # 수동 라벨링 (~100건)
│       └── cross_validation.py
│
├── agent/                             # Layer 4: 정책 인텔리전스 (선택)
│   ├── AGENT_SPEC.md
│   └── system_prompts/
│
├── data/                              # .gitignore 대상
│   ├── raw/
│   ├── labeled/
│   └── exports/
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_7c_distribution.ipynb
│   ├── 03_temporal_analysis.ipynb
│   └── 04_cooccurrence_network.ipynb
│
├── tests/
│
└── scripts/
    ├── run_pipeline.py
    ├── setup_db.py
    └── generate_sample_data.py
```

---

## 6. 12주 실행 타임라인

### 설계 원칙

- **병렬 트랙**: 데이터 수집(시간 민감)과 매핑 검증(공저자 협업)을 동시 진행
- **게이트 체크**: 각 Phase 완료 시 다음 단계 진입 판단
- **업무 병행**: 주당 업무 시간 일부 활용 기준

---

### Phase 1: 기반 구축 + 긴급 수집 (Week 1~3)

**Track A: 데이터 수집 (최우선)**

| 작업 | 산출물 | 비고 |
|------|--------|------|
| Naver API 키 발급 확인 | API credentials | Week 1 즉시 |
| `ingestion/naver_client.py` 개발 | 수집 스크립트 | blog, news, cafe |
| `ingestion/preprocessor.py` 개발 | 전처리 스크립트 | HTML strip, 중복 제거 |
| `ingestion/db.py` + `setup_db.py` | SQLite DB | 스키마 설계 |
| 1차 키워드 수집 실행 | raw 데이터 | 2026.02.07~03.21 |
| 2차·3차 키워드 보완 수집 | 추가 데이터 | 기저 불신 + 정치 담론 |

**Track B: Stage 1 매핑 검증**

| 작업 | 산출물 | 비고 |
|------|--------|------|
| `7C_CODEBOOK.md` 초안 작성 | 코드북 | 7C 정의 + CAVES 매핑 + 코딩 예시 |
| 공저자에게 독립 검토 요청 | 검토 양식 배포 | 동의/수정/거부 기록 |
| 독립 검토 결과 수합 | 2인 검토 결과 | |
| Cohen's kappa 산출 | kappa 값 | `stage1_mapping/kappa_analysis.py` |
| 불일치 항목 합의 논의 | 최종 매핑 테이블 | |

**Track C: 문서·인프라**

| 작업 | 산출물 |
|------|--------|
| `ETHICS_STATEMENT.md` 초안 | IRB 면제 사유 정리 |
| `DATA_GOVERNANCE.md` 초안 | PII 처리, 보관 정책 |
| 프로젝트 scaffolding | pyproject.toml, 디렉토리 구조 |

**Phase 1 게이트 체크**:
- [ ] 네이버 데이터 최소 500건 수집 완료
- [ ] CAVES→7C 매핑 Cohen's kappa ≥ 0.8 (또는 합의 완료)
- [ ] SQLite DB 정상 운영

---

### Phase 2: LLM 벤치마크 + 분류 준비 (Week 4~7)

**Stage 2: 영어 벤치마크**

| 작업 | 산출물 | 비고 |
|------|--------|------|
| CAVES 데이터셋 확보 (Poddar 2022) | 영어 트윗 ~10K | arXiv/GitHub에서 다운로드 |
| 모델 선정 및 로컬 셋업 | 모델 파일 | PH-LLM-3B Q4_K_M 또는 대안 |
| 분류 프롬프트 v1 설계 | `caves_classifier.txt` | CAVES 11개 카테고리 분류 |
| CAVES 데이터셋으로 벤치마크 실행 | F1 per category | `stage2_benchmark/` |
| 프롬프트 반복 최적화 | 프롬프트 v2~v3 | macro-avg F1 ≥ 0.7 목표 |
| CAVES→7C 변환 로직 구현 | `7c_mapper.txt` | Stage 1 매핑 기반 |
| `PROMPT_REGISTRY.md` 작성 | 프롬프트 버전 관리 | |

**Stage 3 준비: 한국어 적용 시작**

| 작업 | 산출물 | 비고 |
|------|--------|------|
| 한국어 분류 프롬프트 설계 | 한국어 프롬프트 v1 | 영어 프롬프트 기반 적응 |
| 수집 데이터 100건 샘플링 | gold standard 후보 | 채널별 층화추출 |
| 수동 코딩 실행 (2인) | gold standard | 7C 차원 직접 코딩 |
| `EVALUATION_PROTOCOL.md` 작성 | 평가 프로토콜 | |

**Phase 2 게이트 체크**:
- [ ] 영어 벤치마크 macro-avg F1 ≥ 0.7
- [ ] 한국어 gold standard 100건 완성
- [ ] 한국어 분류 프롬프트 v1 준비

---

### Phase 3: 한국어 적용 + 분석 (Week 8~10)

**Stage 3: 한국어 데이터 분석**

| 작업 | 산출물 | 비고 |
|------|--------|------|
| 전체 수집 데이터 LLM 분류 실행 | labeled 데이터 | 배치 분류 |
| Gold standard 대비 교차 검증 | 한국어 F1 | `stage3_korean/cross_validation.py` |
| 7C 유형별 시계열 분석 | temporal trends | `analytics/temporal.py` |
| 채널별(뉴스/카페/블로그) 비교 | 채널 비교 테이블 | |
| 7C 차원 간 공동출현 분석 | co-occurrence network | `analytics/cooccurrence.py` |
| 이벤트 전후(02.21 기준) 비교 | pre/post comparison | `analytics/indicators.py` |
| 시각화 (Figure 초안) | matplotlib/plotly | notebooks/ |

**Phase 3 게이트 체크**:
- [ ] 한국어 분류 F1 보고 완료
- [ ] 시계열 + 공동출현 분석 완료
- [ ] Figure 초안 3개 이상

---

### Phase 4: 통합·논문·공개 (Week 11~12)

**논문 준비**

| 작업 | 산출물 | 비고 |
|------|--------|------|
| Background/Introduction 최종화 | 논문 섹션 | `background_draft.docx` 기반 |
| Methods 작성 | 논문 섹션 | 3단계 파이프라인 상세 |
| Results 작성 | 논문 섹션 + Figure/Table | |
| Discussion 작성 | 논문 섹션 | 한국 보상 역설, 정책 함의 |
| JMIR Infodemiology 포맷 맞춤 | 투고 준비 원고 | |

**오픈소스 준비**

| 작업 | 산출물 |
|------|--------|
| `run_pipeline.py` — end-to-end 실행 | 통합 스크립트 |
| `CONTRIBUTING.md`, `CHANGELOG.md` | 오픈소스 문서 |
| `.gitignore` 정리 | data/, .env, 모델 파일 제외 |
| `generate_sample_data.py` | 오픈소스 이용자용 |
| GitHub Actions CI | lint (ruff) + test |
| GitHub public repo 공개 준비 | README 최종화 |

**Layer 4 (선택 — 시간 여유 시)**

| 작업 | 산출물 |
|------|--------|
| 정책 브리핑 에이전트 설계 | `AGENT_SPEC.md` |
| 카운터메시징 프롬프트 | system_prompts/ |

---

## 7. 핵심 리스크 & 대응

| 리스크 | 영향 | 대응 |
|--------|------|------|
| **네이버 과거 데이터 소실** | 2026.02~03 데이터 수집 불가 | Phase 1에서 즉시 수집 착수 (최우선) |
| CAVES 데이터셋 접근 불가 | Stage 2 벤치마크 불가 | Poddar 2022 GitHub 확인, 저자 연락 |
| PH-LLM-3B 한국어 성능 부족 | 분류 정확도 미달 | 프롬프트 최적화 + 대안 모델 (Gemma-3-4B, Qwen2.5-3B) |
| Naver API 일일 호출 제한 | 수집량 부족 | 키워드 우선순위 + 일일 배치 스케줄링 |
| IRB 면제 불인정 | 논문 투고 불가 | 신청 서류 준비 완료 (연구개요.docx + DATA_GOVERNANCE.md). KDCA 연구윤리위원회 온라인 신청 예정. 면제 불인정 시 full IRB 심의 신청. |
| 12주 타임라인 초과 | 전체 지연 | Phase 1~2 우선 완료 → PoC1 중간 발표 가능 |
| 공저자 검토 지연 | Stage 1 병목 | Week 2까지 검토 완료 목표, 사전 양식 준비 |

---

## 8. 기술 스택

| 구성 요소 | 도구 | 비고 |
|-----------|------|------|
| 언어 | Python 3.11+ | |
| 데이터 수집 | Naver Search API | blog, news, cafe |
| 로컬 LLM | PH-LLM-3B (Q4_K_M) | llama-cpp-python. 대안: Gemma-3-4B |
| DB | SQLite | 경량, 단일 파일 |
| 분석 | pandas, scipy, networkx | Phi coefficient, 시계열, co-occurrence |
| 시각화 | matplotlib, plotly | 논문용 Figure |
| 정책 인텔리전스 | Claude API (Sonnet) | Layer 4 (선택) |
| 테스트 | pytest | |
| CI/CD | GitHub Actions | lint (ruff) + test |
| 패키지 관리 | uv | pyproject.toml 기반 |

---

## 9. 산출물 목록

### 학술 산출물

| # | 산출물 | 목표 시점 | 상태 |
|---|--------|-----------|------|
| 1 | Background/Introduction 초안 | Phase 1 | ✅ `background_draft.docx` — 6개 섹션 (Introduction, Korean Compensation Paradox + Table 1 국제비교, Triggering Event, Research Gap & Objectives, Methodological Approach + Table 2 CAVES→7C 매핑, Significance) |
| 2 | CAVES→7C 검증된 매핑 테이블 | Phase 1 | 🔴 진행 예정 |
| 3 | 영어 벤치마크 보고서 | Phase 2 | 🔴 |
| 4 | 한국어 교차 검증 결과 | Phase 3 | 🔴 |
| 5 | 논문 완성 원고 (JMIR 포맷) | Phase 4 | 🔴 |

### 기술 산출물

| # | 산출물 | 목표 시점 | 상태 |
|---|--------|-----------|------|
| 6 | 데이터 수집 파이프라인 | Phase 1 | 🟡 진행 중 — `naver_client.py`, `db.py`, `setup_db.py` 완성. `preprocessor.py` 미작성 |
| 7 | LLM 분류 + 7C 매핑 파이프라인 | Phase 2 | 🔴 |
| 8 | 분석 모듈 (시계열, 공동출현) | Phase 3 | 🔴 |
| 9 | GitHub public repo | Phase 4 | 🔴 |

### 문서 산출물

| # | 문서 | 용도 | 상태 |
|---|------|------|------|
| 10 | POC_SCENARIO.md | 시나리오 맥락 | ✅ |
| 11 | 7C_CODEBOOK.md + 7C_CODEBOOK.docx | 조작적 정의 + 매핑 + 코딩 예시 | ✅ |
| 12 | ETHICS_STATEMENT.md | IRB/윤리 — 면제 근거 정리, IRB 신청 진행 중 | ✅ |
| 13 | DATA_GOVERNANCE.md | 데이터 정책 — 수집·비식별화·보관·폐기 | ✅ |
| 16 | MAPPING_REVIEW_FORM.docx | 공저자 독립 검토 양식 (Stage 1) | ✅ |
| 17 | IRB_면제확인요청_연구개요.docx | IRB 온라인 신청 첨부용 연구 개요 | ✅ |
| 14 | PROMPT_REGISTRY.md | 프롬프트 버전 관리 | 🔴 |
| 15 | EVALUATION_PROTOCOL.md | 평가 방법론 | 🔴 |

---

## 10. 한국 보상 역설: 국제비교 데이터

Background 초안(background_draft.docx)에 포함된 핵심 데이터. 한국은 세계 최고 수준의 백신 피해 보상 인정률에도 불구하고 조직화된 불신이 존재하는 "보상 역설(Compensation Paradox)"을 보여준다.

### 접종 10만건당 보상 인정 건수 (국제비교)

| 국가 | 보상 인정 건수/10만 접종 | 출처 |
|------|--------------------------|------|
| **한국** | **17.6** | KDCA 내부자료 (2026.1.1 기준) |
| 태국 | 6.5 | Chu et al. 2025 |
| 핀란드 | 3.2 | Chu et al. 2025 |
| 일본 | 2.8 | Chu et al. 2025 |
| 노르웨이 | 1.8 | Chu et al. 2025 |
| 스웨덴 | 1.2 | Chu et al. 2025 |
| 덴마크 | 0.9 | Chu et al. 2025 |
| 영국 | 0.004 | VDPS 2024 |
| 미국 | 0.0 | CICP 2024 |

> **함의**: 보상의 "양"이 아닌 "신뢰 구조(trust architecture)"가 핵심 문제. 이는 7C 프레임워크에서 Confidence(시스템 신뢰)와 Conspiracy(의도적 은폐 의심) 차원으로 분석 가능.

---

## 11. 참고문헌

- Betsch, C., et al. (2018). Beyond confidence: Development of a measure assessing the 5C psychological antecedents of vaccination. *PLoS ONE*, 13(12), e0208601.
- Geiger, M., et al. (2021). The 7Cs of vaccination readiness. *European Journal of Psychological Assessment*, 38(4), 261–269.
- Poddar, S., et al. (2022). Winds of Change: Impact of COVID-19 on Vaccine-Related Opinions of Twitter Users. *Proceedings of SIGIR 2022*.
- Chu, S. Y., et al. (2025). The characteristics of COVID-19 vaccine injury compensation in South Korea. *Vaccine*, 43, 126830.
- Kang, S. H., et al. (2024). [JKMS, PMC11004775]

---

## 12. 즉시 실행 항목 (Next Actions)

1. **즉시**: Naver API 키 발급 상태 확인
2. **이번 주**: `naver_client.py` 프로토타입 → 1차 키워드 테스트 수집
3. **이번 주**: 공저자에게 CAVES→7C 매핑 검토 양식 발송
4. **Week 2**: 본격 데이터 수집 + 7C_CODEBOOK.md 초안
5. **Week 3**: Stage 1 검증 완료 목표 + CAVES 데이터셋 확보
