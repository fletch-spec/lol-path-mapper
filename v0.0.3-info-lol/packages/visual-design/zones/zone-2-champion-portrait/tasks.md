# Tasks for Zone 2 – Champion Portrait & Core Stats

- **Task:** Implement champion splash art display
  - **Description:** [Quality Mandate Required] Create framed champion splash art display (desaturated, runic circle border). Handle image loading, caching, and fallbacks. Ensure portrait maintains visual hierarchy without overwhelming zone. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/visual-design/zones/zone-2-champion-portrait/README.md`
  - **Dependencies:** Asset pipeline for champion art set up; visual design system complete
  - **Estimated effort:** M (9–11 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Zone 2 Implementation

- **Task:** Build five-ring performance dial (pentagon radar chart)
  - **Description:** [Quality Mandate Required] Implement interactive pentagon radar chart displaying Kill Participation, Gold Efficiency, Map Pressure Index, Survivability Quotient, and Momentum Impact. Support hover tooltips with calculation formulas and pro tips. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/visual-design/zones/zone-2-champion-portrait/README.md`
  - **Dependencies:** [Role Normalization algorithm](../../statistics-and-algorithms/role-positional-normalization/tasks.md) complete; charting library available
  - **Estimated effort:** L (18–23 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Zone 2 Implementation

- **Task:** Implement performance score central display
  - **Description:** [Quality Mandate Required] Create central number display (0-100 scale) with color coding (Poor/Below Avg/Average/Good/Elite). Show role-matched contextual interpretation of the composite score. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/visual-design/zones/zone-2-champion-portrait/README.md`
  - **Dependencies:** [Role Normalization algorithm](../../statistics-and-algorithms/role-positional-normalization/tasks.md) complete
  - **Estimated effort:** S (5–7 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Zone 2 Implementation

- **Task:** Create corner insight callout for dial
  - **Description:** [Quality Mandate Required] Display one contextual insight highlighting the player's relative strength/weakness (e.g., "Top 12% KP but weak map pressure"). Support dynamic text based on metric values. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/visual-design/zones/zone-2-champion-portrait/README.md`
  - **Dependencies:** Insight generation system ready; metrics computed
  - **Estimated effort:** M (7–9 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Zone 2 Implementation

- **Task:** Ensure Zone 2 colorblind accessibility
  - **Description:** [Quality Mandate Required] Apply colorblind-safe palettes to pentagon radar. Test with all four colorblind modes. Ensure all metric values are distinguishable without relying on color alone. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/visual-design/zones/zone-2-champion-portrait/README.md`
  - **Dependencies:** Zone 2 implementation complete; accessibility standards defined
  - **Estimated effort:** M (9–11 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Accessibility specialist + Designer
  - **Milestone:** Phase 2 – Quality Assurance

## Cross‑Directory Task Links

- Depends on [Visual Design framework tasks](../tasks.md) and [Zones overview tasks](../tasks.md)
- Five metrics depend on [Role Normalization](../../statistics-and-algorithms/role-positional-normalization/tasks.md) and [Win Probability](../../statistics-and-algorithms/win-probability-model/tasks.md) algorithms
- Insight callout depends on [Natural Language Generation](../../statistics-and-algorithms/natural-language-generation/tasks.md)
- Accessibility depends on [Accessibility compliance tasks](../../infrastructure/accessibility/tasks.md)
