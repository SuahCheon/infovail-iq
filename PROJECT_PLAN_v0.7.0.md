# Infovail-IQ PoC1 실행계획

> **Version**: 0.7.0 | **Date**: 2026-03-09 | **Author**: Suah Cheon, MD
> **변경 이력**: v0.1.0 (2026-03-04) 초안 → v0.2.0 7C 전환 → v0.3.0 날짜·배경 확정 → v0.4.0 문서 완성 → v0.5.0 Week 1 코드 완료 → v0.6.0 법원판결 이벤트 추가 → **v0.7.0 (2026-03-09) DB 통합·노이즈 제거·3그룹 재정의·Figure 완성**

---

## 0. 변경 이력

### v0.6.0 → v0.7.0 주요 변경사항

| 항목 | v0.6.0 | v0.7.0 | 변경 근거 |
|------|--------|--------|-----------|
| DB 경로 | 루트/poc1 분리 | **poc1 단일 DB 확정** | merge_db.py 실행, 중복 0건 확인 |
| DB 건수 | 4,855건 + 2,412건 | **5,973건** | "백신 오염" 1,294건 노이즈 제거 후 |
| 노이즈 키워드 | "백신 오염" 포함 | **"백신 오염" 제거** | 축산·환경 오염과 우연 매칭 확인 |
| 키워드 그룹 | 2그룹 (이물질 vs 법원) | **3그룹** (FM_Direct / Court / Chronic) | 만성 기저불신 담론 분리 |
| 이벤트 구조 | primary 1개 (02.23) | **primary 2개** (02.23 감사원 + 03.02 SBS) | 독립 활성화 패턴 실증 확인 |
| 이론 프레임 | C1+C7 vs C1+C6+C7 | **Chronic = 증폭기(amplifier)** 추가 | 두 이벤트 모두 Chronic 동반 상승 확인 |
| Figure | 없음 | **fig1_timeline.png 완성** (3그룹, 300dpi) | outputs/figures/ |
| 신규 스크립트 | collect_court_ruling.py | + merge_db.py, explore_db.py, inspect_baseline.py, regroup_analysis.py, plot_timeline.py v2, remove_noise.py | |

### v0.5.0 → v0.6.0 주요 변경사항

| 항목 | v0.5.0 | v0.6.0 | 변경 근거 |
|------|--------|--------|-----------|
| 이벤트 | 감사원 발표 단일 | + 03.02 SBS 보도 (심근경색 판결+항소) | 3/3 게시물 206건 폭증 확인 |
| 수집 키워드 | 10개 | + 법원판결 7개 | collect_court_ruling.py |
| Stage 1 일정 | Week 3 완료 목표 | **Week 7로 연기** (gold standard 코딩과 병합) | |

---

## 1. 연구 개요

### 1.1 연구 질문

2026년 2월~3월 두 개의 촉발 사건(02.23 감사원 감사 결과 발표, 03.02 SBS 심근경색 판결 보도) 전후, 한국 네이버 소셜미디어에서 백신 주저함(vaccine hesitancy) 담론의 7C 유형별 분포와 다이나믹스는 어떻게 변화하는가? 특히 두 이벤트가 서로 다른 7C 프로파일을 활성화하는가?

### 1.2 연구 목적

1. CAVES 실증 분류 카테고리와 7C 이론 프레임워크 간 체계적 매핑 수립 및 검증
2. LLM 기반 다차원 백신 주저함 분류기의 영어 벤치마크 성능 확인
3. 검증된 분류기의 한국어 소셜미디어 데이터 적용 및 교차 검증
4. 두 촉발 사건의 이벤트별 7C 프로파일 비교 및 만성 기저불신의 증폭기 역할 실증

### 1.3 핵심 가설

**가설 1**: 02.23 감사원 발표 → FM_Direct 담론 폭증 (C1+C7 우세), 03.02 SBS 보도 → Court 담론 폭증 (C1+C6+C7 우세) — 이벤트별 7C 프로파일이 다르다.

**가설 2**: 두 이벤트 간 담론 교차는 ~5% 수준으로 미미하다 — 이슈 특이적(issue-specific) 독립 활성화 경로.

**가설 3**: Chronic(만성 기저불신) 담론은 두 이벤트 모두에 동반 상승한다 — 기저 불신이 증폭기(amplifier) 역할.

---

## 2. 이론 프레임워크

### 2.1 7C 모델 (Geiger et al., 2021)

| 차원 | 정의 | FM_Direct 예상 | Court 예상 |
|------|------|---------------|-----------|
| **Confidence** | 백신 안전성·효과성·시스템 신뢰 | ✅ 이물질 안전성 | ✅ 보상 시스템 불신 |
| **Complacency** | 질병 위험 낮음 인식 | 약함 | 약함 |
| **Constraints** | 물리적·구조적 접근 장벽 | 없음 | 없음 |
| **Calculation** | 위험-편익 정보 탐색·저울질 | 약함 | 약함 |
| **Collective responsibility** | 집단 보호 동기 약화 | 약함 | 약함 |
| **Compliance** | 사회적 압력·강제 반대 | 약함 | ✅ 강제접종 후 국가 배신 |
| **Conspiracy** | 음모론적 해석 | ✅ 의도적 은폐 | ✅ 항소 = 국가가 또 싸운다 |

### 2.2 담론 그룹 × 이벤트 구조

| 담론 그룹 | 수집 키워드 | 관련 이벤트 | 예상 7C |
|-----------|------------|------------|---------|
| **FM_Direct** | 코로나 백신 이물질, 코로나 백신 곰팡이, 감사원 백신 | 02.23 감사원 | C1+C7 |
| **Court** | 코로나 백신 소송, 백신 심근경색 판결, 코로나 백신 항소, 질병청 항소, 코백회, 백신 피해 법원, 코로나 백신 사망 판결 | 03.02 SBS | C1+C6+C7 |
| **Chronic** | 코로나 백신 피해, 백신 피해 보상, 코로나 백신 부작용, 백신 피해자 모임, 코로나 백신 정부 책임, 백신 피해자 | 두 이벤트 모두 | 혼합 (증폭기) |

> **제외**: "백신 오염" — 노이즈 확인, DB 및 모든 스크립트에서 제거 완료 (2026-03-09)

### 2.3 CAVES→7C 매핑 (Stage 1 검증 대상)

| CAVES 카테고리 | 7C 매핑 | 근거 |
|---------------|---------|------|
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
합의 도출                   벤치마크 보고서             이벤트별 7C 비교
```

---

## 4. 데이터 수집 설계

### 4.1 수집 범위

| 구분 | 기간 | 목적 |
|------|------|------|
| **Baseline** | 2026.02.07 ~ 02.22 | 이벤트 전 기저 담론 |
| **Post-event 1** | 2026.02.23 ~ 03.01 | 감사원 발표 후 반응 |
| **Post-event 2** | 2026.03.02 ~ 03.21 | SBS 보도 + 코백회 후 반응 |

### 4.2 수집 채널

| 채널 | 상태 | 비고 |
|------|------|------|
| Naver Blog | ✅ 수집 | 주력 채널 |
| Naver News 댓글 | ✅ 수집 | |
| Naver Cafe | ❌ 제외 | API 날짜 필드 없어 시계열 분석 불가 |

### 4.3 최종 DB 현황 (2026-03-09)

| 항목 | 수치 |
|------|------|
| DB 경로 | `poc1/data/processed/naver_posts.db` |
| 전체 게시물 | **5,973건** |
| FM_Direct | 1,209건 |
| Court | 2,412건 |
| Chronic | 2,087건 |
| 미분류 ("정은경 백신") | 265건 |

### 4.4 주요 이벤트 타임라인

| 날짜 | 이벤트 | 실측 담론 영향 |
|------|--------|---------------|
| 2026.02.23 | 감사원 감사 결과 공개 | FM_Direct 73배 급증 (14→1,024건/주) |
| 2026.02.26 | 국민의힘 장동혁 정치 발언 | |
| 2026.03.02 | SBS 단독 보도 (심근경색 + 항소) | Court 3배 급증 (276→696건/주) |
| 2026.03.04 | 코백회 국회 기자회견 | Court 지속 상승 |

### 4.5 탐색적 분석 핵심 발견

| 발견 | 수치 | 의미 |
|------|------|------|
| FM_Direct × Court 교차 | ~5% | 독립 활성화 경로 확정 |
| DB 통합 중복 | 0건 | 두 키워드셋이 완전히 다른 담론 공간 수집 |
| Chronic 동반 상승 | 두 이벤트 모두 | 증폭기 역할 실증 |

---

## 5. 12주 실행 타임라인

### Phase 1: 기반 구축 + 긴급 수집 (Week 1~3) ✅ 완료

| 작업 | 상태 |
|------|------|
| 수집 파이프라인 (naver_client, preprocessor, db) | ✅ |
| 전체 키워드 수집 (5,973건) | ✅ |
| DB 통합 + 노이즈 제거 | ✅ |
| 키워드 3그룹 재정의 | ✅ |
| 탐색적 분석 스크립트 | ✅ |
| fig1_timeline.png | ✅ |
| 7C_CODEBOOK.md, ETHICS_STATEMENT, DATA_GOVERNANCE | ✅ |
| IRB 신청 서류 | ✅ (제출 예정) |

**Phase 1 게이트 체크**:
- [x] 데이터 ≥ 500건 → **5,973건**
- [ ] kappa ≥ 0.8 → **Week 7로 연기**
- [x] DB 정상 운영

### Phase 2: LLM 벤치마크 + 분류 준비 (Week 4~7) 🔴

- CAVES 데이터셋 확보
- 모델 선정 + 로컬 셋업
- 영어 벤치마크 (macro-avg F1 ≥ 0.7 목표)
- 한국어 Gold standard 100건 수동 코딩
- CAVES→7C Cohen's kappa (gold standard와 병합)
- PROMPT_REGISTRY.md, EVALUATION_PROTOCOL.md

### Phase 3: 한국어 적용 + 분석 (Week 8~10) 🔴

- 전체 5,973건 LLM 분류
- 이벤트별 7C 프로파일 비교 (FM_Direct vs Court)
- Chronic 증폭기 역할 정량화
- co-occurrence network
- Figure 2~3

### Phase 4: 통합·논문·공개 (Week 11~12) 🔴

- 논문 Methods / Results / Discussion
- JMIR Infodemiology 투고 준비
- GitHub public repo 공개

---

## 6. 핵심 리스크 & 대응

| 리스크 | 대응 |
|--------|------|
| CAVES 데이터셋 접근 불가 | Poddar 2022 GitHub 확인, 저자 연락 |
| LLM 한국어 성능 부족 | 프롬프트 최적화 + 대안 모델 |
| IRB 면제 불인정 | KDCA 온라인 신청 예정, 불인정 시 full IRB |
| ~~네이버 데이터 소실~~ | ✅ 해소 — 5,973건 수집 완료 |

---

## 7. 즉시 실행 항목 (Next Actions)

1. **즉시**: IRB 면제 확인 — KDCA 연구윤리위원회 온라인 신청
2. **Week 4**: CAVES 데이터셋 확보
3. **Week 4**: LLM 모델 선정 + 로컬 셋업
4. **Week 4**: classification/llm_runner.py 개발 착수
5. **추후 결정**: "정은경 백신" 265건 그룹 분류
6. **3/21 이후**: collect_all.py 재실행 (post-event 잔여 기간 보완)

---

## 8. 참고문헌

- Betsch, C., et al. (2018). Beyond confidence. *PLoS ONE*, 13(12), e0208601.
- Geiger, M., et al. (2021). The 7Cs of vaccination readiness. *EJPA*, 38(4), 261–269.
- Poddar, S., et al. (2022). CAVES dataset. *Proceedings of SIGIR 2022*.
- Chu, S. Y., et al. (2025). COVID-19 vaccine injury compensation in South Korea. *Vaccine*, 43, 126830.
- Kang, S. H., et al. (2024). JKMS, PMC11004775.
