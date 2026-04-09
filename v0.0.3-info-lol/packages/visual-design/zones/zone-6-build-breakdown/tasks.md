# Tasks for Zone 6 – Build & Ability Breakdown

- **Task:** Implement item path timeline (Gantt-style)
  - **Description:** [Quality Mandate Required] Create horizontal timeline showing each item purchase as a bar spanning its ownership duration. Add spike detection bands for items that caused >30% damage increase. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/visual-design/zones/zone-6-build-breakdown/README.md`
  - **Dependencies:** Item purchase timestamps; damage output per minute data available
  - **Estimated effort:** L (14–18 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Zone 6 Implementation

- **Task:** Build mythic comparison ghost line
  - **Description:** [Quality Mandate Required] Display alternative mythic's expected damage trajectory as ghost line alongside actual mythic. Support hover to compare stats and tooltip explaining choice impact. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/visual-design/zones/zone-6-build-breakdown/README.md`
  - **Dependencies:** [Build Adaptation Scoring](../../statistics-and-algorithms/build-adaptation-scoring/tasks.md) complete; damage oracle model available
  - **Estimated effort:** M (11–14 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Zone 6 Implementation

- **Task:** Display resource management metrics
  - **Description:** [Quality Mandate Required] Show mana waste index and cooldown utilization metrics. Include interpretation and comparison to role baseline. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/visual-design/zones/zone-6-build-breakdown/README.md`
  - **Dependencies:** Mana spend and ability cast data available; role baselines computed
  - **Estimated effort:** M (7–9 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Zone 6 Implementation

## Cross‑Directory Task Links

- Sub-tasks in [Ability Efficiency Rating tasks](ability-efficiency-rating/tasks.md)
- Mythic comparison depends on [Build Adaptation Scoring](../../statistics-and-algorithms/build-adaptation-scoring/tasks.md)
