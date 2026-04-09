# Tasks for Localization

- **Task:** Create terminology glossary for 14 languages
  - **Description:** [Quality Mandate Required] Define League-specific terms (CS, KDA, gank, roaming, etc.) in all 14 languages. Source from official League client terminology. Get professional translator review. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/infrastructure/localization/README.md`
  - **Dependencies:** Professional translators hired; League terminology documented
  - **Estimated effort:** L (16–21 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Localization manager + Translators
  - **Milestone:** Phase 2 – Localization

- **Task:** Implement region-specific number/date formatting
  - **Description:** [Quality Mandate Required] Auto-detect user region (IP/account settings). Format numbers (comma/period separators), dates (DD/MM vs. MM/DD), times (24h/12h), timezones. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/infrastructure/localization/README.md`
  - **Dependencies:** All metric displays finalized; backend locale detection available
  - **Estimated effort:** M (11–14 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Localization

- **Task:** Hire professional translators for all 14 languages
  - **Description:** [Quality Mandate Required] Recruit native speakers with gaming experience. Brief on project scope, brand tone, League terminology. Set up translation QA process. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/infrastructure/localization/README.md`
  - **Dependencies:** Budget approved; terminology glossary ready
  - **Estimated effort:** M (9–11 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Localization manager
  - **Milestone:** Phase 2 – Localization

- **Task:** Translate all UI text and metric names
  - **Description:** [Quality Mandate Required] Professional translation of all buttons, headings, metric labels, tooltips. Use translation management tool (Crowdin) for version control and review. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/infrastructure/localization/README.md`
  - **Dependencies:** Translators hired; UI text finalized; terminology glossary ready
  - **Estimated effort:** XL (44–56 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Professional translators
  - **Milestone:** Phase 2 – Localization

- **Task:** Translate auto-generated narrative text and insights
  - **Description:** [Quality Mandate Required] Adapt templates and train language-specific NLG models. Translate improvement prompts, parting shots, event annotations. Maintain emotional tone in each language. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/infrastructure/localization/README.md`
  - **Dependencies:** [Natural Language Generation](../statistics-and-algorithms/natural-language-generation/tasks.md) complete; translators ready
  - **Estimated effort:** XL (56–67 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** ML engineer + Translators
  - **Milestone:** Phase 3 – Global Expansion

- **Task:** Implement localization build and deployment
  - **Description:** [Quality Mandate Required] Set up CI/CD pipeline for translation updates. Test all 14 language builds. Automate regional variable selection (numbers, dates, timezones). This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/infrastructure/localization/README.md`
  - **Dependencies:** All translations complete; CI/CD framework available
  - **Estimated effort:** M (11–14 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** DevOps engineer
  - **Milestone:** Phase 3 – Deployment

- **Task:** Conduct regional testing and validation
  - **Description:** [Quality Mandate Required] Test with native speakers in each region. Verify natural phrasing, cultural appropriateness, and correct formatting (numbers, dates). Iterate on feedback. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/infrastructure/localization/README.md`
  - **Dependencies:** All translations complete; testing team recruited
  - **Estimated effort:** L (18–23 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** QA team + Translators
  - **Milestone:** Phase 3 – Quality Assurance

## Cross‑Directory Task Links

- Text translation impacts all [Visual Design zones](../visual-design/zones/tasks.md)
- NLG translation feeds [Zone 3 narratives](../visual-design/zones/zone-3-timeline-narrative/tasks.md) and [Zone 7 insights](../visual-design/zones/zone-7-comparative-insights/tasks.md)
