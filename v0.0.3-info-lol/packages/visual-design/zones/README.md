# Zones – Detailed Specifications

This package contains the complete specification for all 7 visual zones that comprise The Summoner's Chronicle graphic.

## Zone Overview

| Zone | Name | Height | Focus | Purpose |
|------|------|--------|-------|---------|
| 1 | [Header](zone-1-header/README.md) | 200px | Match Context & Champion Identity | Establish context (win/loss, role, champion) and player name |
| 2 | [Champion Portrait & Core Stats](zone-2-champion-portrait/README.md) | 400px | Visual + Performance Dial | Show champion splash art and 5-ring performance metrics |
| 3 | [Timeline Narrative](zone-3-timeline-narrative/README.md) | 500px | Chronological Story Arc | Display momentum curve, key events, turning points, sentiment |
| 4 | [Advanced Performance Matrix](zone-4-performance-matrix/README.md) | 450px | Analytical Deep-Dive | Present 4 quadrants of efficiency, objective, and clutch metrics |
| 5 | [Positioning & Vision Intelligence](zone-5-positioning-vision/README.md) | 350px | Spatial Heatmap + Vision | Show champion position density and warding strategy analysis |
| 6 | [Build & Ability Breakdown](zone-6-build-breakdown/README.md) | 300px | Item & Ability Efficiency | Display item spike windows and ability efficiency ratings |
| 7 | [Comparative & Predictive Insights](zone-7-comparative-insights/README.md) | 200px | Learning & Comparison | Percentile rankings, shadow match, improvement suggestions |

## Design Principles for All Zones

1. **Context Preservation** – Every metric is contextualized (role-specific, matchup-adjusted, game-state-aware)
2. **Data Honesty** – No misleading visualizations; calculations are transparent via tooltips
3. **Accessibility** – Every visual has a text equivalent; colorblind-safe palettes; ARIA labels
4. **Interactivity** – Hover for tooltips, click for details or replay navigation (when applicable)

## Cascading Concerns

- **Zones 1-2:** Summary & Identity (what happened, who was involved)
- **Zone 3:** Narrative Arc (how the game unfolded)
- **Zones 4-6:** Analysis & Metrics (why the champion performed this way)
- **Zone 7:** Learning & Improvement (what to do next)

This cascade mirrors a natural learning progression: context → story → analysis → action.

## Boundaries

**Assumes:**
- Statistics & Algorithms provides accurate, meaningful calculations for all displayed metrics
- Infrastructure ensures data is available and privacy-preserved

**Constraints:**
- Each zone's content must fit within its allocated height (200-500px)
- All metrics must be contextualized (role-based, game-state-aware, not global comparisons)
- Visual hierarchy within zones should be consistent with the overall narrative flow
