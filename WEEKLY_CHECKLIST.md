# Infovail-IQ PoC1 — 12주 실행 체크리스트

> **기간**: 2026년 3월 ~ 5월 | **업무 병행** 기준

---

## Phase 1: 기반 구축 + 긴급 수집 (Week 1~3) ✅ 완료

### Week 1 ✅
- [x] Naver API + naver_client.py, db.py, setup_db.py
- [x] 테스트 수집 166건
- [x] 7C_CODEBOOK.md v1.0.0, MAPPING_REVIEW_FORM.docx
- [x] GitHub repo

### Week 2 ✅
- [x] preprocessor.py
- [x] 1~3차 키워드 수집 4,855건
- [x] cafearticle 제외 확정
- [x] ETHICS_STATEMENT.md, DATA_GOVERNANCE.md

### Week 3 ✅
- [x] 4차 키워드 (법원판결 7개) — 2,412건
- [x] DB 통합 (루트→poc1) — merge_db.py
- [x] 노이즈 제거 ("백신 오염") — **최종 5,973건**
- [x] 키워드 3그룹 재정의 (FM_Direct / Court / Chronic)
- [x] 탐색적 분석 (explore_db, inspect_baseline, regroup_analysis)
- [x] fig1_timeline.png (3그룹, 300dpi)
- [x] PROJECT_PLAN.md v0.7.0, WEEKLY_CHECKLIST, POC_SCENARIO, CLAUDE_PROJECT_SETUP 업데이트

**Phase 1 게이트 체크**:
- [x] 데이터 ≥ 500건 → **5,973건**
- [ ] kappa ≥ 0.8 → **Week 7로 연기**
- [x] SQLite DB 정상 운영

---

## Phase 2: LLM 벤치마크 + 분류 준비 (Week 4~7)

### Week 4
- [ ] CAVES 데이터셋 확보 (Poddar 2022)
- [ ] 모델 선정 + 로컬 셋업 (PH-LLM-3B / 대안: Gemma-3-4B)
- [ ] classification/llm_runner.py
- [ ] IRB 면제 — KDCA 온라인 신청

### Week 5
- [ ] 분류 프롬프트 v1 (caves_classifier.txt)
- [ ] 영어 벤치마크 1차 실행
- [ ] PROMPT_REGISTRY.md v1

### Week 6
- [ ] 프롬프트 최적화 v2~v3 (F1 ≥ 0.7 목표)
- [ ] CAVES→7C 변환 로직 (7c_mapper.txt)
- [ ] 100건 층화추출 + 한국어 프롬프트 v1

### Week 7
- [ ] 100건 수동 코딩 (2인, 7C 직접 코딩)
- [ ] **CAVES→7C 매핑 kappa 산출** (Stage 1 완료)
- [ ] EVALUATION_PROTOCOL.md

**Phase 2 게이트 체크**:
- [ ] 영어 벤치마크 macro-avg F1 ≥ 0.7
- [ ] Gold standard 100건 완성
- [ ] 한국어 프롬프트 v1 준비

---

## Phase 3: 한국어 적용 + 분석 (Week 8~10)

### Week 8
- [ ] 5,973건 전체 LLM 분류
- [ ] Gold standard 교차 검증

### Week 9
- [ ] 이벤트별 7C 프로파일 비교 (FM_Direct vs Court)
- [ ] Chronic 증폭기 역할 정량화
- [ ] co-occurrence network

### Week 10
- [ ] Figure 2: 이벤트별 7C 비교
- [ ] Figure 3: co-occurrence
- [ ] Table: 분류 성능 요약

**Phase 3 게이트 체크**:
- [ ] 한국어 F1 보고
- [ ] Figure ≥ 3개

---

## Phase 4: 통합·논문·공개 (Week 11~12)

- [ ] Methods / Results / Discussion 작성
- [ ] JMIR Infodemiology 투고 준비
- [ ] GitHub public repo 공개

---

## 빠른 참조

| Phase | 기간 | 핵심 산출물 | 상태 |
|-------|------|-------------|------|
| 1 | W1–3 | 5,973건 DB + fig1 + 3그룹 | ✅ 완료 |
| 2 | W4–7 | 벤치마크 + Gold standard + kappa | 🔴 |
| 3 | W8–10 | 7C 프로파일 비교 + Figure 2~3 | 🔴 |
| 4 | W11–12 | 논문 원고 + repo | 🔴 |
