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
         제외 소계: 3,633
4,870 posts
     ↓ Stage 3: LLM semantic filter (claude-haiku-4-5-20251001)
         pro_vaccine 제거: n=12
         irrelevant 제거: n=439
         political → 별도 stratum: n=1,409
3,010 posts (hesitancy n=2,671 + informational n=339)
     ↓ 7C LLM Classification (5 dimensions: C1, C2, C4, C6, C7)
         → Table 5 (prevalence) + Figure 2 (panels a–c) + Figure 3 (volume)
```

**숫자 검증 (preprocessor.py 코드 기준, 2026-03-29 확인)**
- Stage 2 필터는 포스트당 첫 번째 탈락 조건에서 멈춤 (mutually exclusive)
- hard_exclude 92건은 boilerplate 514건과 **겹치지 않는 독립 집합**
- must-have 미포함 3,027 = Stage 2에서 boilerplate/hard_exclude 통과 후 핵심어 없는 것
- 원고/PROJECT_PLAN의 "must-have 미포함 3,119" = hard_exclude 92 + no_must_have 3,027을 묶어 표현한 것
- 8,503 − 514 − 92 − 3,027 = **4,870** ✅

**생성 도구**: Python matplotlib (flowchart)
**출력 파일**: `outputs/figures/figure1_pipeline.png` (300dpi)
**본문 연결**: Methods 2.3절 마지막에 "(Figure 1)" 참조 추가
