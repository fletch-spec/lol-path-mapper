# Infrastructure: Data, Privacy, Accessibility & Polish

## Purpose

Describe the operational infrastructure, data sources, privacy guarantees, accessibility support, localization, and final polish interactions that enable and secure the graphic experience.

## Overview

This package addresses non-visual but critical concerns:

1. **[Data Sources](data-sources/README.md)** – Where data comes from, API reliability
2. **[Privacy Guardrails](privacy-guardrails/README.md)** – User data protection, opt-ins, retention
3. **[Accessibility](accessibility/README.md)** – Colorblind modes, screen readers, keyboard navigation
4. **[Localization](localization/README.md)** – Multi-language support, regional formatting
5. **[Polish Features](polish-features/README.md)** – Micro-interactions, sharing, replay sync

## Service Architecture

### Data Pipeline

```
Match Ends (Summoner's Rift)
    ↓
Riot API: Fetch match timeline, participant frames, events
    ↓
├─→ Local Client: Fetch replay file (if enabled)
├─→ Cloud: Process match data (compute metrics)
└─→ ML Services: Compute advanced metrics (CV heatmaps, NLG, etc.)
    ↓
Aggregation Layer: Combine all computations
    ↓
Caching Layer: Store results locally (optional cloud backup)
    ↓
Render Engine: Generate graphic (web/client)
    ↓
User Sees: Complete graphic
```

## Performance Targets

| Component | Target | Acceptable |
|-----------|--------|----------|
| Data fetch (API) | <5 seconds | <10 seconds |
| Metric computation | <30 seconds | <60 seconds |
| CV heatmap (local) | <60 seconds | <120 seconds |
| Full graphic render | <2 seconds | <5 seconds |
| Total user wait | <60 seconds | <120 seconds |

## Privacy-First Design

**Core Principle:** User data should never be transmitted, stored, or analyzed without explicit opt-in.

- **Replay files:** Client-side processing only (unless user opts into cloud analysis)
- **Match data:** Aggregated (no individual player info retained post-analysis)
- **Heatmaps:** Single-user only (never cross-player analysis)
- **Comparisons:** Only against anonymized aggregate data or consented pro-play

## Accessibility Standards

**Compliance:**
- WCAG 2.1 Level AA (minimum)
- Colorblind-friendly all color-coded visuals
- Screen reader support on all text and metrics
- Keyboard-navigable UI

## Localization

**Languages Supported:** 14 (English, Spanish, French, German, Italian, Portuguese, Russian, Japanese, Korean, Simplified Chinese, Traditional Chinese, Vietnamese, Turkish, Thai)

**Formatting:**
- Numbers: Region-appropriate (1.234,56 for EU; 1,234.56 for US)
- Timestamps: Local timezone with offset display
- Match narratives: Culturally sensitive phrasing (e.g., "dragon" terminology varies by region)

## Micro-Interactions & Polish

**Interactive Elements:**
- Hover tooltips with calculation explanations
- Click-through to replay moments (in-client only)
- Shareable summary cards (1200×630px for social media)
- Dynamic titles that change based on performance archetype

## Data Retention & GDPR Compliance

**Retention Policy:**
- Match graphics: Stored for 30 days (user can request deletion anytime)
- Aggregated analytics: Anonymized, retained indefinitely for model improvement
- Personal data: Deleted on account deletion or explicit request

**GDPR Compliance:**
- Right to access: Users can download their graphics
- Right to deletion: Users can delete specific matches
- Right to portability: Graphics exportable as PDF

## Boundaries

**Assumes from All Packages:**
- All metrics are computed accurately (Stats & Algorithms)
- All visuals are WCAG AA compliant (Visual Design)

**Provides to All Packages:**
- Reliable data access
- User privacy protection
- Universal accessibility
- Global language support
- Polished user experience

---

## Navigation

- **[Data Sources](data-sources/README.md)** — Riot API, replays, databases
- **[Privacy Guardrails](privacy-guardrails/README.md)** — Opt-ins, retention, compliance
- **[Accessibility](accessibility/README.md)** — Colorblind modes, screen readers
- **[Localization](localization/README.md)** — 14 language translations, regional formatting
- **[Polish Features](polish-features/README.md)** — Tooltips, sharing, replay sync
