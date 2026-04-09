# Tasks for Zone 5 – Positioning & Vision Intelligence

- **Task:** Implement Summoner's Rift heatmap visualization
  - **Description:** [Quality Mandate Required] Create 600×600px map replica with Gaussian KDE heatmap overlay showing champion position density. Support color gradient (blue → cyan → yellow → red). This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/visual-design/zones/zone-5-positioning-vision/README.md`
  - **Dependencies:** [Computer Vision heatmap data](computer-vision-heatmap/tasks.md) available; map coordinate system established
  - **Estimated effort:** L (16–21 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Zone 5 Implementation

- **Task:** Create game-phase toggle system
  - **Description:** [Quality Mandate Required] Implement buttons to toggle between Laning (0-14), Mid (14-25), and Late (25+) game phase overlays. Update heatmap visualization on toggle. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/visual-design/zones/zone-5-positioning-vision/README.md`
  - **Dependencies:** Heatmap implementation complete; phase-segmented position data available
  - **Estimated effort:** M (7–9 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Zone 5 Implementation

- **Task:** Display CV-derived metrics (brush time, proximity, click dispersion, vision crossings)
  - **Description:** [Quality Mandate Required] Render metric cards around heatmap showing brush dwelling, wall proximity, mouse click pattern, and vision line crossings. Include interpretations. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/visual-design/zones/zone-5-positioning-vision/computer-vision-heatmap/README.md`
  - **Dependencies:** [Computer Vision metrics](computer-vision-heatmap/tasks.md) computed; metric definitions finalized
  - **Estimated effort:** M (9–11 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Zone 5 Implementation

- **Task:** Implement ward placement visualization
  - **Description:** [Quality Mandate Required] Overlay green dots for placed wards, red dots for cleared wards, and lines for vision chains on the heatmap. Support click to see ward details. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/visual-design/zones/zone-5-positioning-vision/ward-placement-intelligence/README.md`
  - **Dependencies:** Ward placement data available; vision chain calculation complete
  - **Estimated effort:** M (9–11 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Zone 5 Implementation

## Cross‑Directory Task Links

- Sub-tasks in [Computer Vision heatmap tasks](computer-vision-heatmap/tasks.md) and [Ward placement tasks](ward-placement-intelligence/tasks.md)
- Heatmap data sourced from [Computer Vision](../../statistics-and-algorithms/computer-vision-heatmaps/tasks.md)
