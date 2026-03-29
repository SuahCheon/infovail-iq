# **2. Methods**

*[DRAFT — v0.1.0, 2026-03-23]*

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

To ensure analytical focus on Korean COVID-19 vaccine hesitancy discourse, a two-stage relevance filtering pipeline was applied prior to classification.

In the first stage, all posts from the `news` channel (n = 191) were excluded, as news article texts represent institutional media output rather than individual public discourse.

In the second stage, keyword-based relevance filtering was applied to the remaining posts. A post was retained if its title or body contained at least one of 14 Korea-specific COVID-19 vaccination discourse markers, defined a priori as lexical patterns directly referencing Korean institutional actors, events, or policy contexts (e.g., "코로나 백신", "이상반응", "감사원", "방역패스", "정은경", "코백회"). Prior to this match, posts containing a recurrent boilerplate footer pattern ("영구적인 코로나 봉쇄부터 백신 여권") were excluded (n = 514), as these were identified as originating from a single blogger whose posts systematically appended a globally-circulating anti-vaccine conspiracy text regardless of post topic. Posts failing both the boilerplate exclusion check and the must-have pattern match were flagged as `is_relevant = 0` (n = 3,119 not matching must-have patterns; n = 92 matching hard-exclusion patterns for entirely irrelevant content). Flagged posts were retained in the database but excluded from all classification and analysis steps.

This filtering reduced the analysis corpus from 8,694 to 4,870 posts (56.0% retained). The differential retention rate across discourse groups (FM_Direct: 43%; Court: 24%; Chronic: 53%) reflected the higher proportion of globally-circulating conspiracy content in the Court keyword set, which is discussed as a finding in its own right in Section 4.1.4.

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

The classification prompt incorporated five few-shot examples per dimension, selected from the CAVES training set to represent boundary cases between adjacent dimensions (particularly C1↔C4 and C1↔C7). Few-shot examples were drawn verbatim from the CAVES dataset (Poddar et al., 2022) and selected to maximize coverage of the C1↔C4 and C1↔C7 boundary regions identified in pilot testing. The CAVES tweet IDs for selected examples are documented in PROMPT_REGISTRY.md.

### **2.6.3 Classification Execution**

All Korean-language classification was performed using the Anthropic Batch API to minimize latency and cost. Prompt caching was applied to the system prompt component to reduce token processing costs across batches. Classification was applied to the post-filtering corpus of 4,870 posts. Posts for which the LLM response could not be parsed as valid JSON (parse errors; n = 129, 2.6%) were assigned all-zero labels as a conservative fallback. Two posts were lost due to batch processing errors (0.04%). Parse error and batch error rates are reported in Table 4.

## **2.7 English Benchmark Validation**

Prior to Korean-language application, the classification pipeline was benchmarked on the English CAVES test set (n = 1,846) to establish classifier reliability. Per-dimension precision, recall, and F1 scores were computed against CAVES human-annotated ground truth labels using the validated CAVES→7C mapping (Section 2.5). Macro-average F1 was computed across the five active dimensions. The resulting performance metrics (macro F1 = 0.585) are presented in Table 4 of the Results section.

## **2.8 Korean-Language Gold Standard Validation**

Korean-language classification performance was evaluated against an expert-coded gold standard sample. A stratified random sample of 50 posts was drawn from the post-filtering corpus using proportional allocation across six strata (discourse group × collection period: 3 groups × 2 periods). Sampling used a fixed random seed (seed = 42) to ensure reproducibility. Each post was coded by the lead author (S.C.), a Korean-English bilingual physician-epidemiologist with ten years of experience in vaccine safety surveillance and adverse event causality assessment (single expert coder design). Nine posts assigned all-zero labels by the expert coder (commercial advertisements for vaccine side-effect treatment services, n = 2; topically irrelevant content, n = 4; pro-vaccination content, n = 3) were excluded from F1 calculation, yielding a final evaluation set of 41 posts. Per-dimension F1 scores were computed by matching expert-coded labels against LLM predictions for the same posts, identified by post ID. Overall macro-average F1 was computed across four scorable dimensions (C2 excluded: support = 0).

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
