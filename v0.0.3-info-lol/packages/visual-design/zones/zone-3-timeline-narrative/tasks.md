# Tasks for Zone 3 – Timeline Narrative

- **Task:** Implement momentum wave visualization
  - **Description:** [Quality Mandate Required] Create continuous bezier curve showing gold differential delta over match duration. Support color gradient (red → gray → gold). Add annotations for kills, deaths, and objectives. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/visual-design/zones/zone-3-timeline-narrative/README.md`
  - **Dependencies:** Match timeline data available; charting library supports bezier curves
  - **Estimated effort:** L (16–21 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Zone 3 Implementation

- **Task:** Create event strip icon layer
  - **Description:** [Quality Mandate Required] Render event icons (kill, death, turret, dragon, power spike) at appropriate timeline positions. Support size scaling for multikills and colored borders for participation. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/visual-design/zones/zone-3-timeline-narrative/README.md`
  - **Dependencies:** Match timeline data available; icon set created
  - **Estimated effort:** M (11–14 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Zone 3 Implementation

- **Task:** Build state annotation system
  - **Description:** [Quality Mandate Required] Display auto-generated natural language callouts for key match moments. Support hover/click for details. Ensure callouts appear at correct timeline positions. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/visual-design/zones/zone-3-timeline-narrative/README.md`
  - **Dependencies:** [Natural Language Generation](../../statistics-and-algorithms/natural-language-generation/tasks.md) complete; match event detection available
  - **Estimated effort:** M (11–16 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Zone 3 Implementation

- **Task:** Implement sentiment arc (win probability impact band)
  - **Description:** [Quality Mandate Required] Render thin color-coded band showing win probability impact over time. Use green for positive swings, red for negative. Add hover tooltips showing impact percentage. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/visual-design/zones/zone-3-timeline-narrative/README.md`
  - **Dependencies:** [Win Probability Model](../../statistics-and-algorithms/win-probability-model/tasks.md) complete
  - **Estimated effort:** M (9–11 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Zone 3 Implementation

- **Task:** Ensure timeline accessibility
  - **Description:** [Quality Mandate Required] Add text alternatives for all visual elements. Support keyboard navigation through timeline events. Implement screen reader descriptions of momentum and sentiment. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/visual-design/zones/zone-3-timeline-narrative/README.md`
  - **Dependencies:** Timeline implementation complete
  - **Estimated effort:** M (11–14 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Accessibility specialist
  - **Milestone:** Phase 2 – Quality Assurance

## Cross‑Directory Task Links

- Depends on [Visual Design framework](../tasks.md) and [Zones overview](../tasks.md)
- State annotations depend on [Natural Language Generation](../../statistics-and-algorithms/natural-language-generation/tasks.md)
- Sentiment arc depends on [Win Probability Model](../../statistics-and-algorithms/win-probability-model/tasks.md)
