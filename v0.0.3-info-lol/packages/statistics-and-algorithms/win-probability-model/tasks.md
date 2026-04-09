# Tasks for Win Probability Model

- **Task:** Collect and prepare training dataset
  - **Description:** [Quality Mandate Required] Gather 10M+ ranked solo queue games from Riot API. Extract features at 1-minute intervals (gold diff, XP diff, towers, dragons, champion comp synergy). Label outcomes (win/loss). This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/win-probability-model/README.md`
  - **Dependencies:** Riot API access; data pipeline infrastructure; storage for 10M games
  - **Estimated effort:** XL (44–56 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Data engineer
  - **Milestone:** Phase 1 – Data Preparation

- **Task:** Engineer 30+ game state features
  - **Description:** [Quality Mandate Required] Design and calculate features from game timeline data: gold differential, XP gap, tower count, objective counts, death timers, gold/min trajectory, patch balance state, etc. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/win-probability-model/README.md`
  - **Dependencies:** Training dataset prepared; feature definitions finalized
  - **Estimated effort:** L (18–23 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Data scientist
  - **Milestone:** Phase 1 – Data Preparation

- **Task:** Train gradient-boosted win probability model
  - **Description:** [Quality Mandate Required] Build XGBoost model with 500 trees, max depth 8. Train on 8M games, validate on 1M, test on 1M. Target >75% accuracy on test set. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/win-probability-model/README.md`
  - **Dependencies:** Features computed; XGBoost training framework available; GPU resources
  - **Estimated effort:** XL (33–44 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Data scientist
  - **Milestone:** Phase 2 – Algorithm Implementation

- **Task:** Implement counterfactual inference for action attribution
  - **Description:** [Quality Mandate Required] Build system to estimate how removing an action (e.g., a death) changes win probability. Support per-action impact calculation. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/win-probability-model/README.md`
  - **Dependencies:** Win probability model trained; counterfactual simulation framework
  - **Estimated effort:** L (16–21 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Data scientist
  - **Milestone:** Phase 2 – Algorithm Implementation

- **Task:** Validate model calibration and accuracy
  - **Description:** [Quality Mandate Required] Test model on holdout test set. Verify calibration: "predicted 60% actually wins 60%". Test edge cases (early lead, 4v5, late stall). This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/win-probability-model/README.md`
  - **Dependencies:** Model training complete
  - **Estimated effort:** M (14–18 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Data scientist + QA analyst
  - **Milestone:** Phase 2 – Quality Assurance

## Cross‑Directory Task Links

- Model used in [Zone 3 - Timeline sentiment arc](../visual-design/zones/zone-3-timeline-narrative/tasks.md)
- Model used in [Zone 7 - Shadow match comparisons](../visual-design/zones/zone-7-comparative-insights/tasks.md)
