# Tasks for Role Positional Normalization

- **Task:** Prepare training dataset for role clustering
  - **Description:** [Quality Mandate Required] Collect 10k diverse games from different roles/ranks. Extract 20 key statistics per game (economy, combat, survival, map, utility metrics). This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/role-positional-normalization/README.md`
  - **Dependencies:** Match data access; feature extraction framework
  - **Estimated effort:** M (11–14 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Data engineer
  - **Milestone:** Phase 1 – Data Preparation

- **Task:** Run PCA analysis on champion performance data
  - **Description:** [Quality Mandate Required] Perform principal component analysis on 20-feature dataset. Extract first 3 PCs explaining 85%+ variance. Interpret axes (economy, damage, utility). This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/role-positional-normalization/README.md`
  - **Dependencies:** 10k game dataset prepared; PCA library available
  - **Estimated effort:** M (9–11 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Data scientist
  - **Milestone:** Phase 2 – Algorithm Implementation

- **Task:** Implement K-Means clustering for role archetypes
  - **Description:** [Quality Mandate Required] Cluster the 10k games into 6 archetypes (Carry, Brawler, Tank, Support, Jungler, Control). Document archetype profiles and feature distributions. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/role-positional-normalization/README.md`
  - **Dependencies:** PCA complete; K-Means framework available
  - **Estimated effort:** M (11–14 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Data scientist
  - **Milestone:** Phase 2 – Algorithm Implementation

- **Task:** Create role-specific benchmark database
  - **Description:** [Quality Mandate Required] Compute mean and standard deviation for each metric within each archetype. Store benchmarks for weekly updates post-patch. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/role-positional-normalization/README.md`
  - **Dependencies:** Archetype assignments complete
  - **Estimated effort:** S (5–7 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Data engineer
  - **Milestone:** Phase 2 – Algorithm Implementation

- **Task:** Implement weekly benchmark retraining pipeline
  - **Description:** [Quality Mandate Required] Automate weekly PCA/K-Means recomputation with new games. Update percentile rankings and archetype boundaries to reflect current meta. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/role-positional-normalization/README.md`
  - **Dependencies:** Baseline clustering complete; automation framework available
  - **Estimated effort:** M (9–11 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** DevOps / Data engineer
  - **Milestone:** Phase 3 – Maintenance

- **Task:** Validate archetype assignments against known roles
  - **Description:** [Quality Mandate Required] Test clustering on 1000 games where official role is known. Achieve >92% accuracy in assigning players to correct archetype. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/statistics-and-algorithms/role-positional-normalization/README.md`
  - **Dependencies:** Clustering complete; test set with known roles available
  - **Estimated effort:** S (5–7 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** QA analyst
  - **Milestone:** Phase 2 – Quality Assurance

## Cross‑Directory Task Links

- Benchmarks used in all [Visual Design zones](../visual-design/zones/tasks.md) for metric normalization
- Weekly updates feed [Infrastructure performance targets](../infrastructure/tasks.md)
