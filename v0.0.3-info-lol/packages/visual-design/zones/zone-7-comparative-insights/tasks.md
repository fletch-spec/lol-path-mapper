# Tasks for Zone 7 – Comparative & Predictive Insights

- **Task:** Implement percentile rankings table
  - **Description:** [Quality Mandate Required] Display 5-row table showing player's value vs. role average vs. percentile rank. Include interpretation of each ranking (strengths vs. weaknesses). This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/visual-design/zones/zone-7-comparative-insights/README.md`
  - **Dependencies:** Percentile ranking data available from [Role Normalization](../../statistics-and-algorithms/role-positional-normalization/tasks.md); benchmarks computed
  - **Estimated effort:** M (9–11 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Zone 7 Implementation

- **Task:** Build shadow match comparison display
  - **Description:** [Quality Mandate Required] Find and display pro-play/high-elo game with similar match state at 15 min. Show pro player name, champion matchup, key differences, and projected win probability. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/visual-design/zones/zone-7-comparative-insights/README.md`
  - **Dependencies:** Pro play game database; [Win Probability Model](../../statistics-and-algorithms/win-probability-model/tasks.md) complete; matching algorithm implemented
  - **Estimated effort:** L (18–23 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Backend engineer
  - **Milestone:** Phase 2 – Zone 7 Implementation

- **Task:** Generate improvement prompt
  - **Description:** [Quality Mandate Required] Procedurally create actionable improvement suggestion targeting lowest-scoring metric. Support 2-3 specific, achievable recommendations. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/visual-design/zones/zone-7-comparative-insights/README.md`
  - **Dependencies:** [Natural Language Generation](../../statistics-and-algorithms/natural-language-generation/tasks.md) complete; metric rankings available
  - **Estimated effort:** M (9–11 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Zone 7 Implementation

- **Task:** Implement parting shot generation
  - **Description:** [Quality Mandate Required] Generate poetic single-sentence summary based on performance profile. Support emotional tone matching game outcome and player performance level. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/visual-design/zones/zone-7-comparative-insights/README.md`
  - **Dependencies:** [Natural Language Generation](../../statistics-and-algorithms/natural-language-generation/tasks.md) with VAE variation complete
  - **Estimated effort:** M (9–11 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Zone 7 Implementation

## Cross‑Directory Task Links

- Depends on [Visual Design framework](../tasks.md) and [Zones overview](../tasks.md)
- Percentile rankings depend on [Role Normalization](../../statistics-and-algorithms/role-positional-normalization/tasks.md)
- Shadow match depends on [Win Probability Model](../../statistics-and-algorithms/win-probability-model/tasks.md)
- Improvement and parting shot depend on [Natural Language Generation](../../statistics-and-algorithms/natural-language-generation/tasks.md)
