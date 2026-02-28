# Infovail-IQ

### ⚠️ Disclaimer

*This is a personal research project conducted by the author. The views, thoughts, and opinions expressed in this project belong solely to the author and do not necessarily reflect the official policy or position of the Korea Disease Control and Prevention Agency (KDCA) or any other agency/organization.*

> **Multi-Layered AI Infoveillance for Public Health Policy**

Infovail-IQ automates the **WHO CAVES framework** for vaccine hesitancy using compact LLMs, transforming social media data into actionable policy intelligence. The system goes beyond simple sentiment monitoring by analyzing the *structure* and *dynamics* of public concerns to generate evidence-based crisis communication strategies.

---

## Architecture

```
Layer 1: Aggregation       →  "What is happening now?"
Layer 2: Co-occurrence     →  "Which concerns are connected?"
Layer 3: Temporal Dynamics →  "When to intervene?"
Layer 4: Policy Generation →  "What specifically to do?"
```

Compact LLMs (3B parameters, quantized) classify Korean-language text across sentiment, misinformation, and 7 CAVES concern types. Layers 2–3 analyze concern co-occurrence patterns and temporal shifts. Layer 4 (Claude API) synthesizes all layers into weekly policy briefings with behavioral directives.

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

**Suah Cheon. MD**
Deputy Director at KDCA | Public Health Practitioner & Researcher
Focus: Pharmacovigilance, AI-driven Public Health, System Architecture.

## License

[MIT](LICENSE)
