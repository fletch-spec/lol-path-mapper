# Tasks for Polish Features

- **Task:** Implement hover tooltips with calculations
  - **Description:** [Quality Mandate Required] Create tooltip system showing formula and pro tips when hovering over metrics. Support 150ms fade-in. Dismiss on mouse-out or 5s timeout. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/infrastructure/polish-features/README.md`
  - **Dependencies:** All metrics defined; tooltip framework available
  - **Estimated effort:** M (11–14 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Polish

- **Task:** Build click-through zone highlighting system
  - **Description:** [Quality Mandate Required] Implement click on stats to highlight related zones or insights. Example: click "Map Pressure 41" highlights positioning heatmap and roaming callouts. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/infrastructure/polish-features/README.md`
  - **Dependencies:** All zones implemented; data relationships mapped
  - **Estimated effort:** M (9–11 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Polish

- **Task:** Create shareable highlight strip generator
  - **Description:** [Quality Mandate Required] Generate 1200×630px summary card showing champion, top 3 stats, and emotional title. Support "Copy to Clipboard", "Download PNG", and "Share to Discord". This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/infrastructure/polish-features/README.md`
  - **Dependencies:** All visual designs finalized; image generation library available
  - **Estimated effort:** M (11–14 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Polish

- **Task:** Implement full graphic PDF export
  - **Description:** [Quality Mandate Required] Generate high-resolution PDF of complete graphic (all 7 zones). Support printing as poster. Include metadata (summoner, date, match ID). This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/infrastructure/polish-features/README.md`
  - **Dependencies:** PDF generation library; all zone rendering complete
  - **Estimated effort:** M (9–11 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Polish

- **Task:** Build dynamic title system (emotional signatures)
  - **Description:** [Quality Mandate Required] Generate contextual titles (e.g., "Unkillable Demon King", "Ghost of the Rift") based on performance profile. Support 10+ archetypes. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/infrastructure/polish-features/README.md`
  - **Dependencies:** Performance metrics available; title templates created
  - **Estimated effort:** M (7–9 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer + Content strategist
  - **Milestone:** Phase 2 – Polish

- **Task:** Implement replay integration (client feature)
  - **Description:** [Quality Mandate Required] Enable click on timeline events to jump replay to that moment. Show heatmap overlay on replay playback (optional client enhancement). This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/infrastructure/polish-features/README.md`
  - **Dependencies:** Replay API available; client integration framework ready
  - **Estimated effort:** L (18–23 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Client engineer
  - **Milestone:** Phase 2 – Polish

- **Task:** Create error handling and graceful degradation
  - **Description:** [Quality Mandate Required] If zone/algorithm unavailable, show informative message. Support "Try Again" button. Allow user to continue viewing other zones. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/infrastructure/polish-features/README.md`
  - **Dependencies:** Error scenarios documented; fallback UI designed
  - **Estimated effort:** M (9–11 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Quality Assurance

- **Task:** Implement success confirmations and feedback
  - **Description:** [Quality Mandate Required] Show brief "✓ Copied!" notifications for actions (copy, download, share). Clear after 2-3s. Provide helpful error messages on failures. This task is not complete until all seven pillars of the Quality Mandate are verified.
  - **Source:** `packages/infrastructure/polish-features/README.md`
  - **Dependencies:** All interactive elements in place
  - **Estimated effort:** S (5–7 hours)
  - **Quality Checklist:** See DEVELOPER_AGENT_QUALITY_MANDATE.md sections 1-7 for required verification
  - **Assigned role:** Frontend engineer
  - **Milestone:** Phase 2 – Polish

## Cross‑Directory Task Links

- Tooltips improve usability of all [Visual Design zones](../visual-design/zones/tasks.md)
- Sharing features depend on [Privacy guardrails](privacy-guardrails/tasks.md) opt-in
- Replay integration depends on [Computer Vision](../statistics-and-algorithms/computer-vision-heatmaps/tasks.md)
