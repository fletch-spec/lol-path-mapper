# Tasks for Ability Efficiency Rating

- **Task:** Build ability efficiency calculation system
  - **Description:** [Quality Mandate Required] Implement AER formula for all abilities: (damage + cc utility + misc value) / (mana cost × casts + cooldown × 0.5). Normalize to 0-100 scale per champion. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/visual-design/zones/zone-6-build-breakdown/ability-efficiency-rating/README.md`
  - **Dependencies:** Ability damage, CC duration, mana cost, cooldown data available; champion baseline data computed
  - **Estimated effort:** L (16–21 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Backend engineer
  - **Milestone:** Phase 2 – Zone 6 Implementation

- **Task:** Implement AER display UI
  - **Description:** [Quality Mandate Required] Display four bars (Q, W, E, R) each showing AER value, percentile ranking, and hit/land rate (for skill shots). Support hover for detailed breakdown. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/visual-design/zones/zone-6-build-breakdown/ability-efficiency-rating/README.md`
  - **Dependencies:** AER calculations complete; percentile rankings available
  - **Estimated effort:** M (9–11 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Zone 6 Implementation

- **Task:** Generate ability-specific insights
  - **Description:** [Quality Mandate Required] Create actionable callouts for high/low AER abilities. Example: "Charm AER 82 (excellent) suggests increasing land rate further" or "Orb AER 54 (poor) – reduce miss rate". This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/visual-design/zones/zone-6-build-breakdown/ability-efficiency-rating/README.md`
  - **Dependencies:** [Natural Language Generation](../../statistics-and-algorithms/natural-language-generation/tasks.md) complete; AER calculations available
  - **Estimated effort:** M (7–9 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Zone 6 Implementation

## Cross‑Directory Task Links

- Depends on [Zone 6 overview](../tasks.md)
- AER calculations depend on backend ability tracking system
- Insights depend on [Natural Language Generation](../../statistics-and-algorithms/natural-language-generation/tasks.md)
