# Tasks for Build Adaptation Scoring

- **Task:** Collect high-elo game dataset for training
  - **Description:** [Quality Mandate Required] Gather 10k Masters+ ranked games with full item purchase timelines and gold states at each recall. Extract decision states and outcomes. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/build-adaptation-scoring/README.md`
  - **Dependencies:** Riot API access; item purchase tracking from match timeline
  - **Estimated effort:** M (11–14 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Data engineer
  - **Milestone:** Phase 1 – Data Preparation

- **Task:** Build win probability oracle model
  - **Description:** [Quality Mandate Required] Train XGBoost to predict 5-minute win probability change given game state + proposed item. Use this as reward signal for RL training. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/build-adaptation-scoring/README.md`
  - **Dependencies:** 10k game dataset; [Win Probability Model](../win-probability-model/tasks.md) framework available
  - **Estimated effort:** L (16–21 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Data scientist
  - **Milestone:** Phase 2 – Algorithm Implementation

- **Task:** Train Deep Q-Network for optimal itemization
  - **Description:** [Quality Mandate Required] Train DQN on 10k games where state = game situation, action = item choice, reward = oracle 5-min win prob change. Learn Q-function mapping state→action values. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/build-adaptation-scoring/README.md`
  - **Dependencies:** Oracle model complete; RL training framework; GPU resources
  - **Estimated effort:** XL (39–50 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Reinforcement learning engineer
  - **Milestone:** Phase 2 – Algorithm Implementation

- **Task:** Implement build adaptation scoring calculation
  - **Description:** [Quality Mandate Required] For each recall in a new game, extract state, compute optimal item via Q-Network, compare to actual item, compute reward gap. Output 0-100 score. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/build-adaptation-scoring/README.md`
  - **Dependencies:** DQN training complete; oracle model available
  - **Estimated effort:** M (9–11 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Backend engineer
  - **Milestone:** Phase 2 – Algorithm Implementation

- **Task:** Validate adaptation scoring accuracy
  - **Description:** [Quality Mandate Required] Test on 1000 holdout games. Verify that high-elo players score 70+, average players score 50±10, new players score <40. Check oracle accuracy >80%. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/build-adaptation-scoring/README.md`
  - **Dependencies:** Scoring implementation complete
  - **Estimated effort:** M (11–14 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** QA analyst
  - **Milestone:** Phase 2 – Quality Assurance

## Cross‑Directory Task Links

- Mythic comparison used in [Zone 6 - Build & Ability](../visual-design/zones/zone-6-build-breakdown/tasks.md)
- Build insights used in [Zone 6 detail display](../visual-design/zones/zone-6-build-breakdown/tasks.md)
