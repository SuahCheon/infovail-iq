# **3. Results**

*[DRAFT — v0.3.0, 2026-03-23 | 수치 전면 업데이트: 4,870건 기준 (전처리 필터 적용), Korean F1 0.548 확정]*

## **3.1 Dataset Overview**

A total of 4,870 Korean-language posts were retained for analysis following relevance filtering (initial collection: 8,694 posts; see Methods for filtering procedure) from two Naver channels (blog posts and news article comments) across three discourse groups between February 7 and March 21, 2026. The FM_Direct group comprised 2,418 posts (49.7%), the Court group 585 posts (12.0%), and the Chronic group 1,867 posts (38.3%). The all-zero classification rate — posts not positively labeled for any 7C dimension — was 23.0%, substantially lower than in the pre-filtering corpus (45.1%), confirming that relevance filtering successfully concentrated vaccine hesitancy discourse. Post overlap between FM_Direct and Court groups was approximately 5%, confirming that the two keyword sets captured substantially independent discourse spaces. Table 3 summarizes dataset composition.

Table 3. Dataset composition by discourse group (post-filtering corpus, n = 4,870).

| **Discourse Group** | **Keywords** | **Posts (n)** | **Collection Period** | **Channel** |
| --- | --- | --- | --- | --- |
| FM_Direct (Vaccine injury / direct advocacy) | Foreign matter, fungal contamination | 2,418 | Feb 7 – Mar 21, 2026 | Blog + News comment |
| Court (Litigation / judicial discourse) | COVID-19 vaccine lawsuit, court ruling | 585 | Feb 7 – Mar 21, 2026 | Blog + News comment |
| Chronic (Long-term skepticism) | Vaccine injury chronic, ongoing symptoms | 1,867 | Feb 7 – Mar 21, 2026 | Blog + News comment |
| Total | — | 4,870 | Feb 7 – Mar 21, 2026 |  |

*Note: Naver cafearticle channel excluded from analysis due to absence of publication timestamps, which precluded temporal analysis. News articles (n = 191) excluded as they represent media framing rather than public discourse. Boilerplate spam posts (n = 514) and posts lacking Korea-specific COVID-19 vaccination discourse markers (n = 3,119) excluded via relevance filtering. Collection period: February 7 – March 21, 2026 (6 weeks). E1 = BAI audit disclosure (February 23); E2 = SBS broadcast on court-recognized causal link between COVID-19 vaccination and myocardial infarction (March 2).*

## **3.2 LLM Classification Pipeline Performance**

### ***3.2.1 English Benchmark (CAVES Dataset)***

The LLM classifier (claude-haiku-4-5-20251001, prompt v1.1.0) was evaluated on the full CAVES English test set (n = 1,846). Overall macro-average F1 across five mapped dimensions (C1, C2, C4, C6, C7) was 0.585. Performance was highest for C1 Confidence (F1 = 0.696) and C6 Compliance (F1 = 0.632), and lowest for C4 Calculation (F1 = 0.393) and C7 Conspiracy (F1 = 0.403). The C4 and C7 underperformance is attributable to boundary ambiguity: C4 items blend rational risk-weighing language with institutional distrust expressions that overlap with C1 and C7 respectively, as documented in the error analysis (see Supplementary File S1). This macro-F1 level is consistent with published benchmarks for multi-label tweet classification tasks involving overlapping semantic categories (Poddar et al., 2022), and is considered acceptable for the purposes of population-level discourse analysis where distributional trends rather than individual-level classification accuracy are the primary unit of inference. Table 4 summarizes per-dimension performance.

Table 4. LLM classification performance: English benchmark (CAVES, n = 1,846) and Korean gold standard (n = 41).

| **Dimension** | **English Precision** | **English Recall** | **English F1** | **Support (n)** | **Korean F1** | **Korean Support (n)** |
| --- | --- | --- | --- | --- | --- | --- |
| C1 Confidence | 0.712 | 0.681 | 0.696 | 842 | 0.778 | 31 |
| C2 Complacency | 0.583 | 0.467 | 0.518 | 120 | N/A | 0 |
| C4 Calculation | 0.441 | 0.352 | 0.393 | 284 | 0.444 | 7 |
| C6 Compliance | 0.671 | 0.598 | 0.632 | 198 | 0.500 | 5 |
| C7 Conspiracy | 0.438 | 0.372 | 0.403 | 356 | 0.471 | 8 |
| Macro avg | — | — | **0.585** | — | **0.548** | — |

*Macro F1 reported in main text (0.585) reflects the v1.1.0 prompt. Korean macro F1 computed across four scorable dimensions (C2 excluded, support = 0). C3 Constraints and C5 Collective responsibility excluded per CAVES→7C mapping.*

### ***3.2.2 Korean-Language Validation***

Korean-language classification performance was evaluated against a 50-item stratified gold standard sample coded by the lead author (S.C.), a Korean-English bilingual physician-epidemiologist with expertise in vaccine adverse event surveillance. Nine posts assigned all-zero labels (commercial advertisements, n = 2; topically irrelevant content, n = 4; pro-vaccination content, n = 3) were excluded from F1 calculation, yielding a final evaluation set of 41 items. Per-dimension F1 scores are reported in Table 4. Overall macro-average F1 across four scorable dimensions was **0.548**. Qualitative review of misclassified items confirmed that the primary error pattern observed in the English benchmark — C1↔C7 boundary confusion — persisted in Korean, as short social media texts frequently employ institutional distrust language that straddles the boundary between targeted safety concern (C1) and generalized conspiracy belief (C7). This limitation is directionally conservative for the main hypothesis, as it implies potential underestimation of C1+C7 true co-occurrence rates.

## **3.3 Event-Specific 7C Activation Profiles**

Table 5 presents the prevalence of each 7C dimension across three temporal periods (Pre-E1, E1→E2, Post-E2) for all three discourse groups, with odds ratios and significance tests comparing Pre-E1 to Post-E2. Figure 2 (panels a–c) illustrates these distributional shifts graphically.

Table 5. 7C-type prevalence (%) by discourse group and temporal period, with Pre-E1 vs. Post-E2 odds ratios.

|  | **Pre-E1** | **E1→E2** | **Post-E2** | **Δ (Pre vs Post)** | **OR (95% CI)** | **p-value** | **Notes** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **FM_Direct** | *n = 20* | *n = 1,083* | *n = 1,315* |  |  |  |  |
| C1 Confidence | 50.0% | 80.2% | 69.8% | +19.8pp | 2.70 (0.95–5.60) | 0.039* | Primary finding |
| C4 Calculation | 5.0% | 1.3% | 2.0% | -3.0pp | 0.38 (0.07–2.08) | 0.310 ns |  |
| C6 Compliance | 10.0% | 6.1% | 7.1% | -2.9pp | 0.69 (0.18–2.65) | 0.620 ns |  |
| C7 Conspiracy | 45.0% | 22.9% | 22.5% | -22.5pp | 0.42 (0.15–1.14) | 0.069 ns |  |
| **Court** | *n = 128* | *n = 87* | *n = 370* |  |  |  |  |
| C1 Confidence | 40.6% | 18.4% | 82.7% | +42.1pp | 7.17 (4.48–10.89) | <0.001*** | Post-E2 surge |
| C4 Calculation | 5.5% | 3.4% | 7.0% | +1.5pp | 1.30 (0.65–2.59) | 0.458 ns |  |
| C6 Compliance | 0.8% | 3.4% | 3.2% | +2.4pp | 4.17 (0.89–19.55) | 0.118 ns |  |
| C7 Conspiracy | 28.1% | 1.1% | 9.7% | -18.4pp | 0.29 (0.16–0.46) | <0.001*** | Counter-hypothesized |
| **Chronic** | *n = 238* | *n = 492* | *n = 1,137* |  |  |  |  |
| C1 Confidence | 44.1% | 67.1% | 67.6% | +23.5pp | 2.71 (1.99–3.52) | <0.001*** | Amplifier role |
| C4 Calculation | 8.8% | 5.3% | 3.9% | -4.9pp | 0.53 (0.31–0.88) | 0.014* | Novel finding |
| C6 Compliance | 2.5% | 6.5% | 5.9% | +3.4pp | 2.42 (1.04–5.65) | 0.038* |  |
| C7 Conspiracy | 22.3% | 25.0% | 13.7% | -8.6pp | 0.59 (0.41–0.84) | 0.003** |  |

*Note: E1 = BAI audit disclosure (February 23, 2026); E2 = SBS broadcast / KDCA press release (March 2, 2026). Odds ratios compare Pre-E1 vs. Post-E2 prevalence; Fisher's exact test or χ² as appropriate. C2 Complacency prevalence <1% across all groups and periods; omitted from table. C3 Constraints and C5 Collective responsibility excluded per CAVES→7C mapping. Pre-E1 stratum for FM_Direct: n = 20 (small pool due to short pre-event window and post-filtering; estimates interpreted with caution; OR 95% CI is wide).*

### ***3.3.1 FM_Direct Group***

In the FM_Direct group, C1 (Confidence) prevalence increased from 50.0% pre-event to 69.8% post-event (+19.8 percentage points, OR = 2.70, 95% CI: 0.95–5.60, p = 0.039). C7 (Conspiracy) showed a non-significant decrease (45.0% to 22.5%, OR = 0.42, p = 0.069), indicating that the BAI audit disclosure activated targeted institutional distrust while the pre-existing conspiracy discourse was diluted by the large influx of C1-dominant post-event content. The pre-event C7 prevalence of 45.0% reflects the baseline conspiracy discourse present prior to the trigger event. C4 (Calculation) and C6 (Compliance) showed non-significant changes. Note that the FM_Direct pre-event stratum comprised n = 20 posts following relevance filtering; estimates for this stratum should be interpreted with caution given the small sample size.

### ***3.3.2 Court Group***

The Court group exhibited a strikingly different and counter-hypothesized pattern. C1 surged from 40.6% pre-event to 82.7% post-event (+42.1pp, OR = 7.17, 95% CI: 4.48–10.89, p < 0.001), the largest statistically significant OR observed across all group-dimension combinations. Contrary to the a priori hypothesis, C7 decreased substantially from 28.1% to 9.7% (-18.4pp, OR = 0.29, p < 0.001). C4 and C6 showed non-significant changes. The Court E1→E2 period showed a transient decrease in C1 (18.4%) followed by a dramatic post-E2 surge (82.7%), suggesting that the SBS broadcast on March 2 was the primary activation event for this group.

The pre-event C7 prevalence in the Court group (28.1% in the filtered corpus) warrants specific attention. Channel-level decomposition revealed that the '코로나 백신 소송' (COVID-19 vaccine lawsuit) keyword in the Naver Blog channel carried substantially higher C7 prevalence pre-event compared with the news comment channel for the same keyword. Qualitative inspection of LLM rationale outputs confirmed that this blog content predominantly referenced global conspiratorial narratives (World Economic Forum, Chinese Communist Party involvement, nanomaterial injection theories) rather than Korea-specific institutional critique, indicating that Naver Blog functions as a transnational anti-vaccine conspiracy content circulation medium within the Court discourse space.

### ***3.3.3 Chronic Group***

The Chronic group demonstrated sustained C1 co-elevation across both trigger events, with C1 increasing from 44.1% pre-event to 67.6% post-event (+23.5pp, OR = 2.71, 95% CI: 1.99–3.52, p < 0.001). C6 also increased significantly (+3.4pp, OR = 2.42, p = 0.038), consistent with the interpretation that long-term skepticism activates compliance resistance in conjunction with confidence concerns following institutional disclosures. Notably, C4 showed a significant post-event decrease (-4.9pp, OR = 0.53, p = 0.014) — a novel finding suggesting that the trigger events suppressed exploratory cost-benefit analysis in chronic distrust communities, possibly reflecting a shift from uncertainty-driven information-seeking toward settled institutional distrust. C7 also decreased significantly (-8.6pp, OR = 0.59, p = 0.003).

## **3.4 C1+C7 Co-occurrence Architecture**

Table 6 presents C1+C7 co-labeling rates across groups and periods. Following relevance filtering, C1+C7 co-occurrence rates were higher at baseline across all groups than previously estimated (FM_Direct: 40.0%; Court: 18.8%; Chronic: 19.7%), reflecting the concentration of vaccine hesitancy discourse following noise removal. Post-event, C1+C7 co-occurrence declined in all three groups (FM_Direct: 40.0% to 24.6%, 0.6-fold; Court: 18.8% to 10.0%, 0.5-fold; Chronic: 19.7% to 14.7%, 0.7-fold). This decline reflects compositional dilution: the large influx of C1-dominant event-specific content numerically overwhelmed the pre-existing C7 background, while the structural coupling between C1 and C7 — measured as C7-positive posts that are also C1-positive — remained high. In the FM_Direct post-event corpus (n = 1,315), 24.6% of posts carried C1+C7 jointly and only a negligible fraction carried C7 alone, confirming that residual C7 is almost entirely embedded within C1 following the audit disclosure.

Table 6. C1+C7 co-occurrence rates by discourse group, pre-event and post-event.

| **Group** | **Pre-E1 (%)** | **Post-E2 (%)** | **Fold change** | **Interpretation** |
| --- | --- | --- | --- | --- |
| FM_Direct | 40.0% | 24.6% | 0.6× | C7 embedded within C1; diluted by C1 influx |
| Court | 18.8% | 10.0% | 0.5× | C7 displaced by C1 surge (specificization) |
| Chronic | 19.7% | 14.7% | 0.7× | Background amplifier; C7 diluted post-event |

## **3.5 Discourse Volume and Event Responsiveness**

Post-collection volume analysis confirmed that discourse activation was event-driven rather than gradual. FM_Direct weekly posting volume increased substantially following the BAI audit disclosure. Court weekly volume surged following the SBS broadcast. The Chronic group co-elevated with both events, consistent with its hypothesized amplifier role.

Importantly, political events did not produce equivalent discourse activation. The March 10 parliamentary health committee hearing produced a transient 78% volume increase in FM_Direct posts on March 10–11, attributable to time-delayed responses to the February 23 audit rather than a new triggering event. The March 13 political figure meeting produced a 27% volume decrease. These patterns confirm that discourse activation is selective for institutional disclosures from independent agencies (audit bodies, courts) rather than political amplification of the same information — a finding addressed in the Discussion's treatment of locus of scientific authority.

── Draft Notes (remove before submission) ──────────────────────────────

*• v0.3.0 (2026-03-23): 전면 수치 업데이트 — 4,870건 기준, Korean F1 0.548 확정, Table 5 OR/CI 신규 수치 반영*
*• Table 5 수치 출처: data/exports/stats_recalculated_v3.txt (sentinel -1 수정 완료)*
*• FM_Direct Pre-E1 n=20 (필터 후): OR CI 넓음, Limitations에 명시*
*• Figure 2 reference: figure2_v2_20260323.png (재생성 예정)*
*• Court 3.3.2 절: 54.7% / 7.7% C7 채널별 수치 = pre-filtering corpus 기준 — footnote 필요*
