# Tasks for Natural Language Generation

- **Task:** Create event annotation templates
  - **Description:** [Quality Mandate Required] Write templates for kill, death, objective, and teamfight events. Format: "{timestamp} — {event_type} {qualifier} {outcome} {strategic_comment}". Create 10+ variant templates per event type. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/natural-language-generation/README.md`
  - **Dependencies:** Event types defined; brand voice guide finalized
  - **Estimated effort:** M (9–11 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Content strategist
  - **Milestone:** Phase 2 – Algorithm Implementation

- **Task:** Train VAE on professional commentary
  - **Description:** [Quality Mandate Required] Collect 100k LCS/pro league broadcast transcripts. Train VAE to learn natural phrasing and tone variations. Support sampling for diverse generation. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/natural-language-generation/README.md`
  - **Dependencies:** 100k transcript dataset; VAE framework available
  - **Estimated effort:** XL (33–44 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** ML engineer
  - **Milestone:** Phase 2 – Algorithm Implementation

- **Task:** Build template instantiation system
  - **Description:** [Quality Mandate Required] Implement template variable substitution (champion names, kill types, positions, gold values). Support conditional logic for different game states. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/natural-language-generation/README.md`
  - **Dependencies:** Templates created; match data available
  - **Estimated effort:** M (9–11 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Backend engineer
  - **Milestone:** Phase 2 – Algorithm Implementation

- **Task:** Implement VAE stylistic variation sampling
  - **Description:** [Quality Mandate Required] Use trained VAE to generate natural variants of templated text. Select highest-confidence variation for display. Support multiple samples for testing. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/natural-language-generation/README.md`
  - **Dependencies:** VAE training complete; template system ready
  - **Estimated effort:** M (11–14 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** ML engineer
  - **Milestone:** Phase 2 – Algorithm Implementation

- **Task:** Extend NLG to support 14 languages
  - **Description:** [Quality Mandate Required] Hire professional translators to adapt templates and train language-specific VAE models for each language. Maintain factual accuracy across translations. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/natural-language-generation/README.md`
  - **Dependencies:** English NLG complete; [Localization infrastructure](../../infrastructure/localization/tasks.md) ready; professional translators hired
  - **Estimated effort:** XL (56–67 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** ML engineer + Linguists
  - **Milestone:** Phase 3 – Global Expansion

- **Task:** Validate NLG output for coherence and accuracy
  - **Description:** [Quality Mandate Required] Test 1000 generated event descriptions for grammatical correctness, factual accuracy, and readability. Achieve >90% coherence score. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/natural-language-generation/README.md`
  - **Dependencies:** NLG system complete
  - **Estimated effort:** M (11–14 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** QA analyst + Linguist
  - **Milestone:** Phase 2 – Quality Assurance

## Cross‑Directory Task Links

- Event narratives used in [Zone 3 - Timeline](../visual-design/zones/zone-3-timeline-narrative/tasks.md)
- Improvement prompts used in [Zone 7 - Comparative Insights](../visual-design/zones/zone-7-comparative-insights/tasks.md)
- Parting shot used in [Zone 7 - Comparative Insights](../visual-design/zones/zone-7-comparative-insights/tasks.md)
