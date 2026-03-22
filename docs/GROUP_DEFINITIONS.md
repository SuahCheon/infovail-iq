# Discourse Group Definitions (PoC1)

## 3-Group Schema (as of 2026-03-10)

### FM_Direct (Foreign Matter / Audit Disclosure)
이물질 직접 언급 + 감사원 이벤트 촉발 담론

**Keywords:**
- 코로나 백신 이물질
- 코로나 백신 곰팡이
- 감사원 백신
- 정은경 백신 *(accountability subtype)*

**Accountability Subtype Note:**
"정은경 백신" (265건)은 감사원 발표(2/23)에 의해 촉발된 인물 책임론.
- Post-event1에 75.8% 집중 (FM_Direct와 동일한 촉발 구조)
- Post-event2의 50건 중 FM 맥락 38% > Court 맥락 22%
- 7C 프로파일이 FM_Direct와 동일 (C1+C7)
- 라벨링 시 `accountability_flag=True`로 서브태깅 권장
- Discussion: "인물 책임론이 이물질 담론의 하위 패턴으로 출현"

### Court (Court Ruling / SBS Report)
법원판결 + 항소 + 피해자 단체 담론

**Keywords:**
- 코로나 백신 소송
- 백신 심근경색 판결
- 코로나 백신 항소
- 질병청 항소
- 코백회
- 백신 피해 법원
- 코로나 백신 사망 판결

### Chronic (Chronic Distrust)
만성 기저불신 담론 (두 이벤트 모두에 동반 상승하는 증폭기)

**Keywords:**
- 코로나 백신 피해
- 백신 피해 보상
- 코로나 백신 부작용
- 백신 피해자 모임
- 코로나 백신 정부 책임
- 백신 피해자

### Excluded
- ~~백신 오염~~ (removed: 축산/환경 등 무관 노이즈 다수)

## Summary Statistics (post-cleanup)
- Total DB: 5,973 posts
- FM_Direct: 1,474 (incl. 정은경 265)
- Court: 2,412
- Chronic: 2,087
