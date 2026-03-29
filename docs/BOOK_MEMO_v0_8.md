# Book Project Memo — v0.8.0
> 작성일: 2026-03-27 | 세션: Book A 제목 확정 + Epilogue→Book B Intro 연결 구조 확정
> 변경 (v0.8): Book A 정식 제목 확정, Book A Epilogue 마지막 문장 + Book B Intro 연결 문장 초안 추가, Section 9 업데이트
> 이전 (v0.7): Section 4에 "Institutional C4 Failure" 개념 메모 신규 추가
> 이전 (v0.6): Book 포트폴리오 A+B로 축약, Book C 폐기

---

## 1. Book A — *The Architecture of Distrust: Institutional Failure and the Production of Vaccine Hesitancy* (확정)

### 개요
- **Substack 시리즈**: *The Architecture of Distrust*
- **정식 제목**: *The Architecture of Distrust: Institutional Failure and the Production of Vaccine Hesitancy*
- **핵심 논점**: 동아시아 두 사례(일본 HPV, 한국 COVID-19)를 통해 vaccine distrust가 어떻게 구조적으로 생산됐는가
- **Theoretical anchor**: Stuart Blume, *Immunization: How Vaccines Became Controversial* (Reaktion Books, 2017)
  - Blume 논점: 기관 불신이 vaccine hesitancy의 근원
  - 차별점: Blume은 서구 중심 역사 서술 → 이 book은 아시아 사례로 그 구조를 실증적으로 보여줌

---

## 2. 핵심 비교 프레임

### 일본 HPV vs 한국 COVID-19

| | **일본 HPV** | **한국 COVID-19** |
|---|---|---|
| **감시 기능** | 있었으나 정책 결정에서 배제됨 | 있었으나 목적 자체가 보상 지원으로 오염됨 |
| **문제의 성격** | 감시 결과의 무력화 (과학 → 정치) | 감시 기능의 도구화 (감시 → 보상 시녀) |
| **능동감시** | 부재 또는 미약 | 뒤늦게 외주화, 역학 시그널을 보상 기준으로 활용 |
| **zero-risk 논리** | 정치적 판단 — "가능성 배제 못하면 중단" | 입법/사법적 제도화 — "불가능하지 않으면 보상" (특별법 6조 2항) |
| **작동 채널** | 미디어 압력 → 행정부 결정 | 미디어 압력 → 사법 판결 → 입법화 |
| **결과** | 9년간 공백, 자궁경부암 부담 | 구조적 불신 기저화, 보상 과잉 → 음모론 기폭제 |
| **공통점** | 감시체계가 제 역할을 못했을 때 정책 공백을 미디어와 정치가 채움 |

### 핵심 대비
- 일본: **행정적 zero-risk** (중단)
- 한국: **사법/입법적 zero-risk** (보상)
- 결과는 역설적으로 같음 — 대중이 신뢰할 수 있는 독립적 안전성 정보의 부재

---

## 3. 일본 HPV 사례 — 핵심 구조 (확인 완료)

### 감시 기능은 있었으나 결과가 무력화됨
- MHLW 산하 **Vaccine Adverse Reactions Review Committee(VARRC)**가 조사 → 인과관계 지지하는 고품질 증거 없다는 결론
- 그럼에도 과학적 결론이 정책에 반영되지 않음
- **"pseudo informed consent"** 유지 — 시민 인식을 확인하는 방식으로 suspension 정당화

### 보고 시스템의 목적 오염
- 2013년 예방접종법 개정 → 의사뿐만 아니라 피접종자, 보호자 등 **3자도 의학적 평가 없이** 이상반응 보고 가능
- 결과: 과거 접종분까지 포함한 이상반응 보고 단기간 급증 → 신호와 노이즈 구분 불가

### 정치적 작동
- 2019년 전 MHLW 관계자 인터뷰: "suspension이 주로 미디어 보도의 영향을 받았다"
- 일본의 "zero-risk" 사고방식 + public opinion 없이 재개 불가능한 정치 구조

### 비용
- 접종률 1% 이하로 추락 (2016년 기준)
- 2021년 proactive recommendation 재개까지 약 9년
- 자궁경부암 부담 증가: 매년 약 10,000명 진단, 3,000명 사망

### 관련 문헌
- Blume 2017 (theoretical anchor)
- VARRC 관련: ScienceDirect 2019 paper (ethical validity criticism)
- 자궁경부암 비용: Scientific Reports 2020 (Ueda et al.)
- 재개: PMC9746481 (2022)

---

## 4. 한국 COVID-19 사례 — 선례의 연쇄 구조 (핵심 챕터)

### 선례 연쇄
```
1976 돼지독감 → GBS (역학적 근거 있음, 특수 맥락)
↓ 탈맥락화
계절 인플루엔자 백신 → GBS 선례 형성 (근거 약함)
↓ 대법원 판결
COVID-19 AZ → 뇌해면상혈관종(CVM) 동반 뇌출혈 (2022, 최초 판결)
→ KDCA 항소 → 정치적 압력 → 항소 포기 → 사실상 묵시적 선례
↓
COVID-19 AZ → 뇌해면상혈관종(Cerebral Cavernous Malformation) (2022)
COVID-19 Pfizer → 모야모야병 동반 뇌출혈 (2025, Case No. 2023GuHap73595)
↓
특별법 제6조 2항 → "불가능해 보이지 않으면 보상"
↓
심근경색까지 확대 남용 (SBS 보도 + 2026 법원 판결)
```

### 1976 돼지독감-GBS 선례의 탈맥락화
- **Safranek et al. (1991, Am J Epidemiol)** [PMID: 1851395]: 1976 돼지독감 백신 후 6주 이내 GBS 상대위험도 7.10, 접종자 100만 명당 초과 사례 약 9건
- **Lehmann et al. (2010, Lancet Infect Dis)** [PMID: 20797646]: 1976년 돼지독감이라는 특수 맥락 제외하면, 계절 인플루엔자 백신이 GBS를 일으켰다는 증거 없음 (100만 명당 1건 미만)
- **핵심**: 특수한 역학적 맥락(1976 돼지독감)에서 나온 신호가 이후 모든 인플루엔자 백신 + COVID-19 백신에 적용되는 선례가 됨

### 한국 뇌혈관계 케이스 공개 판결
1. **최초 판결 (2022)**: AZ 접종 후 뇌내출혈 + 뇌해면상혈관종(CVM) + 단발신경병증 → 서울행정법원 보상 인정 (Korea Times, 2022-09)
   - KDCA 항소 → 정치적 비판 → 사실상 항소 포기
2. **Moyamoya disease 판결 (2025)**: Pfizer 접종 2시간 후 뇌출혈로 사망 (Case No. 2023GuHap73595, 서울행정법원 2025-07-11)
   - 판결 언어: "백신이 기저 질환을 악화시켜 사망에 이르게 했다는 추론이 의학 이론이나 경험 원칙상 불가능해 보이지 않는다"
3. **심근경색 판결 (2026, SBS 보도)**: 70% 이상 내강 협착 고지혈증 환자, 운동 후 심근경색 → "불가능해 보이지 않는다" + "급하게 만든 백신"
   - SBS 보도: "밀접하다"로 과장 → KDCA 항소를 "은폐 확인"으로 보도

### KDCA 구조적 문제
- **삼중 역할**: 사업 시행 + 보상 결정 + 수동감시 수신
- **능동감시**: 뒤늦게 외주화(한림원), 역학 시그널을 보상 기준으로 활용 목적 오염
- **결과**: 감시 공백 → 법원과 언론이 그 공백을 채움

### 구조적 불투명성의 내러티브 (Chapter 3 삽입 확정)

**삽입 위치**: KDCA 구조적 문제 직후, 특별법 제6조 2항 직전

**논점**: Calculation asymmetry의 제도적 표현 — 공개 자료만 사용

**출처 원칙**:
- BAI 감사 결과 보고서 (2026.2.23) — 공개 자료
- 공공기관 정보공개법 — 공개 자료
- 예방접종도우미 포털 기능 — 공개 사실
- 내부 콜센터 데이터 — **미사용** (비공개 자료, 향후 공개 시 재검토)

**초안 (확정)**:

> The institutional design that produced this confusion did not remain abstract. It became, for many people, a question they could not answer about themselves.
>
> The Board of Audit and Inspection's February 23 disclosure reported that 1,285 batches of COVID-19 vaccines had been flagged for foreign-matter contamination. The agency's response was technically accurate: the flagged vaccines had been quarantined and not administered. But accuracy is not the same as answerability. The question that most people actually had was different — not whether those vaccines had been used in general, but whether their vaccine, the one they had personally received, was among them.
>
> That question had a structural answer: it could not be answered. A citizen's own vaccination record, including lot number, was retrievable through the national vaccination portal. The lot numbers of flagged vaccines were not publicly disclosed — withheld under the Act on Public Institution Information. The two lists existed simultaneously and could not be compared. This was not an oversight. It was the predictable consequence of a system in which the agency responsible for administering the vaccination program was also the agency responsible for deciding what information about that program citizens could access.
>
> What followed was a communication failure only in the narrow sense. In the broader sense, it was a transparency failure produced by structural design. When an institution simultaneously runs a program, adjudicates its harms, and controls information about its own conduct, the result is not merely opacity — it is a specific kind of opacity that is indistinguishable, from the outside, from concealment. The distinction between "we cannot tell you" and "we will not tell you" collapses when the same institution decides both questions.
>
> This is what Calculation asymmetry looks like at the institutional level. The system produced the question. It was simply not designed to answer it.

**서술 원칙**:
- 처방 없음 — 진단에서 멈춤
- 마지막 문장: "The system was simply not designed to permit it"
- 해법 제시 없음: 책의 성격이 구조 해부이지 정책 제언이 아님

### 특별법 제6조 2항
- "불가능하지 않으면 보상" — zero-risk의 입법화
- 인플루엔자-GBS 선례 기준이 근거 없는 케이스에 남용됨

### Institutional C4 Failure — 개념 메모 (v0.7 신규)

**논문(discussion_draft_v0_8) 연결**: 4.4 Fourth 항목 끝에 2문장으로 씨앗 심음.  
**책에서의 역할**: 독립 개념으로 발전.

**핵심 논점**:
- 7C 프레임워크의 C4(Calculation)는 **개인의 주관적 benefit-risk 계산**을 다루도록 설계됨
- 그런데 한국 사례는 C4 오류가 **개인 수준을 넘어 제도 수준에서 법제화**될 수 있음을 보여줌
- 특별법 제6조 2항의 "불가능하지 않으면 보상" 기준 = background rates 없이 시간근접성만으로 인과를 인정하는 것 = 공중보건 당국의 C4 오류를 입법화한 것
- 이 제도적 C4 오류는 개인의 C4 왜곡을 **구조적으로 강화하는 feedback loop**를 형성함:
  ```
  제도가 시간근접성 = 인과성으로 인정
  → 대중도 동일 논리를 정당한 것으로 수용
  → 개인 C4 오류가 제도에 의해 검증받음
  → 구조적 불신 심화
  ```

**일본과의 대비**:
- 일본: 과학을 **정치적으로 침묵**시킴 (행정적 zero-risk)
- 한국: 잘못된 인과 기준을 **법으로 제도화**함 (사법/입법적 zero-risk)
- 결과는 같음 — 대중이 신뢰할 수 있는 독립적 안전성 기준의 부재

**집필 원칙**:
- 공개된 법률 조문 + 판결문 언어만 사용
- "담당자가 틀렸다"가 아니라 "시스템이 그렇게 설계됐다"는 구조 진단
- 처방 없음 — 진단에서 멈춤 (Book A의 서술 원칙 유지)

---

## 5. Blume 인용 전략

### 인용 구조 제안
> Blume argued that vaccine hesitancy is rooted not in irrationality but in institutional mistrust — a product of how public health systems are designed and governed. The Asian cases examined here suggest something sharper: that the architecture of that mistrust is not merely a byproduct of institutional failure, but is actively produced by institutional design.

### Blume과의 차별점
- Blume: 글로벌화 + 신자유주의 경제 → 기관 불신 (서구 중심, 역사적)
- 이 book: 기관의 구조적 이중역할 → distrust 생산 (아시아 사례, 데이터 기반)

---

## 6. Book B — *Bounded Autonomy* (별도 프로젝트)

- **정식 제목**: *Bounded Autonomy: Designing AI Systems for Safety-Critical Healthcare*
- **Substack 시리즈**: *AI Constrained. Epidemiologist Augmented.*
- **첫 에세이**: *Bringing the Expert Panel to the Field* (Vax-Beacon)
- **게시 시점**: JMIR PH&S 투고 후
- **학회 연계**: ISoP Global Meeting 포스터 발표 전후

### Book B 앞부분 논리 흐름 (Book C 고유 내용 흡수)

Book C (*Designing for Safety*) 폐기 결정에 따라, Book C의 핵심 기여였던 **능동감시 설계 원칙**을 Book B 앞부분으로 흡수한다. 이 흐름이 Vax-Beacon의 존재 이유를 직접 설명하는 구조가 된다.

```
[Book B 앞부분]

1. "능동감시가 있었다면 이랬어야 했다"
   — background rate 제시 의무
   — 접종군 vs 미접종군 동일 기간 발생율 비교
   — 모수 대비 발생율의 공개 구조
   — 안전성 기준의 비대칭성 (약은 효과 먼저, 백신은 안전 먼저)

2. "그러나 한국은 구조적으로 만들 수 없는 나라다"
   — KDCA 삼중 역할 (사업 시행 + 보상 결정 + 감시 수신)
   — 능동감시 외주화 + 목적 오염 (역학 시그널 → 보상 기준)
   — Book A의 진단이 Book B의 출발점이 됨

3. "그렇다면 수동감시(AEFI 신고)를 능동감시의 기준으로 해석할 수 있어야 한다"
   — passive signal을 active reasoning으로 처리
   → Vax-Beacon
```

### Book A → Book B 연결
- Book A: "왜 실패했는가" — 진단에서 멈춤
- Book B: "그 실패한 구조 안에서 무엇을 할 수 있는가" — Book C 없이 A→B 연결 완결

---

## 7. Substack 전략 (두 시리즈)

| | **Series A** | **Series B** |
|---|---|---|
| **시리즈** | *The Architecture of Distrust* | *AI Constrained. Epidemiologist Augmented.* |
| **Book** | Book A | *Bounded Autonomy* |
| **첫 에세이** | They were the result, not the cause. | Bringing the Expert Panel to the Field |
| **Note (선게시)** | Beyond Sentiment: Decoding the Architecture of Distrust (LinkedIn 포스팅 편집본) | — |
| **논문** | JMIR Infodemiology | JMIR PH&S |
| **게시 시점** | 논문 투고 후 | 논문 투고 후 |

---

## 8. PoC (Infovail-IQ)가 Book A에서 하는 역할

### 구조
```
Preface (PoC로 시작)
  → "2026년 2월 23일, 나는 데이터를 보고 있었다"
  → 6주간 Naver 데이터가 수십 년간의 구조적 실패를 현재형으로 드러냈다
  → 이 책은 그 데이터가 가리킨 곳을 따라간 결과다

Chapter 1–4 (역사 분석 + 비교)
  → 일본 HPV / 한국 COVID-19 사례
  → PoC 데이터가 중간중간 현재형 증거로 등장
    예: C1 flatline → "구조적 불신은 이미 2026년에도 바닥에 있었다"
    예: discourse specificization → "사건은 새로운 distrust를 만들지 않았다, 드러냈을 뿐"

Epilogue (PoC로 끝)
  → "C1 flatline은 이 책의 모든 주장이 현재형임을 보여준다"
  → "The signal had been there before anyone thought to measure it"
  → infoveillance가 가능하게 한 것: 구조적 실패의 실시간 증명
```

### Preface 첫 문장
> *"What if I tried to analyze the present?"*

이 한 문장이 Preface의 출발점이에요. 에세이 v21의 Hook과 동일한 순간에서 책이 시작해요:
- Kaggle 제출 완료 → LinkedIn 열기 → 감사원 뉴스 → npj Digital Medicine 논문
- "미래를 위해 설계하던 날, 현재가 먼저 왔다"
- 그 질문이 이 책 전체의 방법론적 출발점이자 동기

에세이와 책이 같은 순간에서 시작하는 구조 — Substack 독자가 에세이를 읽고 책으로 이어지는 자연스러운 연속성이 생김.

### PoC 데이터의 역할
- **Preface**: 책을 쓰게 된 동기이자 방법론적 출발점
- **본문**: 역사 분석을 현재형으로 anchoring하는 실증 증거
- **Epilogue**: "지금도 작동하고 있다"는 마무리

### 차별화 포인트
- 다른 vaccine hesitancy 학술서와 달리 **실시간 데이터로 검증된 역사 분석**
- Blume은 역사를 썼지만, 이 책은 역사가 현재에도 반복되고 있음을 데이터로 보여줌

### Epilogue → Book B Intro 연결 (v0.8 확정)

**Book A Epilogue 마지막 문단**:
> "The question is not whether compensation is sufficient. The question is whether the evidence that determines compensation — and the communication of that evidence — can be trusted. Japan answered by silencing the science. Korea answered by legislating around it. Both answers produced the same result: a public with no independent ground to stand on. That is the architecture. The structure remains."

**Book B 첫 문장**:
> "If the architecture cannot be rebuilt from above, can it be reinforced from within — one signal at a time?"

**연결의 논리**:
- Book A: 안전성 평가의 부재 또는 왜곡 + 투명한 전달 실패 → 보상 규모와 무관하게 동일한 결과 (공중보건 사업에 대한 구조적 불신)
- Book B: 그 구조가 이미 실패한 나라에서, 수동감시 + AI로 무엇을 할 수 있는가
- Book A가 진단에서 멈추는 이유: 처방은 Book B의 몫

---

## 9. 다음 세션 Book 작업 항목

- [x] Chapter 3 구조적 불투명성 섹션 초안 확정 (v0.5, 2026-03-19)
- [x] Book C 폐기 결정 + 고유 내용 Book B 앞부분으로 흡수 (v0.6, 2026-03-21)
- [x] Institutional C4 Failure 개념 메모 추가 (v0.7, 2026-03-27)
- [x] Book A 정식 제목 확정 (v0.8, 2026-03-27)
- [x] Book A Epilogue → Book B Intro 연결 문장 초안 확정 (v0.8, 2026-03-27)
- [ ] Book A 챕터 구조 초안 작성
  - Chapter 1: Blume 프레임 설정
  - Chapter 2: 일본 HPV — 감시 결과의 무력화
  - Chapter 3: 한국 COVID-19 — 감시 기능의 목적 오염 + 선례 연쇄
  - Chapter 4: 비교 분석 + Institutional C4 Failure 개념 통합
- [ ] Institutional C4 Failure 챕터 초안 — 특별법 조문 + 판결문 언어 기반으로 작성
- [ ] Book A Epilogue 초안 작성 (확정된 마지막 문단 기반)
- [ ] Book B 앞부분 초안 작성 (능동감시 설계 원칙 → 구조적 불가능 → Vax-Beacon)
- [ ] 일본 HPV 사례 추가 문헌 검토 (VARRC 관련 원문)
- [ ] 한국 특별법 제6조 2항 원문 확인 + 인용
- [ ] 인플루엔자-GBS 대법원 판결 공개 자료 확인

---

## 10. 참고 문헌 (확인 완료)

### 이론적 기반
- Blume, S. (2017). *Immunization: How Vaccines Became Controversial*. Reaktion Books.

### 일본 HPV
- VARRC 관련: [ScienceDirect 2019](https://www.sciencedirect.com/science/article/abs/pii/S0168851019303057)
- 자궁경부암 비용: [Scientific Reports 2020](https://www.nature.com/articles/s41598-020-73106-z)
- 재개 이후: [PMC9746481](https://pmc.ncbi.nlm.nih.gov/articles/PMC9746481/)
- Wikipedia 요약: [HPV vaccination in Japan](https://en.wikipedia.org/wiki/HPV_vaccination_in_Japan)

### 1976 돼지독감-GBS
- Safranek et al. (1991). Am J Epidemiol. [PMID: 1851395](https://pubmed.ncbi.nlm.nih.gov/1851395/) [DOI](https://doi.org/10.1093/oxfordjournals.aje.a115973)
- Lehmann et al. (2010). Lancet Infect Dis. [PMID: 20797646](https://pubmed.ncbi.nlm.nih.gov/20797646/) [DOI](https://doi.org/10.1016/S1473-3099(10)70140-7)
- Vellozzi et al. (2014). Clin Infect Dis. [PMID: 24415636](https://pubmed.ncbi.nlm.nih.gov/24415636/) [DOI](https://doi.org/10.1093/cid/ciu005)

### 한국 뇌혈관계 판결
- AZ + CVM 뇌출혈 (2022): [Korea Times](https://program.koreatimes.co.kr/www/nation/2022/10/119_336369.html)
- Moyamoya 판결 (2025, Case No. 2023GuHap73595): [Korean Law Blog](https://www.thekoreanlawblog.com/2025/09/korean-covid-19-vaccination-injury.html)
- KDCA 항소 비판 (2022): [Korea Times](https://www.koreatimes.co.kr/www/nation/2022/09/119_336543.html)
- 서울시 위로금 확대 (2022): [Korea Herald](https://m.koreaherald.com/article/3206972)
