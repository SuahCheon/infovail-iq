# **3. Results**

*[DRAFT — v0.6.0, 2026-03-28 | Stage 2 LLM 필터링 반영: 3,010건 기준 전면 재실행]*

## **3.1 Dataset Overview**

A total of 3,010 Korean-language posts were retained for analysis following three-stage relevance filtering (initial collection: 8,694 posts; see Methods for filtering procedure) from two Naver channels (blog posts and news article comments) across three discourse groups between February 7 and March 21, 2026. Stage 1 and Stage 2 rule-based filtering reduced the corpus from 8,694 to 4,870 posts. Stage 3 LLM-based semantic filtering further excluded pro-vaccine advocacy posts (n = 12), topically irrelevant posts (n = 439), and politically partisan posts that used vaccine issues as a vehicle for party-political discourse rather than expressing personal vaccine hesitancy (n = 1,409; retained in a separate stratum for volume analysis). The final analysis corpus of 3,010 posts comprised hesitancy-coded posts (n = 2,671, 88.7%) and neutral informational posts (n = 339, 11.3%).

The FM_Direct group comprised 1,373 posts (45.6%), the Court group 436 posts (14.5%), and the Chronic group 1,201 posts (39.9%). The all-zero classification rate — posts not positively labeled for any 7C dimension — was 18.4%, substantially lower than in the pre-Stage 3 corpus (23.0%), confirming that semantic filtering further concentrated vaccine hesitancy discourse. Post overlap between FM_Direct and Court groups was approximately 5%, confirming that the two keyword sets captured substantially independent discourse spaces. Table 3 summarizes dataset composition.

Table 3. Dataset composition by discourse group (post-filtering corpus, n = 3,010).

| **Discourse Group** | **Keywords** | **Posts (n)** | **Collection Period** | **Channel** |
| --- | --- | --- | --- | --- |
| FM_Direct (Vaccine injury / direct advocacy) | Foreign matter, fungal contamination | 1,373 | Feb 7 – Mar 21, 2026 | Blog + News comment |
| Court (Litigation / judicial discourse) | COVID-19 vaccine lawsuit, court ruling | 436 | Feb 7 – Mar 21, 2026 | Blog + News comment |
| Chronic (Long-term skepticism) | Vaccine injury chronic, ongoing symptoms | 1,201 | Feb 7 – Mar 21, 2026 | Blog + News comment |
| Total | — | 3,010 | Feb 7 – Mar 21, 2026 |  |

*Note: Naver cafearticle channel excluded due to absence of publication timestamps. News articles (n = 191) excluded as institutional media output. Stage 2 rule-based filtering excluded boilerplate spam (n = 514) and posts lacking Korea-specific COVID-19 vaccination discourse markers (n = 3,119). Stage 3 LLM-based filtering excluded pro-vaccine (n = 12), irrelevant (n = 439), and political (n = 1,409) posts. E1 = BAI audit disclosure (February 23); E2 = SBS broadcast on court-recognized causal link between COVID-19 vaccination and myocardial infarction (March 2).*

## **3.2 LLM Classification Pipeline Performance**

### ***3.2.1 English Benchmark (CAVES Dataset)***

The LLM classifier (claude-haiku-4-5-20251001, prompt v1.1.0) was evaluated on the full CAVES English test set (n = 1,846). Overall macro-average F1 across five mapped dimensions (C1, C2, C4, C6, C7) was 0.585. Performance was highest for C1 Confidence (F1 = 0.696) and C6 Compliance (F1 = 0.632), and lowest for C4 Calculation (F1 = 0.393) and C7 Conspiracy (F1 = 0.403). The C4 and C7 underperformance is attributable to boundary ambiguity: C4 items blend rational risk-weighing language with institutional distrust expressions that overlap with C1 and C7 respectively, as documented in the error analysis (see Supplementary File S1). This macro-F1 level is consistent with published benchmarks for multi-label tweet classification tasks involving overlapping semantic categories (Poddar et al., 2022), and is considered acceptable for the purposes of population-level discourse analysis where distributional trends rather than individual-level classification accuracy are the primary unit of inference. Table 4 summarizes per-dimension performance.

Table 4. LLM classification performance: English benchmark (CAVES, n = 1,846) and Korean gold standard (n = 41, inter-rater).

| **Dimension** | **English Precision** | **English Recall** | **English F1** | **Support (n)** | **Korean F1** | **Korean κ** | **Korean Support (n)** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 Confidence | 0.712 | 0.681 | 0.696 | 842 | 0.778 | 0.444 | 31 |
| C2 Complacency | 0.583 | 0.467 | 0.518 | 120 | N/A | N/A | 0 |
| C4 Calculation | 0.441 | 0.352 | 0.393 | 284 | 0.444 | 0.217 | 7 |
| C6 Compliance | 0.671 | 0.598 | 0.632 | 198 | 0.500 | 0.451 | 5 |
| C7 Conspiracy | 0.438 | 0.372 | 0.403 | 356 | 0.471 | 0.217 | 8 |
| Macro avg | — | — | **0.585** | — | **0.548** | **0.330** | — |

*Macro F1 reported in main text (0.585) reflects the v1.1.0 prompt. Korean macro F1 computed across four scorable dimensions (C2 excluded, support = 0). Korean κ = Cohen's kappa between Coder A and Coder B on 41-item final evaluation set. C3 Constraints and C5 Collective responsibility excluded per CAVES→7C mapping.*

### ***3.2.2 Korean-Language Validation***

Korean-language classification performance was evaluated against a 50-item stratified gold standard sample with inter-rater reliability assessment. Following independent coding, nine posts were identified by both coders as falling outside the target construct and excluded, yielding a final evaluation set of 41 items. Both coders were Korean-English bilingual physician-epidemiologists with AEFI causality assessment experience (lead author S.C. and co-author E.C.S.); neither had formal training in discourse analysis or social science coding methodology. Per-dimension F1 scores and inter-rater kappa values are reported in Table 4.

Overall macro-average F1 across four scorable dimensions was **0.548**, and macro-average Cohen's kappa was **0.330**. C1 Confidence showed the highest inter-rater agreement (κ = 0.438, Moderate), consistent with both coders' domain expertise in institutional trust assessment. C4 Calculation and C7 Conspiracy showed lower agreement (κ = 0.217, Fair), reflecting boundary ambiguity in distinguishing these dimensions from C1 in short-form social media texts — a pattern consistent with the lower English benchmark performance observed for the same dimensions (C4 F1 = 0.393; C7 F1 = 0.403). These kappa values are consistent with reported inter-rater reliability in multi-label social media classification tasks. The lower agreement on C4 and C7 is directionally conservative for the primary finding: systematic boundary uncertainty between C1 and adjacent dimensions would reduce rather than inflate observed C1 effects.

## **3.3 Event-Specific 7C Activation Profiles**

Table 5 presents the prevalence of each 7C dimension across three temporal periods (Pre-E1, E1→E2, Post-E2) for all three discourse groups, with odds ratios and significance tests comparing Pre-E1 to Post-E2. Figure 2 (panels a–c) illustrates these distributional shifts graphically.

Table 5. 7C-type prevalence (%) by discourse group and temporal period, with Pre-E1 vs. Post-E2 odds ratios.

|  | **Pre-E1** | **E1→E2** | **Post-E2** | **OR (95% CI)** | **p-value** | **Notes** |
| --- | --- | --- | --- | --- | --- | --- |
| **FM_Direct** | *n = 16* | *n = 797* | *n = 560* | | | |
| C1 Confidence | 10/16 (62.5%) | 695/797 (87.2%) | 488/560 (87.1%) | 4.07 (1.43–11.53) | 0.013* | Pre-E1 exploratory |
| C4 Calculation | 1/16 (6.2%) | 43/797 (5.4%) | 18/560 (3.2%) | 0.50 (0.06–3.92) | 0.420 ns | |
| C6 Compliance | 2/16 (12.5%) | 94/797 (11.8%) | 88/560 (15.7%) | 1.31 (0.29–5.92) | 1.000 ns | |
| C7 Conspiracy | 9/16 (56.2%) | 241/797 (30.2%) | 245/560 (43.8%) | 0.60 (0.22–1.65) | 0.445 ns | High baseline |
| **Court** | *n = 74* | *n = 52* | *n = 310* | | | |
| C1 Confidence | 51/74 (68.9%) | 25/52 (48.1%) | 298/310 (96.1%) | 11.20 (5.25–23.91) | <0.001*** | Near-saturation post-E2 |
| C4 Calculation | 6/74 (8.1%) | 2/52 (3.8%) | 25/310 (8.1%) | 0.99 (0.39–2.54) | 1.000 ns | |
| C6 Compliance | 4/74 (5.4%) | 2/52 (3.8%) | 13/310 (4.2%) | 0.77 (0.24–2.47) | 0.752 ns | |
| C7 Conspiracy | 31/74 (41.9%) | 13/52 (25.0%) | 44/310 (14.2%) | 0.23 (0.13–0.40) | <0.001*** | Discourse specificization |
| **Chronic** | *n = 184* | *n = 349* | *n = 668* | | | |
| C1 Confidence | 111/184 (60.3%) | 264/349 (75.6%) | 551/668 (82.5%) | 3.10 (2.17–4.42) | <0.001*** | Progressive amplification |
| C4 Calculation | 29/184 (15.8%) | 40/349 (11.5%) | 57/668 (8.5%) | 0.50 (0.31–0.81) | 0.006** | Calculation suppression |
| C6 Compliance | 8/184 (4.3%) | 47/349 (13.5%) | 66/668 (9.9%) | 2.41 (1.14–5.12) | 0.018* | Compliance activation |
| C7 Conspiracy | 53/184 (28.8%) | 118/349 (33.8%) | 146/668 (21.9%) | 0.69 (0.48–1.00) | 0.061 ns | |

*p<0.05*, **p<0.01, ***p<0.001 (Pre-E1 vs Post-E2; Fisher's exact test or χ²). OR = Post-E2 odds / Pre-E1 odds (Woolf method; 95% CI). C2 Complacency omitted (prevalence <1% across all groups and periods). C3 Constraints, C5 Collective responsibility not in CAVES→7C mapping. FM_Direct Pre-E1 n=16: wide CI reflects small stratum; estimates exploratory (see Limitations).*

### ***3.3.1 FM_Direct Group***

The FM_Direct pre-event stratum comprised n = 16 posts following Stage 3 semantic filtering, due to the short data collection window prior to E1 and the API 1,000-result ceiling disproportionately affecting this high-volume keyword group (see Section 4.6). Pre-event estimates for FM_Direct should therefore be interpreted with caution; the following comparisons are exploratory for the pre-event period, and the wide confidence interval for the C1 OR reflects this constraint directly.

With this caveat noted, C1 (Confidence) prevalence was already elevated at baseline (62.5% pre-event) and increased further to 87.1% post-event (+24.6 percentage points, OR = 4.07, 95% CI: 1.43–11.53, p = 0.013). C7 (Conspiracy) showed a non-significant decrease from a high pre-event baseline (56.2% to 43.8%, OR = 0.60, p = 0.445), suggesting that the pre-existing conspiracy discourse was diluted by the large influx of C1-dominant post-event content rather than genuinely suppressed. C4 (Calculation) and C6 (Compliance) were observed at negligible prevalence (<1%) across all periods.

### ***3.3.2 Court Group***

The Court group exhibited a striking pattern. C1 increased from an already-elevated pre-event baseline of 68.9% to near-saturation at 96.1% post-event (+27.2pp, OR = 11.20, 95% CI: 5.25–23.91, p < 0.001), the largest statistically significant OR observed across all group-dimension combinations. Contrary to the a priori hypothesis, C7 decreased substantially from 41.9% to 14.2% (-27.7pp, OR = 0.23, p < 0.001). C4 and C6 were observed at low prevalence (<5%) across all periods. The Court E1→E2 period showed a transient decrease in C1 (48.1%) followed by a dramatic post-E2 surge (96.1%), suggesting that the SBS broadcast on March 2 was the primary event associated with this group's post-event discourse shift.

Daily-resolution analysis confirmed the abruptness and structural nature of this transition. Following E2, C1 rose immediately and dramatically: 94.3% on March 3, sustained at high levels across all subsequent observation days through March 21. Critically, this elevation was independent of daily post volume: the Pearson correlation between total corpus volume and Court C1 prevalence was r = 0.073 (near-zero), and on days when Court posts constituted the entirety of the daily corpus (e.g., March 5–6: total n = 59, Court n = 59), C1 prevalence remained above 61%. Post-E2 Court C1 never fell below 50% on any day in the observation period. These findings confirm that the post-E2 C1 elevation represents a structural qualitative transformation in discourse content rather than a compositional artifact of volume change.

The high pre-event C7 prevalence in the Court group (41.9%) warrants specific attention. Following Stage 3 semantic filtering, this baseline reflects genuine conspiracy-coded vaccine hesitancy discourse rather than political or irrelevant content. Channel-level decomposition confirmed that Court keyword blog content predominantly referenced global conspiratorial narratives rather than Korea-specific institutional critique, indicating that Naver Blog functions as a transnational anti-vaccine conspiracy content circulation medium within this discourse space.

### ***3.3.3 Chronic Group***

The Chronic group demonstrated sustained C1 co-elevation across both trigger events, with C1 increasing from 60.3% pre-event to 82.5% post-event (+22.2pp, OR = 3.10, 95% CI: 2.07–4.65, p < 0.001). C6 also increased significantly (+5.6pp, OR = 2.41, p = 0.018), consistent with long-term skepticism communities activating compliance resistance following institutional disclosures. Notably, C4 showed a significant post-event decrease (-7.3pp, OR = 0.50, p = 0.006) — consistent with a shift from uncertainty-driven information-seeking toward more settled institutional distrust. C7 showed a non-significant decrease (-6.9pp, OR = 0.69, p = 0.061).

## **3.4 C1+C7 Co-occurrence Architecture**

Table 6 presents C1+C7 co-labeling rates across groups and periods. Following Stage 3 semantic filtering, C1+C7 co-occurrence rates at baseline were: FM_Direct 35.3%, Court 17.2%, Chronic 24.1% — reflecting concentrated vaccine hesitancy discourse. Post-event, C1+C7 co-occurrence declined in all three groups (FM_Direct to ~30–42%; Court to 13.9%; Chronic modestly), consistent with compositional dilution: the large influx of C1-dominant event-specific content overwhelmed the pre-existing C7 background. In the FM_Direct post-event corpus, only a negligible fraction carried C7 alone, confirming that residual C7 is almost entirely embedded within C1 following E1.

Table 6. C1+C7 co-occurrence rates by discourse group across temporal periods.

| **Group** | **Overall** | **C1 only** | **C7 only** | **C1+C7** | **Neither** |
| --- | --- | --- | --- | --- | --- |
| FM_Direct (N=1,373) | — | 51.6% | 0.8% | 35.3% | 12.3% |
| Court (N=436) | — | 68.6% | 3.0% | 17.2% | 11.2% |
| Chronic (N=1,201) | — | 53.0% | 2.2% | 24.1% | 20.6% |

| **Group** | **Pre-E1** | **E1→E2** | **Post-E2** | **Trend** |
| --- | --- | --- | --- | --- |
| FM_Direct | 50.0% | 30.0% | 42.3% | Dilution post-E1 → partial recovery |
| Court | 29.7% | 19.2% | 13.9% | Monotonic decrease (specificization) |
| Chronic | 24.5% | 31.2% | 20.4% | Transient increase E1→E2 → decrease |

*C1+C7 = proportion of posts with both C1=1 and C7=1. FM_Direct Pre-E1 n=16: estimate exploratory.*

## **3.5 Discourse Volume and Event Responsiveness**

Daily post volume analysis confirmed that discourse activation co-occurred with discrete institutional events rather than gradual accumulation (Figure 3B). The hesitancy corpus (n = 3,010) showed peak volume on February 24 (313 hesitancy posts) and March 3 (306 hesitancy posts) — the days immediately following E1 and E2 respectively. Informational posts also peaked on February 23–24 (71 and 59 posts respectively), consistent with event-reactive information-seeking behaviour.

Notably, the 1,409 politically partisan posts excluded from the primary analysis showed a markedly different temporal pattern: near-zero Pre-E1 (n = 10), modest E1→E2 (n = 337), and concentrated Post-E2 (n = 1,060), with daily peaks on March 16 (180 posts), March 11 (149 posts), and March 17 (116 posts). This political volume surge coincides with the parliamentary health committee hearing (March 10), the ruling party's announcement of an investigation (March 11), and special legislation proposals (March 17–18). The temporal sequence — hesitancy activation preceding political mobilization by approximately two weeks — confirms that partisan political discourse did not precede or initiate the primary hesitancy discourse surge. However, the sustained political volume during March 10–19 overlaps with the post-E2 hesitancy plateau, suggesting that parliamentary amplification may have contributed to prolonging rather than generating institutional distrust discourse.


