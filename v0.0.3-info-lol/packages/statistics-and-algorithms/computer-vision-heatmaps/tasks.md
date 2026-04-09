# Tasks for Computer Vision Heatmaps

- **Task:** Train object detection model for champion tracking
  - **Description:** [Quality Mandate Required] Fine-tune YOLO or custom CNN on League champion sprites. Achieve >85% detection confidence on replay footage. Validate against known positions. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/computer-vision-heatmaps/README.md`
  - **Dependencies:** 10k+ manually annotated champion frames; YOLO/CNN framework available
  - **Estimated effort:** XL (33–44 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Machine learning engineer
  - **Milestone:** Phase 2 – Algorithm Implementation

- **Task:** Implement position density heatmap calculation
  - **Description:** [Quality Mandate Required] Build Gaussian KDE system to compute position density from tracked bounding boxes. Support phase-based segmentation (laning/mid/late). This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/computer-vision-heatmaps/README.md`
  - **Dependencies:** Position tracking model trained; KDE library available
  - **Estimated effort:** L (14–18 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Data scientist
  - **Milestone:** Phase 2 – Algorithm Implementation

- **Task:** Calculate advanced positioning metrics
  - **Description:** [Quality Mandate Required] Compute brush dwelling time, wall proximity, mouse click dispersion, and vision line crossings. Normalize metrics against player baselines. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/computer-vision-heatmaps/README.md`
  - **Dependencies:** Position tracking complete; map terrain data available
  - **Estimated effort:** M (11–14 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Data engineer
  - **Milestone:** Phase 2 – Algorithm Implementation

- **Task:** Validate CV accuracy against API data
  - **Description:** [Quality Mandate Required] Compare CV-derived positions to Riot API official positions on 100 test games. Achieve <15px average error. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/computer-vision-heatmaps/README.md`
  - **Dependencies:** CV model complete; API position comparison framework available
  - **Estimated effort:** M (9–11 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** QA analyst
  - **Milestone:** Phase 2 – Quality Assurance

## Cross‑Directory Task Links

- Heatmap visualization depends on [Zone 5 - Positioning & Vision](../visual-design/zones/zone-5-positioning-vision/tasks.md)
