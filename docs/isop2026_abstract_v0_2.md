# ISoP 2026 Annual Meeting Abstract — Draft v0.2.0

*22–25 September 2026 | San José, Costa Rica*
*Submission deadline: 20 April 2026*

---

**Track:** J — Vaccines & Public Health / J-1 Vaccine Safety

**Title:** Structural Distrust as a Pharmacovigilance Failure: LLM-Based Analysis of Vaccine Hesitancy Discourse Following a Government Audit Disclosure in South Korea

**Authors:** Myeong-eun Cheon, MD, M.M.Sc.¹ | Euncheol Son, MD, PhD²
¹Korea Disease Control and Prevention Agency (KDCA), Cheongju, Republic of Korea
²University of Ulsan College of Medicine, Ulsan, Republic of Korea

---

**Introduction**

South Korea operates the world's highest per-capita COVID-19 vaccine injury compensation approval rate (17.6 per 100,000 doses) [1], yet persistent organized vaccine distrust has intensified rather than resolved. In February 2026, the Board of Audit and Inspection (BAI) disclosed that the KDCA had withheld 1,285 foreign matter contamination reports from the drug regulator while 1.42 million doses continued to be administered — a pharmacovigilance system failure with direct public trust consequences. The co-location of active surveillance, compensation adjudication, and public communication functions within a single agency creates a structural conflict of interest that standard communication interventions cannot address.

**Objective**

To examine how the distributional architecture of vaccine hesitancy discourse shifted before and after two discrete institutional disclosure events across three Korean Naver social media discourse groups, and to interpret findings within a structural pharmacovigilance accountability framework.

**Methods**

Korean-language social media posts (n = 3,010; initial corpus: 8,694; three-stage relevance filtering) were collected from Naver blog and news comment channels across three discourse groups — FM_Direct (vaccine injury advocacy), Court (litigation/judicial), and Chronic (long-term skepticism) — over six weeks (February 7 – March 21, 2026). Posts were classified into 7C vaccine hesitancy dimensions [2] using a validated LLM pipeline benchmarked on the CAVES dataset [3] (macro F1 = 0.585) and evaluated against a Korean inter-rater gold standard (macro F1 = 0.548, κ = 0.330). Pre- vs. post-event comparisons used Fisher's exact test with odds ratios. Two trigger events were analyzed: the BAI audit disclosure (E1, February 23) and an SBS broadcast on a court ruling recognising a causal link between COVID-19 vaccination and myocardial infarction (E2, March 2).

**Results**

Pre-event C1 (Confidence) was already elevated across all groups (range: 60.3–68.9%), confirming that institutional distrust predated the trigger events. Post-event C1 increased significantly across all groups (FM_Direct: OR = 4.07, p = .013; Court: OR = 11.20, p < .001; Chronic: OR = 3.10, p < .001). C7 (Conspiracy) decreased significantly in the Court group (41.9% to 14.2%, OR = 0.23, p < .001), reflecting discourse specificization: the judicial event displaced diffuse global conspiracy framing with targeted Korea-specific institutional accountability demands. Pre-event C1+C7 co-occurrence (range: 24.5–50.0% across groups) confirms structural co-production of distrust and conspiracy belief predating both events, consistent with a surveillance–compensation co-location hypothesis. Politically partisan content (n = 1,409), excluded from the primary analysis, emerged predominantly post-E2 — confirming that political mobilization followed rather than preceded the primary hesitancy surge.

**Conclusion**

The findings demonstrate that pharmacovigilance system architecture directly generates measurable discourse-level distrust. When surveillance and compensation are institutionally co-located, safety communications are structurally discounted regardless of content — a pattern we term institutional capture of the trust channel. Pre-existing elevated C1 baseline across all groups confirms that trigger events revealed rather than created institutional distrust. These results have direct implications for pharmacovigilance system design and provide a replicable infoveillance methodology for early monitoring of institutional credibility in post-crisis settings.

**References**

1. Chu CF, et al. International comparison of COVID-19 vaccine injury compensation systems. Vaccine. 2025. doi:10.1016/j.vaccine.2025.126830
2. Geiger M, et al. Measuring the 7Cs of vaccination readiness. Eur J Psychol Assess. 2021;38(4):261–9.
3. Poddar S, et al. CAVES: An annotated corpus for COVID vaccine concerns on social media. Proc SIGIR. 2022:3154–64.


---

**Word count:** 426 (body; limit 450) ✓
**Sections:** Introduction / Objective / Methods / Results / Conclusion / References ✓
**References cited in text:** [1] Introduction; [2][3] Methods ✓

*[DRAFT v0.2.2 — 2026-03-29 | References 수정: Chu CF, Geiger 38(4):261–9, Poddar 3154–64; analysed→analyzed]*

---

## 내부 메모 (제출 시 삭제)

**제출 전 체크리스트:**
- [ ] Background → Introduction 헤딩 수정 ✓ (이미 반영)
- [ ] References Vancouver style 추가 ✓
- [x] Betsch [4] → 제외 확정
- [ ] Title case 확인: "a", "as", "of", "in", "Following" 등 전치사 처리
- [ ] Track J-1 선택 확인
- [ ] Conflict of Interest 선언 준비 (KDCA 소속 명시)
- [ ] Co-author (E.C.S.) 승인 확인
