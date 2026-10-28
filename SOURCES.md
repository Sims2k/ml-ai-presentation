# Source anchors and teaching boundaries

- Kalinowski et al., *Engenharia de Software para Ciência de Dados*: assigned
  Chapters 13–14 (architecture/serving and software design); Chapters 12 and 16
  are explicitly identified as supporting reading.
- Bass et al., *Engineering AI Systems* (2025): Chapters 9–11 (security,
  privacy/fairness, observability) and Chapter 14 (bank customer churn).
- Nazir et al., *Architecting ML-enabled systems*, JSS 207 (2024): selected
  architectural decisions and discussion, DOI 10.1016/j.jss.2023.111860.
- Bucaioni, Kazman & Pelliccione, quality checklist, JSS 231 (2026): selected
  published Table 1 entries, DOI 10.1016/j.jss.2025.112612. The separately
  catalogued corrigendum DOI 10.1016/j.jss.2025.112743 has not been read.
- Breck et al., *The ML Test Score*: monitoring, canary, rollback and tests.
- NIST AI 100-2e2025 (adversarial ML), SP 800-207 (enforcement boundaries),
  SP 800-226 (differential privacy assumptions).
- Krawczyk & Cano (2018), Figure 2: original temporal drift illustration;
  see THIRD_PARTY.md for the supplied link and retrieval provenance.
- SciPy, `ks_2samp` reference: two-sample KS interpretation and continuous-input
  assumptions, https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ks_2samp.html .
  This supports the short speaker-note caveat about discrete counts and ties.

Slide footers cite the underlying readings and identify teaching adaptations.
Personal study notes are preparation material, not cited as primary sources.

These anchors were established during the original preparation; the visual
revision does not claim new complete reads of all books or papers.

Monthly scoring, a next-30-day target, Ana/C042, 0.70, M1/M2, B017/B017-R1,
CRM migration and campaign rules are illustrative teaching choices. The larger
scatter diagrams use 15 invented feature positions and mature outcomes to
isolate a changed relationship. Perfect separation is a deliberate simplification,
not a claim about real churn data or model performance.

No live Airflow/MLflow run, repaired score, observed retention benefit or new
customer outcome is reported. The public repository excludes library source PDFs.

## Day 2 — agentic AI architecture

- Barbaste, Darrigol, Vu & Wiltberger (2026), *Harness Engineering: Anatomy,
  Architecture, and Evolution of Coding Agents*, arXiv:2609.00006.
- Liu, Lo, Lu, Zhu et al. (2025), *Agent Design Pattern Catalogue*, JSS 220,
  arXiv:2405.10467.
- Lu, Zhao, Liu, Zhang et al. (2026), *AgentArcEval*, JSS 232, 112656,
  DOI 10.1016/j.jss.2025.112656; accessible manuscript:
  https://arxiv.org/html/2510.21031v1 . Sections 4–6 support the process,
  scenario catalogue and qualitative Luna case analysis.
- Mohsenimofidi, Galster, Treude & Baltes (2026), *Context Engineering for AI
  Agents in Open-Source Software*, MSR 2026, arXiv:2510.21413.
- Earendil Engineering (1 October 2026), *Pi Durable*,
  https://earendil.com/posts/pi-durable/ . Source for task checkpoints,
  recovery and replay semantics; system description, not an independent benchmark.
- SEI, *Architecture Tradeoff Analysis Method Collection*,
  https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/ .
  Supports the definition of ATAM and its stakeholder/scenario/trade-off analysis.
- Hermes Agent documentation and the harness study support the system examples;
  the 69% token figure is a single user report (issue #5563), not a benchmark.

The session/durable/always-on spectrum and scenario-to-harness mapping are the
presentation team's synthesis. Luna's 95% accuracy and citation figures are
acceptance requirements, not measured results. Optional preparation examples in
speaker notes are labelled teaching illustrations. Study-brief reading locations
are recorded in `preparation/README.md`.
