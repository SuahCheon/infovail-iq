# Infovail-IQ

### ⚠️ Disclaimer

*This is a personal research project conducted by the author. The views, thoughts, and opinions expressed in this project belong solely to the author and do not necessarily reflect the official policy or position of the Korea Disease Control and Prevention Agency (KDCA) or any other agency/organization.*

> **Multi-Layered AI Infoveillance for Public Health Policy**
>
> *"Beyond Sentiment Analysis: Decoding the Architecture of Public Distrust through CAVES-based Intelligence."*

Infovail-IQ automates the **WHO CAVES framework** for vaccine hesitancy using compact LLMs, transforming social media data into actionable policy intelligence. It offers a cost-effective and scalable solution for real-time infodemic management, specifically tailored for both advanced health agencies and Low- and Middle-Income Countries (LMICs).

---

## Core Philosophy: Bounded Autonomy

Infovail-IQ operates on the principle of **Bounded Autonomy**. It does not aim to replace human decision-makers but rather to provide a "structured guide" by decomposing complex public sentiments into manageable, evidence-based policy signals.

---

## Architecture

The system processes data through four distinct layers to bridge the gap between monitoring and decision-making:

* **Layer 1: Aggregation** (The "What")
  — Sentiment distribution, CAVES type ratios, and misinformation detection using PH-LLM-3B.

* **Layer 2: Co-occurrence Analysis** (The "Structure")
  — Analyzes how concerns cluster together (e.g., Government Distrust + Side Effects) using Phi coefficients to reveal the underlying architecture of distrust.

* **Layer 3: Temporal Dynamics** (The "When")
  — Tracks shifts in public opinion before and after official responses to evaluate intervention efficacy and identify leading indicators of emerging concerns.

* **Layer 4: Policy Intelligence** (The "Action")
  — Generates weekly policy briefings via Claude API, including behavioral directives and counter-messaging strategies based on integrated insights from Layers 1–3.

---

## Current PoC Scenario

**2026 COVID-19 Vaccine Contamination Audit** (South Korea)
— Board of Audit report on 1,285 foreign substance cases in vaccines, triggering a complex public trust crisis.

---

## Roadmap

- [ ] **PoC1** — Local model validation & prompt engineering
- [ ] **PoC2** — Policy intelligence dashboard & 4-week operational trial
- [ ] **Retrospective evaluation** — System recommendations vs. actual KDCA responses
- [ ] **Publication** — Target: *JMIR Infodemiology* / *IJMI*

---

## Author

**Suah Cheon, MD** — Deputy Director at KDCA
Public Health Practitioner & Researcher
Focus: Pharmacovigilance, AI-driven Public Health, System Architecture

## License

[MIT](LICENSE)
