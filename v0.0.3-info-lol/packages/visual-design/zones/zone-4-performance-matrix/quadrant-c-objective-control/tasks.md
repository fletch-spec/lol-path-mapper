# Tasks for Quadrant C – Objective Control & Roaming

- **Task:** Implement vision denial ratio metric
  - **Description:** [Quality Mandate Required] Calculate and display (control wards placed + sweeper clears) / (enemy wards in jungle). Show interpretation with comparison to role average. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/visual-design/zones/zone-4-performance-matrix/quadrant-c-objective-control/README.md`
  - **Dependencies:** Ward placement and vision data available
  - **Estimated effort:** S (3–5 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Zone 4 Implementation

- **Task:** Create objective participation heatmap
  - **Description:** [Quality Mandate Required] Render mini-map replica showing proximity circles to each objective (dragon, baron, turret). Use circle size/color to indicate how close player was at objective contest moments. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/visual-design/zones/zone-4-performance-matrix/quadrant-c-objective-control/README.md`
  - **Dependencies:** Map coordinate system; objective death timestamps; positional data available
  - **Estimated effort:** M (9–11 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Zone 4 Implementation

- **Task:** Implement roaming score calculation and display
  - **Description:** [Quality Mandate Required] Calculate roaming score (roaming K+A / game minutes × 0.1) with plate loss penalty. Display with interpretation and comparison to baseline. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/visual-design/zones/zone-4-performance-matrix/quadrant-c-objective-control/README.md`
  - **Dependencies:** Roaming event detection; match timeline data available
  - **Estimated effort:** M (7–9 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Zone 4 Implementation

## Cross‑Directory Task Links

- Depends on [Zone 4 overview](../tasks.md)
- Heatmap depends on [Computer Vision](../../../statistics-and-algorithms/computer-vision-heatmaps/tasks.md) for position tracking
