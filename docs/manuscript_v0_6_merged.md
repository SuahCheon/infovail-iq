---
title: >
  Dynamics of Vaccine Hesitancy Types Following a Vaccine Safety Crisis:
  A 7C Framework Infodemiology Study of Korean Naver Social Media Discourse
version: v0.6.0-merged
date: 2026-03-29
status: DRAFT — pre-submission
supplementary: Supplementary File S3 (theoretical extensions + future directions)
---

*Dynamics of Vaccine Hesitancy Types Following a Vaccine Safety Crisis: A 7C Framework Infodemiology Study of Korean Naver Social Media Discourse*

**Background**

In February–March 2026, South Korea's Board of Audit and Inspection (BAI) disclosed that 1,285 foreign matter reports had been withheld from the Ministry of Food and Drug Safety (MFDS), during which period 1.42 million doses continued to be administered under KDCA oversight; a further 1.31 million doses were administered without national lot release testing (MFDS responsibility). Days later, a court recognized the first judicially confirmed causal link between COVID-19 vaccination and myocardial infarction. Despite operating the world's most generous vaccine injury compensation system, South Korea has experienced persistent organized vaccine distrust — a paradox motivating structural analysis of discourse responses to these institutional disclosures.

**Objective**

To examine how 7C-type distributions of vaccine hesitancy discourse changed before and after two institutional disclosure events (BAI audit, February 23; SBS broadcast on court ruling, March 2, 2026) across three Naver social media discourse groups, using a validated LLM-based classification pipeline.

**Methods**

Korean-language posts (n = 3,010; initial corpus: 8,694; three-stage relevance filtering) were collected from Naver blog and news comment channels across three discourse groups — FM_Direct (vaccine injury advocacy), Court (litigation/judicial), and Chronic (long-term skepticism) — over six weeks (February 7 – March 21, 2026). Posts were classified into five 7C dimensions using Claude Haiku (claude-haiku-4-5-20251001; prompt v1.1.0) via Batch API, benchmarked on the CAVES dataset (n = 1,846; macro F1 = 0.585), and validated against a Korean inter-rater gold standard (n = 41; macro F1 = 0.548; κ = 0.330). Pre-E1 vs. Post-E2 comparisons used Fisher's exact test or chi-squared with odds ratios.

**Results**

C1 (Confidence) was elevated at pre-event baseline across all groups (FM_Direct: 62.5%; Court: 68.9%; Chronic: 60.3%) and increased significantly post-event (FM_Direct: 87.1%, OR = 4.07, p = .013; Court: 96.1%, OR = 11.20, p < .001; Chronic: 82.5%, OR = 3.10, p < .001). Pre-event C1 elevation confirms that trigger events amplified pre-existing institutional distrust rather than generating it. C7 (Conspiracy) decreased significantly in the Court group (41.9% to 14.2%, OR = 0.23, p < .001), reflecting discourse specificization in which judicial causal claims displaced diffuse conspiratorial framing. Chronic group C4 (Calculation) decreased post-event (15.8% to 8.5%, OR = 0.50, p = .006) and C6 (Compliance) increased (4.3% to 9.9%, OR = 2.41, p = .018).

**Conclusions**

Trigger events revealed rather than created institutional distrust. Audit-type disclosures catalyzed targeted C1 activation; judicial-type events produced discourse specificization displacing C7 with C1. These patterns reflect institutional capture of the 7C communication channel arising from co-location of surveillance and compensation functions. Communication interventions targeting vaccine hesitancy cannot succeed without prior structural separation of these functions.

**Keywords:** vaccine hesitancy; 7C model; infoveillance; social media; large language model; infodemiology; COVID-19; South Korea; institutional trust; conspiracy beliefs

**Word count:** 421 (body; limit 450)

---

**Dynamics of Vaccine Hesitancy Types Following a Vaccine Safety
Crisis:**

**A 7C Framework Analysis of Korean Social Media Discourse**

**on the 2026 COVID-19 Vaccine Foreign Matter Incident**

*\[Draft --- Background / Introduction\]*

**1. Introduction**

Vaccine hesitancy---defined by the WHO Strategic Advisory Group of
Experts (SAGE) as a delay in acceptance or refusal of vaccines despite
availability of vaccination services (MacDonald & SAGE Working Group,
2015)---has been recognized as one of the top ten threats to global
health. While much of the early research on vaccine hesitancy focused on
individual-level attitudes and demographic predictors, increasing
attention has been paid to how hesitancy is shaped by specific events,
media narratives, and institutional trust dynamics. The COVID-19
pandemic, which necessitated unprecedented speed in vaccine development
and deployment, amplified both vaccine acceptance and vaccine hesitancy
across populations worldwide.

Understanding vaccine hesitancy requires moving beyond binary
classifications (pro-vaccine vs. anti-vaccine) to examine the
multidimensional nature of concerns that drive hesitant attitudes. The
WHO SAGE Working Group initially proposed the 3C model---Confidence,
Complacency, and Convenience---to categorize determinants of vaccine
hesitancy (SAGE Working Group, 2014). Betsch et al. (2018) extended this
to the 5C model by adding Constraints and Calculation, while subsequent
work further expanded it to the 7C model by incorporating Compliance
(support for societal monitoring of unvaccinated individuals) and
Conspiracy (propensity to endorse conspiracy theories related to
vaccination). The 7C model provides the most comprehensive framework for
capturing the psychological antecedents of vaccination behavior and is
particularly well-suited for analyzing public discourse during crisis
events, where conspiracy narratives and compliance resistance often
intensify.

Despite these theoretical advances, the application of multidimensional
hesitancy frameworks to real-time social media analysis remains limited.
Most existing infoveillance studies on vaccine-related discourse rely on
binary sentiment classification (positive/negative) or broad topic
modeling approaches, which fail to distinguish between qualitatively
different types of hesitancy that may require fundamentally different
public health communication strategies. A parent worried about vaccine
side effects (a Confidence concern) requires a different intervention
than someone who believes vaccines are a tool of government surveillance
(a Conspiracy concern), yet both would be classified identically in a
conventional sentiment analysis.

**2. The Korean Vaccine Compensation Paradox**

South Korea presents a uniquely instructive case for studying vaccine
hesitancy dynamics. The country maintains the world\'s highest
per-capita rate of COVID-19 vaccine injury compensation approvals, with
17.6 approved claims per 100,000 doses administered---approximately
three times the rate of the next-highest country, Thailand (6.5 per
100,000), and incomparably higher than the United States (effectively
0.0 per 100,000) (Table 1).

*Table 1. International Comparison of COVID-19 Vaccine Injury
Compensation (per 100,000 doses administered)*

  -------------------------------------------------------------------------
  **Country**   **Claims     **Claims     **Approval   **Source**
                Filed**      Approved**   Rate (%)**   
  ------------- ------------ ------------ ------------ --------------------
  **South       **70.8**     **17.6**     **26.09**    **KDCA; Chu et al.**
  Korea**                                              

  Thailand      8.8          6.5          ---          KDCA

  Japan         3.9          2.1          74.29        KDCA; Chu et al.

  Germany       6.2          0.2          ---          KDCA

  Australia     6.14         0.46         ---          KDCA

  Canada        3.1          0.2          ---          KDCA

  United        11.3         0.1          2.64         KDCA; Chu et al.
  Kingdom                                              

  United States 1.9          0.0          3.00         KDCA; Chu et al.
  -------------------------------------------------------------------------

*Note: Claims filed and approved are per 100,000 doses. Approval rate
(%) from Chu et al. (2025) where available; South Korea approval rate
(26.09%) is close to the international median of 26.76% across 14
jurisdictions (Chu et al., 2025, n=167,532 total applications). Source:
KDCA internal data (as of 2026.1.1); Chu et al. (Vaccine, 2025, DOI:
10.1016/j.vaccine.2025.126830).*

This paradox is further illuminated by the structural conditions under
which Korea\'s vaccination campaign was conducted. From the outset of
the national COVID-19 immunization program on February 26, 2021,
institutional communication simultaneously introduced both vaccination
guidance and injury compensation pathways---a pattern that stands in
contrast to the early-phase approach of countries such as the United
States and the United Kingdom, which prioritized active safety
surveillance infrastructure (v-safe and Yellow Card, respectively)
during the same period. Within approximately six weeks of the first
vaccinations, public-facing compensation guidance was published by the
KDCA (Korea Disease Control and Prevention Agency \[KDCA\], 2021a). By
May 17, 2021---less than three months after campaign initiation---the
compensation framework was further expanded to cover cases of
\'insufficient causality\' (인과성 불충분), extending support to severe
adverse event cases for which causal evidence was deemed inadequate
under standard review criteria, a standard considerably more permissive
than that applied in most comparator jurisdictions (KDCA, 2021b). While
this early responsiveness reflects a genuine institutional commitment to
accountability, it may have inadvertently established a structural
framing in which adverse event reporting was conflated with injury
claims in public perception. The implications of this framing for the
architecture of vaccine hesitancy---particularly the relationship
between Confidence and Compliance dimensions---will be examined in the
present study.

Yet despite this internationally unparalleled level of compensation,
public distrust toward COVID-19 vaccines persisted and even intensified
in South Korea. Organized advocacy groups representing vaccine-injured
individuals lobbied for legislative action, culminating in the enactment
of the Special Act on COVID-19 Vaccination Injury Compensation in April
2025, which took effect on October 23, 2025. This legislation introduced
a presumption-based causality standard (replacing the previous
burden-of-proof requirement on claimants), established a dedicated
Injury Compensation Committee and Appeals Committee, and allowed
retrospective claims for decisions made before the Act\'s
implementation.

This paradox---the world\'s most generous compensation system failing to
resolve public distrust---suggests that vaccine hesitancy is not
fundamentally a problem of compensation quantity. Rather, it reflects
deeper issues in the trust architecture of public health governance:
procedural transparency, perceived fairness of causality assessment
criteria, and systemic accountability. This observation aligns with the
7C framework\'s distinction between Confidence (trust in vaccine safety
and efficacy), Compliance (attitudes toward institutional mandates), and
Conspiracy (systemic distrust narratives)---dimensions that cannot be
captured by simple sentiment analysis and that persist independent of
compensation generosity.

**3. The 2026 Vaccine Foreign Matter Incident**

On February 23, 2026, South Korea\'s Board of Audit and Inspection (BAI)
released its audit findings on the national COVID-19 response, revealing
significant gaps in vaccine safety management. The audit disclosed two distinct institutional failures attributable to
different agencies. First, the KDCA had received 1,285 reports of
foreign matter found in COVID-19 vaccines from medical institutions
between March 2021 and October 2024, yet failed to report these cases
to the Ministry of Food and Drug Safety (MFDS), instead merely
notifying manufacturers and awaiting their investigation results. During
this period of active suppression, approximately 1.42 million doses
continued to be administered---a failure of KDCA's core safety oversight
function, and the proximate basis for public and parliamentary calls for
the dismissal of the KDCA Commissioner. Second, approximately 1.31
million doses were administered without national lot release
testing---the standard quality verification procedure conducted by the
MFDS for each vaccine batch---representing a separate regulatory failure
attributable to the MFDS rather than the KDCA.

This event is analytically significant for several reasons. First, it
directly implicates institutional safety oversight failures, which are
expected to trigger Confidence-related concerns (trust in the safety
system) as well as Conspiracy narratives (suspicions of deliberate
concealment). Second, it occurred in a context where compensatory trust
mechanisms (the Special Act) had already been established, allowing
observation of how safety-specific concerns interact with pre-existing
systemic distrust. Third, the BAI audit constitutes an official
government self-criticism, creating a unique discursive environment in
which the government\'s own findings validate citizen concerns---a
dynamic that may differentially affect Confidence versus Conspiracy
dimensions of hesitancy.

**4. Research Gap and Objectives**

Existing studies on vaccine-related social media discourse have largely
employed binary sentiment classification or broad topic modeling, which
cannot distinguish between qualitatively different types of vaccine
hesitancy. While the CAVES dataset (Poddar et al., 2022) advanced this
field by introducing fine-grained, multi-label classification of
anti-vaccine concerns (11 categories including side-effects,
ineffectiveness, conspiracy, political motivations, and others), two
significant gaps remain.

First, the CAVES categories were developed as empirical labels for NLP
classification tasks, without systematic mapping to established
theoretical frameworks of vaccine hesitancy. Although the categories are
substantively meaningful, their relationship to the 7C psychological
antecedents framework (Betsch et al., 2018; extended by Geiger et al.,
2021) has not been formally established. This limits the ability to
translate computational classification results into theoretically
grounded public health insights.

Second, most analyses of vaccine-related discourse provide static
snapshots of concern distributions rather than tracking how hesitancy
type compositions shift in response to specific triggering events.
Understanding the dynamics of hesitancy---how different types of
concerns emerge, amplify, co-occur, and attenuate following a crisis
event---is essential for designing timely and targeted public health
communication strategies.

This study addresses these gaps through the following objectives:

> \(1\) To establish a systematic mapping between the CAVES empirical
> classification categories and the 7C theoretical framework, validated
> through independent dual-author review with inter-rater agreement
> (Cohen\'s kappa);
>
> \(2\) To develop and validate an LLM-based classifier for 7C hesitancy
> type classification, benchmarked against the CAVES dataset with
> human-annotated ground truth;
>
> \(3\) To apply the validated classifier to Korean-language social
> media discourse across two Naver channels (blog posts and news article
> comments; Naver Café excluded due to absence of API publication
> timestamps) over a 6-week observation period (February 7 --
> March 21, 2026), spanning approximately 2 weeks of baseline and
> 4 weeks following the BAI audit disclosure;
>
> \(4\) To analyze the temporal dynamics and co-occurrence patterns of
> 7C hesitancy types across channels, with particular attention to the
> interaction between Confidence, Compliance, and Conspiracy dimensions
> following the triggering event.

This study makes three primary contributions: it provides a validated
CAVES–7C mapping with inter-rater reliability metrics; it demonstrates
the feasibility of LLM-based multidimensional hesitancy classification
for non-English social media discourse; and it provides empirical
evidence that qualitatively distinct hesitancy types respond differently
to different institutional disclosure events --- findings calibrated to
the architecture, not merely the volume, of vaccine distrust.

**References**

*(To be completed with full reference list)*

Betsch, C., Schmid, P., Heinemeier, D., Korn, L., Holtmann, C., & Böhm,
R. (2018). Beyond confidence: Development of a measure assessing the 5C
psychological antecedents of vaccination. PLoS ONE, 13(12), e0208601.

Chu, C.-F., Chang, T.-H., & Ho, J.-J. (2025). Comparative analysis of
fourteen COVID-19 vaccine injury compensation systems and claim approval
rates. Vaccine, 52, 126830. DOI: 10.1016/j.vaccine.2025.126830

Geiger, M., Rees, F., Lilleholt, L., et al. (2021). Measuring the 7Cs of
vaccination readiness. European Journal of Psychological Assessment,
38(4), 261--269.

Kang, J. H., et al. (2024). COVID-19 Vaccine Injury Compensation
Programs: A comparative analysis of 10 countries. Journal of Korean
Medical Science, 39(15), e134. PMC11004775

Korea Disease Control and Prevention Agency \[KDCA\]. (2021a). COVID-19
vaccination injury national compensation program guidance \[코로나19
예방접종 후 이상반응 피해 보상 되나요?\]. Retrieved from
https://www.korea.kr/news/policyNewsView.do?newsId=148885933

Korea Disease Control and Prevention Agency \[KDCA\]. (2021b).
Provisional establishment of medical cost support program for severe
adverse event cases with insufficient causality evidence \[코로나19
예방접종 후 인과성 불충분한 중증 환자 의료비 지원사업 한시적 신설\].
Retrieved from
https://www.korea.kr/news/policyNewsView.do?newsId=148889333

MacDonald, N. E., & SAGE Working Group on Vaccine Hesitancy. (2015).
Vaccine hesitancy: Definition, scope and determinants. Vaccine, 33(34),
4161--4164.

Poddar, S., Samad, A. M., Mukherjee, R., Ganguly, N., & Ghosh, S.
(2022). CAVES: A dataset to facilitate explainable classification and
summarization of concerns towards COVID vaccines. In Proceedings of the
45th International ACM SIGIR Conference (pp. 3154--3164).

SAGE Working Group on Vaccine Hesitancy. (2014). Report of the SAGE
Working Group on Vaccine Hesitancy. WHO.

---

# **2. Methods**

## **2.1 Study Design**

This study employed a retrospective cross-sectional infoveillance design to analyze temporal changes in the distributional architecture of vaccine hesitancy discourse on Korean social media following two discrete institutional disclosure events. The observational period was February 7 to March 21, 2026 (six weeks), spanning two weeks of baseline prior to the first trigger event and four weeks following the second. The study was exempt from institutional review board approval as it used only publicly available social media data without collection of personally identifiable information (KDCA Research Ethics Committee, exemption confirmation pending). No direct participant involvement occurred. All analytical decisions were pre-registered in the project plan and subject to independent co-author review.

## **2.2 Data Collection**

### **2.2.1 Platform and Search Interface**

Data were collected from Naver (https://www.naver.com), South Korea's dominant search and social media platform, which accounted for approximately 55% of domestic search traffic as of 2025. Naver hosts three primary user-generated content channels accessible via its Search API: news comments (뉴스 댓글), café posts (카페 게시글), and blog posts (블로그 포스트). The Naver Search API was accessed using the official developer endpoint with approved credentials.

### **2.2.2 Channel Selection**

News comments and blog posts were included in the analysis. Café posts were excluded because the Naver Search API does not return publication timestamps for café articles, rendering temporal analysis impossible. News articles (channel type: `news`) were excluded as they represent institutional media framing rather than public discourse expression. The final analysis corpus comprised blog posts and news comment posts only.

### **2.2.3 Discourse Groups and Keywords**

Three discourse groups were defined a priori based on the topical focus of the triggering events and the theoretical framework:

**FM_Direct** (Vaccine injury / direct advocacy): Keywords directly associated with the BAI audit disclosure, including foreign matter contamination, fungal contamination, and mRNA vaccine adverse events. This group was expected to capture discourse most directly reactive to the BAI audit (E1).

**Court** (Litigation / judicial discourse): Keywords associated with vaccine injury litigation, court rulings, and the KDCA's appeal against the myocardial infarction ruling. This group was expected to capture discourse most reactive to the SBS broadcast (E2).

**Chronic** (Long-term skepticism): Keywords associated with chronic vaccine injury, ongoing adverse event symptoms, and long-term distrust of vaccine safety institutions. This group was expected to function as a background amplifier co-elevating with both events.

A total of 27 keywords were used across three groups (FM_Direct: 10; Court: 7; Chronic: 10), collected separately for blog and news comment channels. The complete keyword list is provided in Supplementary File S2. Keywords were finalized prior to data collection and not modified during the analysis period.

### **2.2.4 Collection Parameters**

Data were collected in three waves: an initial collection (February 7 to March 4, 2026), a supplementary collection (March 9–14, 2026), and a final collection (March 14–21, 2026), yielding a cumulative pre-filtering corpus of 8,694 posts. Duplicate posts (identified by identical content strings) were removed prior to analysis (n = 9 duplicates identified). Post metadata collected included post ID (SHA-256 hashed for privacy), publication timestamp, channel type, keyword, title, and content body.

## **2.3 Relevance Filtering**

To ensure analytical focus on Korean COVID-19 vaccine hesitancy discourse, a three-stage relevance filtering pipeline was applied prior to classification.

In the first stage, all posts from the `news` channel (n = 191) were excluded, as news article texts represent institutional media output rather than individual public discourse.

In the second stage, keyword-based relevance filtering was applied to the remaining posts. A post was retained if its title or body contained at least one of 14 Korea-specific COVID-19 vaccination discourse markers, defined a priori as lexical patterns directly referencing Korean institutional actors, events, or policy contexts (e.g., "코로나 백신", "이상반응", "감사원", "방역패스", "정은경", "코백회"). Prior to this match, posts containing a recurrent boilerplate footer pattern ("영구적인 코로나 봉쇄부터 백신 여권") were excluded (n = 514), as these were identified as originating from a single blogger whose posts systematically appended a globally-circulating anti-vaccine conspiracy text regardless of post topic. Posts failing both the boilerplate exclusion check and the must-have pattern match were flagged as `is_relevant = 0` (n = 3,119 not matching must-have patterns; n = 92 matching hard-exclusion patterns for entirely irrelevant content). This stage reduced the corpus from 8,694 to 4,870 posts (56.0% retained).

In the third stage, a semantic relevance filter was applied using an LLM-based classifier (claude-haiku-4-5-20251001) to identify and exclude posts that passed keyword-based filtering but did not constitute vaccine hesitancy discourse. Each post was classified into one of five content types: (1) *hesitancy* — posts expressing vaccine hesitancy across any 7C dimension; (2) *informational* — neutral factual content (vaccine mechanism explanations, research summaries) without hesitancy expression; (3) *political* — partisan political discourse using vaccine issues as a vehicle, not expressing personal hesitancy; (4) *pro-vaccine* — content advocating vaccination or criticizing vaccine scepticism; and (5) *irrelevant* — content unrelated to vaccine hesitancy (patent news, unrelated court rulings, general pharmaceutical news). Posts classified as *pro-vaccine* (n = 12) or *irrelevant* (n = 439) were excluded from the analysis corpus (n = 451 total, 9.3%). Posts classified as *political* (n = 1,409) were excluded from the primary 7C analysis corpus but retained in a separate stratum for temporal volume analysis (see Section 3.5). Posts classified as *hesitancy* (n = 2,671) and *informational* (n = 339) were retained for 7C classification; *informational* posts were included as they represent C4-relevant content (active information-seeking behaviour) and may carry implicit hesitancy framing.

The final analysis corpus comprised 3,010 posts (hesitancy: 2,671; informational: 339), distributed as follows: FM_Direct 1,373, Court 436, Chronic 1,201 (Figure 1).

## **2.4 Theoretical Framework: The 7C Model**

The 7C model of vaccination readiness (Geiger et al., 2021), an extension of Betsch et al.'s (2018) 5C model, served as the classification framework. The 7C model comprises seven psychological antecedents of vaccination behavior: Confidence (C1; trust in vaccine safety, efficacy, and the delivery system), Complacency (C2; low perceived risk of vaccine-preventable disease), Constraints (C3; structural and practical barriers to vaccination), Calculation (C4; active information search and cost-benefit weighing), Collective Responsibility (C5; prosocial motivation), Compliance (C6; resistance to mandatory vaccination or social pressure), and Conspiracy (C7; propensity to endorse conspiracy theories related to vaccination).

Of the seven dimensions, C3 (Constraints) and C5 (Collective Responsibility) were excluded from the classification system, as these dimensions were not represented in the CAVES benchmark dataset used for classifier validation (see Section 2.5). C2 was retained in the classification schema but was observed at very low prevalence (<1%) throughout the analysis period and is reported descriptively rather than as a primary finding.

## **2.5 CAVES→7C Mapping Validation**

The CAVES dataset (Poddar et al., 2022) consists of approximately 10,000 English-language COVID-19 anti-vaccine tweets with human-annotated multi-labels across 11 empirically derived categories. To use CAVES as a benchmark for 7C classification, a systematic mapping between CAVES categories and 7C dimensions was required. An initial mapping was generated by the lead author (S.C.) based on conceptual correspondence between CAVES category definitions (Poddar et al., 2022) and 7C construct definitions (Betsch et al., 2018; Geiger et al., 2021). This mapping was then independently reviewed by a co-author (E.C.S., field epidemiologist with AEFI causality assessment experience), who recorded agreement, modification, or rejection for each of the 11 category-dimension pairings. Discrepancies were resolved through consensus discussion.

The review yielded 8 agreements and 3 modifications; no categories were rejected. Key modifications were: (a) *Rushed* (originally mapped to Confidence + Calculation) revised to Confidence only, reflecting the 2026 temporal context in which "rushed" discourse functions as entrenched institutional distrust rather than active risk-benefit deliberation; and (b) *Political* (originally mapped to Confidence + Conspiracy) expanded to include Compliance, reflecting the Korean context in which political vaccination framing originates from resistance to de facto mandatory policies (vaccine pass system). The final mapping is presented in Table 2 of the Introduction.

## **2.6 LLM Classification Pipeline**

### **2.6.1 Model and Prompt**

A large language model (LLM) was used to classify each post according to the five active 7C dimensions (C1, C2, C4, C6, C7). The classifier used Claude Haiku (model snapshot: `claude-haiku-4-5-20251001`; Anthropic, San Francisco, CA), with the model snapshot fixed to ensure reproducibility across all classification batches. All classification runs used prompt version v1.1.0 (documented in PROMPT_REGISTRY.md, available in the GitHub repository). The prompt instructed the model to assign binary labels (1 = present, 0 = absent) for each of the five dimensions independently, accompanied by a structured rationale for each assignment. Multi-label classification was explicitly permitted.

### **2.6.2 Few-Shot Examples**

Five few-shot examples per dimension were drawn verbatim from the CAVES training set, selected to represent C1↔C4 and C1↔C7 boundary cases; CAVES tweet IDs are documented in PROMPT_REGISTRY.md (GitHub repository).

### **2.6.3 Classification Execution**

All Korean-language classification was performed using the Anthropic Batch API to minimize latency and cost. Prompt caching was applied to the system prompt component to reduce token processing costs across batches. Classification was applied to the post-filtering corpus of 4,870 posts. Posts for which the LLM response could not be parsed as valid JSON (parse errors; n = 129, 2.6%) were assigned all-zero labels as a conservative fallback. Two posts were lost due to batch processing errors (0.04%). Parse error and batch error rates are reported in Table 4.

## **2.7 English Benchmark Validation**

Prior to Korean-language application, the classification pipeline was benchmarked on the English CAVES test set (n = 1,846) to establish classifier reliability. Per-dimension precision, recall, and F1 scores were computed against CAVES human-annotated ground truth labels using the validated CAVES→7C mapping (Section 2.5). Macro-average F1 was computed across the five active dimensions. The resulting performance metrics (macro F1 = 0.585) are presented in Table 4 of the Results section.

## **2.8 Korean-Language Gold Standard Validation**

Korean-language classification performance was evaluated against an expert-coded gold standard sample with inter-rater reliability assessment. A stratified random sample of 50 posts was drawn from the post-filtering corpus using proportional allocation across six strata (discourse group × collection period: 3 groups × 2 periods). Sampling used a fixed random seed (seed = 42) to ensure reproducibility.

Both coders were Korean-English bilingual physician-epidemiologists with experience in vaccine safety surveillance and AEFI causality assessment (lead author S.C. and co-author E.C.S.). The 50-item sample was coded independently by each coder prior to cross-comparison. Posts were assigned binary labels (1 = present, 0 = absent) for each active 7C dimension (C1, C4, C6, C7); absent labels were recorded as 0 and blank entries treated equivalently. Following independent coding, inter-rater reliability was assessed using Cohen's kappa for each dimension.

Nine posts were identified by both coders as falling outside the target construct (pro-vaccination advocacy, n = 2; topically irrelevant content including patent-related and politically partisan posts, n = 6; content too truncated for reliable coding, n = 1) and were excluded from reliability and F1 calculation, yielding a final evaluation set of 41 posts. Inter-rater reliability on the 41-item set was: C1 κ = 0.438 (Moderate), C4 κ = 0.217 (Fair), C6 κ = 0.450 (Moderate), C7 κ = 0.217 (Fair); macro-average κ = 0.330.

Both coders' AEFI causality assessment expertise supported reliable coding of C1 (institutional trust), the primary outcome dimension; lower agreement on C4 and C7 is directionally conservative for the primary finding (see Section 4.6).

Per-dimension F1 scores were computed by matching expert-coded labels (S.C.) against LLM predictions for the same posts, identified by post ID. Overall macro-average F1 was computed across four scorable dimensions (C2 excluded: support = 0).

## **2.9 Temporal Analysis**

Three temporal periods were defined relative to the two trigger events:

- **Pre-E1**: February 7 to February 22, 2026 (16 days; baseline prior to BAI audit disclosure)
- **E1→E2**: February 23 to March 1, 2026 (7 days; BAI audit disclosure to day before SBS broadcast)
- **Post-E2**: March 2 to March 21, 2026 (20 days; following SBS broadcast on court ruling)

For the FM_Direct and Chronic groups, which were activated primarily by E1 (the BAI audit), the Pre-E1 vs. Post-E2 comparison captures the full event effect. For the Court group, activated primarily by E2 (the SBS broadcast / KDCA appeal), the same comparison captures cumulative post-E2 changes. Group-specific event attribution is discussed in Section 3.3.

## **2.10 Statistical Analysis**

For each group-dimension-period combination, the prevalence of positive classification was computed as the proportion of posts in that stratum with a predicted label of 1. Pre-E1 vs. Post-E2 comparisons were conducted using Fisher's exact test for sparse cells (expected count < 5) or Pearson's chi-squared test otherwise, with a significance threshold of α = 0.05. Odds ratios (OR) with 95% confidence intervals were computed using the standard 2×2 contingency table method. All analyses were performed in Python 3.11 using the `scipy.stats` and `numpy` libraries. C1+C7 co-occurrence was computed as the proportion of posts in a given stratum with both C1 = 1 and C7 = 1.

## **2.11 Ethical Considerations**

This study used only publicly available data from the Naver platform. No personally identifiable information was collected; post IDs were SHA-256 hashed prior to storage. The study does not involve human subjects in the regulatory sense, as no individuals were recruited, contacted, or otherwise engaged. An IRB exemption request was submitted to the KDCA Research Ethics Committee prior to analysis; the formal exemption confirmation is pending at the time of manuscript preparation. The lead researcher (S.C.) is affiliated with the KDCA, the institution central to the structural critique developed in the Discussion. This conflict of interest is fully disclosed; all analytical decisions were pre-registered and subject to independent co-author review.

---

# **3. Results**

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

---

**Discussion \[DRAFT --- v0.3.0, 2026-03-23\]**

*Dynamics of Vaccine Hesitancy Types Following a Vaccine Safety Crisis:
A 7C Framework Analysis of Korean Social Media Discourse*

**4. Discussion**

This study examined how 7C-type distributions of vaccine hesitancy
discourse changed before and after the February 23, 2026 Board of Audit
and Inspection (BAI) audit disclosure across two Naver social media
channels (blog posts and news article comments). Using a validated
LLM-based classification pipeline applied to 3,010 Korean-language
posts (primary analysis corpus following three-stage relevance
filtering; initial collection: 8,694; see Methods), we identified
event-specific shifts in the co-occurrence architecture of vaccine
hesitancy dimensions, with particular salience for the Confidence
(C1)--Conspiracy (C7) cluster. In this section, we
interpret the empirical findings in light of Korea\'s unique
institutional context and discuss the theoretical and practical
implications for public health communication.

**4.1 Principal Findings**

***4.1.1 Event-Specific 7C Activation Profiles***

The empirical findings partially supported our primary hypothesis while
revealing an unexpected and theoretically significant pattern in the
Court discourse group. In the FM_Direct group --- dominated by keywords
directly linked to the BAI audit (foreign matter in vaccines, fungal
contamination) --- C1 prevalence increased significantly from 62.5%
pre-event to 87.1% post-event (+24.6 percentage points, OR=4.07,
p=0.013), confirming the predicted activation of institutional
Confidence concerns. The pre-event stratum comprised n=16 posts
following Stage 3 semantic filtering; these estimates are exploratory
and interpreted with reference to the wide confidence interval (OR:
1.43--11.53). C7 showed a non-significant decrease (56.2% to 43.8%,
OR=0.60, p=0.445), suggesting that the audit disclosure activated
targeted institutional distrust (C1) rather than amplifying generalized
conspiracy beliefs (C7). Notably, the pre-event C7 prevalence of 56.2%
in FM_Direct reflects the baseline conspiracy discourse present prior to
the trigger event; the post-event decline is consistent with the influx
of C1-dominant content following the audit disclosure diluting the
pre-existing C7 background.\
The Court group exhibited a strikingly different and
counter-hypothesized pattern: C7 decreased substantially from 41.9%
pre-event to 14.2% post-event (-27.7 percentage points, OR=0.23,
p\<0.001), while C1 surged from 68.9% to 96.1% (+27.2pp, OR=11.20,
p\<0.001). C4 and C6 were observed at low prevalence (\<9%) across all
periods with no significant pre--post change. Contrary to the
hypothesis of C1+C6+C7 co-activation, the SBS broadcast and KDCA appeal
appear to have displaced rather than amplified conspiracy discourse. We
interpret this pattern as a discourse specificization effect: the judicial
event converted diffuse conspiratorial framing into targeted institutional
distrust directed at a specific agency action (the KDCA appeal). The
structural basis for the pre-event C7 in the Court group is examined in
Section 4.1.4. The Chronic group demonstrated sustained C1 co-elevation
across both trigger events (+22.2pp, OR=3.10, p\<0.001), confirming its
role as a background amplifier, with a significant increase also observed
in C6 (+5.6pp, OR=2.41, p=0.018) and a significant decrease in C4
(-7.3pp, OR=0.50, p=0.006) --- the latter suggesting that trigger events
suppressed exploratory calculation in chronic distrust communities,
possibly reflecting a shift from uncertainty-driven information-seeking
toward settled institutional distrust. The two groups activated largely
independent discourse pathways (~5% post overlap), with the Chronic group
dynamically co-activating with both events rather than persisting as a
static background --- consistent with Betsch et al.\'s (2018)
conceptualization of Confidence as a cumulative attitudinal construct.
Pre-event C1+C7 co-occurrence was elevated across all groups (FM_Direct:
50.0%; Court: 29.7%; Chronic: 24.5%; Table 6), confirming structural
co-production of institutional distrust and conspiracy belief predated
both events. Post-event decline in co-occurrence (FM_Direct: 42.3%;
Court: 13.9%; Chronic: 20.4%) reflects compositional dilution by
C1-dominant event content rather than genuine reduction in the coupling
mechanism; structural interpretation is developed in Section 4.2.3.

***4.1.4 Global--Local C7 Displacement: Transnational Conspiracy
Networks in Korean Vaccine Discourse***

Corpus-level analysis revealed that the pre-event C7 prevalence in
the Court group (41.9% in the Stage 3-filtered corpus^a^) was substantially attributable to global anti-vaccine conspiracy
content circulating on Naver Blog prior to the trigger events. The Court
group keyword set yielded blog-channel posts exclusively throughout the
observation period, precluding direct blog/news_comment channel
comparison within this group. However, cross-group analysis confirmed
that Naver Blog consistently carries higher C7 prevalence than the news
comment channel across independent discourse groups: in FM_Direct,
blog C7 prevalence during the E1→E2 period was 33.8% compared with
13.9% in the news comment channel; in Chronic, the corresponding figures
were 34.7% and 21.9% respectively. This cross-group consistency
supports the interpretation that the blog channel functions as a
transnational anti-vaccine conspiracy content circulation medium at the
platform level, rather than as a Court-group-specific phenomenon.
Qualitative inspection of rationale
outputs confirmed that this blog content predominantly referenced global
conspiratorial narratives --- World Economic Forum, Chinese Communist
Party involvement, David Icke, nanomaterial injection theories ---
rather than Korean-specific institutional critique. An estimated 53.8%
of Court pre-event C7-positive posts reflected global rather than
Korean-specific conspiracy framing. This finding demonstrates that
Korean vaccine hesitancy discourse is embedded within transnational
anti-vaccine information networks, and that the apparent post-event C7
decrease in the Court group reflects a compositional shift --- the
post-event influx of Korea-specific C1-dominant content numerically
diluted the pre-existing global C7 background --- rather than a genuine
reduction in conspiratorial belief.

> ^a^ Following Stage 3 semantic filtering (n=3,010), Court pre-event
> C7 prevalence was 41.9%, higher than in the Stage 2-filtered corpus
> (28.1%, n=4,870). The increase reflects removal of political and
> irrelevant posts that had diluted the C7 signal; the Stage 3 corpus
> more accurately captures genuine conspiracy-coded discourse.

**4.2 The Institutional Capture of the 7C Communication Channel: A
Structural Interpretation**

The high and increasing C1+C7 co-occurrence observed in Korean vaccine
discourse cannot be adequately explained by individual psychological
processes alone. We propose that the observed pattern reflects a
structural condition we term institutional capture of the 7C
communication channel --- a condition in which the institutional
architecture responsible for vaccine safety governance systematically
undermines the credibility of safety-related communications, thereby
converting ordinary distrust (C1) into conspiracy-adjacent belief (C7).

***4.2.1 The Surveillance--Compensation Structural Trap***

In most high-income countries, vaccine pharmacovigilance and injury
compensation are institutionally separated. Active surveillance systems
(e.g., the US v-safe program, the UK Yellow Card scheme) are operated
independently of compensation adjudication bodies, preserving the
epistemic independence of safety signal generation. In South Korea,
however, the Korea Disease Control and Prevention Agency (KDCA)
simultaneously administers passive safety surveillance, compensation
review, and public communication on vaccine safety --- functions whose
co-location creates an inherent credibility deficit.

The consequence of this co-location is what we term contextual
non-acceptance: any KDCA scientific statement on vaccine safety is
structurally interpreted through the lens of its
compensation-adjudicating role, such that evidence of safety is received
as institutional self-interest rather than objective assessment. This
dynamic is not specific to bad-faith actors --- it is a rational
Bayesian inference on the part of the public when the same institution
generates both safety evidence and compensation decisions.

***4.2.2 The Evidence Vacuum and Judicial Substitution***

The absence of a robust active surveillance infrastructure compounded
this structural trap. Without prospective cohort data, signal detection
studies, or population-level pharmacoepidemiological analyses, the KDCA
lacked the evidentiary capacity to respond to causality claims with
scientific authority. Into this evidence vacuum, the judicial system was
called upon to adjudicate vaccine causality --- a role for which courts
are institutionally ill-equipped, as legal standards of causality
(presumption, balance of probabilities) diverge fundamentally from
epidemiological standards (attributable risk, confidence intervals,
dose-response relationships).

The March 2026 SBS broadcast reporting the first judicially recognized
vaccine-related myocardial infarction death --- and the subsequent KDCA
appeal --- crystallized this dynamic. The court\'s presumption-based
ruling, issued in the absence of KDCA-generated active surveillance
data, was publicly received as scientific validation of vaccine harm.
The KDCA\'s appeal, in turn, was interpreted not as a legitimate
scientific objection but as institutional self-protection, further
eroding C1 and catalyzing C7.

A further consequence of the evidence vacuum is the qualitative
transformation of C4 (Calculation). As KDCA-generated safety data became
contextually non-credible, public calculation progressively excluded
official data as a valid input, reconfiguring around audit disclosures,
judicial rulings, and community-sourced injury accounts instead. We term
this the C1→C4 cascade: Confidence collapse does not halt calculation but
redirects it toward causal attribution and legal remedy rather than
prospective vaccination decisions (detailed in Supplementary S3.1.3).

***4.2.3 The Self-Reinforcing Distrust Loop***

These dynamics constitute a closed, self-reinforcing loop that operates
independently of individual vaccination decisions:

> \(1\) KDCA performs surveillance + compensation simultaneously
>
> \(2\) Active surveillance capacity atrophies → evidence vacuum
>
> \(3\) Courts fill the vacuum via presumption-based causality rulings
>
> \(4\) Judicial rulings are received as scientific authority (C7
> legitimation)
>
> \(5\) KDCA scientific rebuttals are discounted as self-interested (C1
> deepening)
>
> \(6\) Public demand for active surveillance grows, but institutional
> identity remains compensation-centered → return to (1)

This loop predicts that in societies where surveillance and compensation
are institutionally co-located, C1 and C7 will be structurally
co-produced --- not as a psychological accident but as a necessary
consequence of the institutional architecture. The present data, showing persistently elevated C1+C7 co-occurrence
rates across all discourse groups prior to the trigger events (FM_Direct:
50.0%; Court: 29.7%; Chronic: 24.5%), provide the first empirical evidence
consistent with this structural prediction in a real-world setting. The
post-event decline in absolute C1+C7 rates reflects compositional
dilution by a large influx of C1-dominant posts following the trigger
events, rather than a genuine reduction in the structural co-production
mechanism --- a distinction that is itself consistent with the
institutional capture hypothesis.

**4.3 The BAI Audit as Evidence-Backed Conspiracy Catalyst**

The 7C framework\'s Conspiracy dimension (C7) was originally
conceptualized as a belief in malicious intent unsupported by evidence
--- a departure from rational risk assessment into the domain of
unfalsifiable narrative (Geiger et al., 2021). The present findings
complicate this picture. As reported in Section 4.1.1, the BAI audit
provided official documentary support for the narrative that \'the
government knew and concealed it\': 1,285 foreign matter reports were
withheld from the MFDS while 1.42 million doses continued to be
administered under KDCA oversight. In this context, C7 narratives
acquired evidentiary scaffolding from the government\'s own audit, yet
the primary post-event response was C1 activation rather than C7
amplification (FM_Direct: 62.5% to 87.1% vs. 56.2% to 43.8% ns),
and residual C7 was almost entirely co-embedded within C1 (C1+C7:
42.3%; C7 alone: negligible). This suggests that official confirmation
of institutional failure drives targeted institutional distrust more
powerfully than generalized conspiracy belief.

We term this dynamic evidence-backed conspiracy catalysis: a process by
which official disclosures of institutional failure provide evidentiary
scaffolding for pre-existing conspiracy narratives, lowering the
psychological cost of transitioning from C1 (distrust) to C7
(conspiratorial belief). This distinction matters for public health
communication: conventional conspiracy inoculation strategies
(Lewandowsky & van der Linden, 2021) target psychologically motivated
reasoning against contrary evidence. Evidence-backed conspiracy
catalysis represents a different challenge --- one in which the evidence
itself is the vector, and inoculation against the narrative risks
appearing to deny the underlying institutional failures.\
The Court group, by contrast, illustrates a second mechanism: discourse
specificization. When a judicial event provides a named institutional
actor and a specific causal claim, diffuse conspiratorial framing is
displaced by targeted institutional distrust (C1) and defensive
calculation (C4). The pre-event Court C7 was disproportionately composed
of global anti-vaccine conspiracy content (transnational networks
referencing WEF, CCP, nanomaterials), which was numerically overwhelmed
by Korea-specific C1 content following the SBS broadcast. Together,
these two mechanisms --- catalysis in FM_Direct, specificization in
Court --- suggest that the relationship between institutional disclosure
events and C7 is not uniform but depends critically on the type of
disclosure: audit-type events feed C7 by validating opacity narratives,
while judicial-type events channel distrust into C1 and C4 by providing
concrete, attributable institutional actors.

The appropriate institutional response in this context is not
communication strategy revision but structural accountability: only
genuine evidence generation through independent active surveillance can
interrupt the C1→C7 transition pathway. As long as the KDCA cannot
produce prospective pharmacoepidemiological data that stands
independently of its compensation function, its communications will
remain structurally non-credible regardless of content.

**4.4 Implications for the 7C Framework**

The 7C framework was developed primarily as a model of individual
psychological antecedents of vaccination behavior (Geiger et al., 2021;
Betsch et al., 2018). The present findings suggest that in contexts of
sustained institutional failure, the 7C dimensions are not solely
psychological states but can be jointly produced by institutional
architecture. Two extensions are most directly supported by the
present data; four additional extensions are detailed in
Supplementary File S3.

First, evidence-backed conspiracy as a distinct C7 subtype: standard C7
measurement instruments (e.g., 5C/7C scales) do not distinguish between
conspiracy beliefs grounded in official disclosures of institutional
failure and those lacking any evidentiary basis. This distinction has
direct implications for intervention design: the former requires
institutional repair, while the latter is amenable to psychological
inoculation approaches (Lewandowsky & van der Linden, 2021).

Second, the behavior--attitude decoupling problem and the limits of C6:
the 7C framework implicitly assumes that observed vaccination behavior
reflects underlying attitudinal acceptance. However, Korea\'s high
vaccination coverage was achieved under conditions of mandatory vaccine
pass (방역패스) policies and pervasive social media-based peer
visibility of vaccination status --- a participatory surveillance
environment in which individuals simultaneously function as data
contributors and horizontal monitors of each other\'s health behaviors
(Albrechtslund, 2008). Under such conditions, elevated C6 (Compliance)
scores in discourse data may reflect not voluntary social norm alignment
but structural coercion and horizontal peer pressure, producing
behavioral compliance that is decoupled from attitudinal acceptance.
This decoupling limits the inferential value of C6 as a predictor of
genuine vaccination readiness in mandate-heavy public health contexts,
and suggests that future 7C applications should distinguish between
compliance grounded in attitudinal acceptance and compliance produced by
institutional or social coercion.

**4.5 Practical Implications for Public Health Communication**

The structural analysis presented above has direct implications for KDCA
communication strategy in the aftermath of the BAI audit disclosure.
Three practical recommendations follow from the empirical and
theoretical findings.

First, message credibility requires structural precondition.
Communication interventions targeting C1 (e.g., corrective messages
about vaccine safety, transparent disclosure of adverse event data) will
have limited efficacy as long as the KDCA simultaneously adjudicates
compensation. Structural separation of active surveillance from
compensation functions --- as practiced in the United States
(VAERS/v-safe vs. CICP) and the United Kingdom (Yellow Card vs. Vaccine
Damage Payment Scheme) --- is a prerequisite for restoring contextual
acceptance of safety communications.

Second, acknowledge the evidentiary legitimacy of distrust. In the
context of evidence-backed conspiracy catalysis, communication
strategies that deny or minimize the BAI audit findings will accelerate
C7 formation. Proactive acknowledgment of institutional failures, paired
with concrete structural remediation commitments, is more likely to
interrupt the C1→C7 transition than defensive messaging.

Third, group-specific communication targeting. The distinct 7C profiles
of FM_Direct (C1-dominant, with C7 co-embedded) and Court (C1+C4,
with C7 displacement) groups indicate that one-size-fits-all
communication is insufficient. FM_Direct audiences
require transparency on safety management procedures and independent
surveillance capacity; Court audiences additionally require
acknowledgment of the tension between judicial presumption standards and
epidemiological causality standards, and a credible commitment to
providing the scientific evidence the judiciary currently lacks.

Fourth, monitor the locus of scientific authority. A critical
precondition for effective public health communication is that the
communicating institution is recognized as a legitimate scientific
authority by its audience. The structural dynamics documented in this
study suggest that this precondition may no longer hold for the KDCA in
the domain of vaccine safety. Systematic longitudinal monitoring of
which institution the public recognizes as the most credible arbiter of
vaccine safety information --- the KDCA, the judiciary, the BAI, or
independent academic researchers --- would provide a sensitive early
indicator of credibility erosion and recovery (see Supplementary File S3
for a proposed survey operationalization). It should be noted that while
partisan political discourse did not precede or initiate the primary
hesitancy surge, the sustained parliamentary amplification during
March 10--19 likely contributed to prolonging institutional distrust
discourse beyond the immediate post-event window --- a distinction that
matters for communication strategy: the structural distrust preceded
politics, but politics subsequently extended its reach.

**4.6 Limitations**

Several limitations of this study warrant acknowledgment. First, the
data are drawn from two Naver channels --- blog posts and news article
comments --- and do not include Naver Café, which constitutes a
quantitatively substantial portion of vaccine-related discourse on the
platform. Café was excluded because the Naver Search API does not return
publication timestamps for Café articles, rendering temporal analysis
impossible. As the central research question concerns event-specific
discourse changes before and after two discrete trigger events, temporal
ordering is analytically indispensable and this exclusion was
unavoidable given current API constraints. It is worth noting that Naver
Café hosts several organized vaccine injury advocacy communities (e.g.,
코백회-affiliated groups), which are disproportionately active in
Compliance (C6) and Conspiracy (C7) discourse. The exclusion of Café may
therefore result in a conservative underestimation of C6 and C7
prevalence relative to the full Naver discourse ecosystem. Furthermore,
the present findings do not represent discourse on platforms such as
YouTube, X (formerly Twitter), or KakaoTalk open channels, and the
extent to which Naver blog and news comment discourse reflects broader
public opinion requires validation against multi-platform data.

Additionally, a three-stage relevance filtering pipeline was applied prior
to classification, reducing the corpus from 8,694 to 3,010 posts for the
primary analysis (Stage 1--2: 8,694 to 4,870; Stage 3 LLM semantic
filtering: 4,870 to 3,010, excluding pro-vaccine [n=12], irrelevant
[n=439], and politically partisan posts [n=1,409]). Stage 1--2 filtering
excluded news article texts (n=191), boilerplate spam posts with
recurrent footer patterns (n=514), and posts lacking Korea-specific
COVID-19 vaccination discourse markers (n=3,119).
While this improved corpus specificity, differential retention rates
across groups (FM_Direct: 43%; Court: 24%; Chronic: 53%) reflect the
higher proportion of globally-circulating conspiracy content in the Court
keyword set. The qualitative characterization of global-local C7
displacement in Section 4.1.4 is based on the Stage 1--2 filtered corpus
(n=4,870) and should be interpreted accordingly.

Second, the LLM classification pipeline achieved a macro F1 of 0.585 on
the English CAVES benchmark (v1.1.0, claude-haiku-4-5-20251001), with
particularly low performance on C4 (F1 = 0.393) and C7 (F1 = 0.403).
Korean-language classification performance was evaluated against a
50-item expert-coded gold standard (single expert coder, SC), yielding a
macro-average F1 of 0.548 across four scorable dimensions (C1: 0.778;
C4: 0.444; C6: 0.500; C7: 0.471; C2 not scorable, support=0). The C1↔C7
boundary ambiguity identified in the English error analysis persists in
Korean, as the linguistic markers distinguishing strong institutional
distrust from explicit conspiracy claims are similarly ambiguous in short
social media texts. This limitation is directionally conservative for our
main hypothesis: observed C1+C7 co-occurrence rates may underestimate
true co-occurrence if C7 precision is reduced by boundary
misclassification.

Third, the FM_Direct pre-event stratum comprised n=16 posts following
Stage 3 semantic filtering, due to the short data collection window
prior to the index event and the API 1,000-result ceiling
disproportionately affecting this high-volume keyword group. Pre-event
FM_Direct estimates should be interpreted with particular caution given
this constraint; the wide confidence interval for the C1 OR (4.07,
95% CI: 1.43--11.53) reflects this limitation directly.

Fourth, the lead researcher (S.C.) is affiliated with the KDCA, the
institution central to the structural critique developed in this
Discussion. This structural conflict of interest is fully disclosed in
the Ethics Statement. All analytical decisions were pre-registered in
the project plan and subject to independent co-author review to mitigate
potential bias.

Fifth, daily discourse volume reflects not only vaccine-specific activation
but also competing news agenda. Major external events occurring during the
observation period — including a geopolitical military incident (February 28)
and an oil price shock (March 6–9) — could in principle suppress
vaccine-related discourse volume through agenda displacement, producing
apparent declines in prevalence that reflect attentional competition rather
than genuine changes in public sentiment. To assess whether this mechanism
confounded the Court group's post-E2 C1 trajectory, we computed the
Pearson correlation between total corpus daily volume and Court C1
prevalence (r = 0.073), finding near-zero association. Furthermore,
Post-E2 Court C1 prevalence never fell below 50% on any observation day,
including days of minimal total volume (e.g., March 5–6: total n = 59).
These analyses confirm that the observed C1 elevation was not an artifact
of volume-driven compositional change. However, this limitation remains
relevant as a general design consideration for future infoveillance systems:
absolute volume decline should not be interpreted as resolution of underlying
distrust without first ruling out agenda displacement as an alternative
explanation.

Sixth, the relationship between partisan political discourse and hesitancy
persistence cannot be fully disentangled within the present cross-sectional
design. Although the temporal sequence confirms that political mobilization
did not initiate the primary hesitancy surge, the sustained parliamentary
amplification during March 10--19 temporally overlaps with the post-E2
hesitancy plateau. Whether this overlap reflects political discourse
prolonging hesitancy activation, or both responding independently to the
same structural conditions, cannot be determined from volume data alone.
Causal inference on this point would require panel survey data or
quasi-experimental designs exploiting variation in political exposure.

**4.7 Future Directions**

Four directions for future research --- including longitudinal natural
experiments on structural reform effects, cross-jurisdictional comparative
studies, survey-based construct validation, and path analysis of
inter-dimensional cascades --- are detailed in Supplementary File S3.

**4.8 Conclusion**

This study provides empirical evidence that the 2026 BAI audit
disclosure produced a significant and group-specific shift in the
architecture of vaccine hesitancy discourse on Korean social media,
characterized by a significant increase in C1 (Confidence) across all
three discourse groups and a concurrent decrease in C7 that reflects
compositional dilution by C1-dominant post-event content rather than
genuine conspiracy belief reduction. We interpret this pattern as reflecting not
primarily individual psychological processes but a structural condition
--- institutional capture of the 7C communication channel --- arising
from the co-location of active surveillance and compensation functions
within a single agency. Under this condition, official safety
disclosures function as evidence-backed conspiracy catalysts rather than
trust-restoring communications, and the judicial system substitutes for
the scientific authority the surveillance infrastructure fails to
produce.

The Korean case offers a critical lesson for global vaccine safety
governance: the quantity of compensation cannot substitute for the
quality of evidence generation. Until the structural condition of
genuine separation between surveillance and compensation functions is
realized, the self-reinforcing distrust loop documented in this study
will persist, independent of communication strategy, compensation
generosity, or political will.
