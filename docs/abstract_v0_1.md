# Abstract — Draft v0.1.0

*Dynamics of Vaccine Hesitancy Types Following a Vaccine Safety Crisis: A 7C Framework Infodemiology Study of Korean Naver Social Media Discourse*

---

**Background**

South Korea experienced a major COVID-19 vaccine safety crisis in February–March 2026, when the Board of Audit and Inspection (BAI) disclosed that 1,285 foreign matter reports had been withheld from the Ministry of Food and Drug Safety and that 1.42 million doses were administered following contamination reports. Days later, a Seoul court recognized the first judicially confirmed causal link between COVID-19 vaccination and myocardial infarction death. Despite operating the world's most generous vaccine injury compensation system, South Korea has experienced persistent organized vaccine distrust. This paradox motivates a structural analysis of how public discourse responded to these institutional disclosures.

**Objective**

This study aimed to examine how the distributional architecture of vaccine hesitancy discourse changed before and after two discrete institutional disclosure events (BAI audit, February 23, 2026; SBS broadcast on court ruling, March 2, 2026) across three Korean Naver social media discourse groups, using a validated large language model (LLM)-based classification pipeline grounded in the 7C vaccine hesitancy framework.

**Methods**

Korean-language posts (n = 4,870 after relevance filtering; initial corpus: 8,694) were collected from Naver blog and news comment channels across three discourse groups — FM_Direct (vaccine injury / direct advocacy), Court (litigation / judicial discourse), and Chronic (long-term skepticism) — over six weeks (February 7 – March 21, 2026). Posts were classified into five 7C dimensions (Confidence [C1], Complacency [C2], Calculation [C4], Compliance [C6], Conspiracy [C7]) using Claude Haiku (claude-haiku-4-5-20251001; prompt v1.1.0) via Batch API. The classifier was benchmarked on the English CAVES dataset (n = 1,846; macro F1 = 0.585) and validated against a Korean-language expert-coded gold standard (n = 41; macro F1 = 0.548). Statistical comparisons used Fisher's exact test or chi-squared with odds ratios (Pre-E1 vs. Post-E2).

**Results**

Across all three groups, C1 (Confidence) increased significantly post-event (FM_Direct: 50.0% to 69.8%, OR = 2.70, p = .039; Court: 40.6% to 82.7%, OR = 7.17, p < .001; Chronic: 44.1% to 67.6%, OR = 2.71, p < .001). C7 (Conspiracy) decreased post-event in all groups (FM_Direct: 45.0% to 22.5%, p = .069 ns; Court: 28.1% to 9.7%, OR = 0.29, p < .001; Chronic: 22.3% to 13.7%, OR = 0.59, p = .003). C1+C7 co-occurrence declined compositionally (FM_Direct: 40.0% to 24.6%; Court: 18.8% to 10.0%; Chronic: 19.7% to 14.7%), reflecting dilution by a large influx of C1-dominant post-event content rather than genuine conspiracy belief reduction. Chronic group C4 (Calculation) showed a novel significant post-event decrease (8.8% to 3.9%, OR = 0.53, p = .014), suggesting suppression of exploratory information-seeking as distrust became institutionally settled.

**Conclusions**

Institutional disclosure events selectively activated targeted Confidence (C1) rather than Conspiracy (C7), with the Court group displaying a distinctive discourse specificization pattern in which judicially concrete causal claims displaced diffuse conspiratorial framing. The findings are interpreted through a structural framework of institutional capture of the 7C communication channel, in which the co-location of vaccine safety surveillance and injury compensation functions within a single agency structurally undermines the credibility of safety communications. These results suggest that communication interventions targeting vaccine hesitancy cannot succeed without prior structural separation of surveillance and compensation functions.

---

**Keywords:** vaccine hesitancy; 7C model; infoveillance; social media; large language model; infodemiology; COVID-19; South Korea; institutional trust; conspiracy beliefs

**Word count:** 448
