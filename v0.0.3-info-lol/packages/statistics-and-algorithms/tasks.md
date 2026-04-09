# Tasks for Statistics & Algorithms Package

- **Task:** Implement computer vision heatmap system
  - **Description:** [Quality Mandate Required] Build champion position tracking from replay files using object detection. Track positions at 2 fps, validate against API data (<15px error target). This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/computer-vision-heatmaps/README.md`
  - **Dependencies:** Replay file access; YOLO/CNN model available; position validation framework
  - **Estimated effort:** XL (44–56 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Machine learning engineer
  - **Milestone:** Phase 2 – Algorithm Implementation

- **Task:** Build win probability model
  - **Description:** [Quality Mandate Required] Train gradient-boosted model on 10M+ games to predict win probability from game state. Implement counterfactual inference for action attribution. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/win-probability-model/README.md`
  - **Dependencies:** 10M+ game dataset; feature engineering framework; XGBoost training infrastructure
  - **Estimated effort:** XL (67–89 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Data scientist
  - **Milestone:** Phase 2 – Algorithm Implementation

- **Task:** Implement role-positional normalization
  - **Description:** [Quality Mandate Required] Run PCA on 20 match statistics to identify role archetypes. Create K-Means clustering to assign each player to an archetype. Update weekly post-patch. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/role-positional-normalization/README.md`
  - **Dependencies:** Historical match data; PCA/K-Means library; weekly automation framework
  - **Estimated effort:** L (28–37 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Data scientist
  - **Milestone:** Phase 2 – Algorithm Implementation

- **Task:** Build natural language generation system
  - **Description:** [Quality Mandate Required] Create template-based event generation + VAE for stylistic variation. Train VAE on 100k LCS transcripts. Support 14 language variants. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/natural-language-generation/README.md`
  - **Dependencies:** VAE training framework; LCS transcript dataset; 14-language translation pipeline
  - **Estimated effort:** XL (56–67 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** ML engineer + Linguist
  - **Milestone:** Phase 2 – Algorithm Implementation

- **Task:** Implement build adaptation scoring
  - **Description:** [Quality Mandate Required] Train Deep Q-Network on 10k high-elo games to learn optimal itemization. Evaluate player's actual items against oracle model. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/build-adaptation-scoring/README.md`
  - **Dependencies:** RL training framework; 10k game dataset; oracle win probability model
  - **Estimated effort:** XL (44–56 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Reinforcement learning engineer
  - **Milestone:** Phase 2 – Algorithm Implementation

- **Task:** Validate all algorithm implementations
  - **Description:** [Quality Mandate Required] Test each algorithm for accuracy, latency, and correctness. Ensure heatmaps <15px error, win prob >75% accuracy, NLG coherence >90%. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/README.md`
  - **Dependencies:** All algorithm implementations complete
  - **Estimated effort:** XL (56–78 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** QA analyst + Data scientist
  - **Milestone:** Phase 2 – Quality Assurance

## Cross‑Directory Task Links

- All algorithms feed into [Visual Design zones](../visual-design/zones/tasks.md)
- Validation must precede [Integration tasks](../tasks.md)
