# Statistics & Algorithms: Computational Methods

## Purpose

Describe the theoretical and practical statistical frameworks that power the insights and analytics displayed across all visual zones.

## Overview

This package contains 5 major algorithmic approaches, each addressing a distinct aspect of match analysis:

1. **[Computer Vision for Heatmaps](computer-vision-heatmaps/README.md)** — Extract champion positioning from replay files
2. **[Win Probability Model](win-probability-model/README.md)** — Attribute match outcome impact to individual actions
3. **[Role Positional Normalization](role-positional-normalization/README.md)** — Contextualize metrics by champion role and expectations
4. **[Natural Language Generation](natural-language-generation/README.md)** — Auto-generate event descriptions and improvement prompts
5. **[Build Adaptation Scoring](build-adaptation-scoring/README.md)** — Evaluate itemization decisions

## Which Zone Uses Which Algorithm?

| Zone | Algorithm(s) |
|------|------------|
| 1: Header | Win Probability (strategic callout) |
| 2: Champion Portrait | Role Normalization (5-ring dial benchmarks) |
| 3: Timeline Narrative | Win Probability (sentiment arc), NLG (event annotations) |
| 4: Performance Matrix | All (normalization for all metrics, roles benchmarks) |
| 5: Positioning & Vision | Computer Vision (heatmap, metrics) |
| 6: Build & Ability | Build Adaptation (item comparison), Role Norm (AER baselines) |
| 7: Comparative Insights | Win Probability (Shadow Match), NLG (improvement prompts, parting shot) |

## Integration Points

**Data Flow:**

```
Match Timeline (API)
    ↓
Match Data Extract (gold, kills, deaths, positions, items, abilities)
    ↓
├─→ Computer Vision (replay → positions)
├─→ Win Probability Model (monte carlo, gradient boosting)
├─→ Role Normalization (contextualize all metrics)
├─→ NLG (generate descriptions)
└─→ Build Adaptation (evaluate items)
    ↓
Visual Zones (display aggregated insights)
```

## Assumptions & Limitations

### General Assumptions
- **Match data accuracy:** Riot API provides truth
- **Replay file availability:** Replays are accessible for CV processing
- **Historical database:** Sufficient player/pro game data exists for benchmarking

### Computation Resources
- **Real-time:** Not required; processing can happen post-game (5-30 minutes)
- **Client-side vs. Cloud:** CV processing (heatmaps) should be client-side for privacy; other algorithms can be cloud-based

### Model Training
- **Frequency:** Weekly updates (post-patch) to account for balance changes
- **Data source:** 10M+ solo queue games + professional play games

## Validation & Testing

All algorithms should be tested against:

1. **Determinism:** Same input → same output (for debugging)
2. **Accuracy:** Validation against known player stats (percentile rankings should match)
3. **Latency:** Processing time <30 seconds for full match analysis
4. **Privacy:** No player data retained; only aggregated metrics stored

## Boundaries

**Assumes from Visual Design:**
- All zones understand the statistical methods behind their metrics
- Metrics are displayed with clear definitions (tooltips explaining formulas)

**Provides to Visual Design:**
- Accurate, validated computations
- Role-specific contexts and benchmarks
- Meaningful, actionable insights

---

## Navigation

- **[Computer Vision Heatmaps](computer-vision-heatmaps/README.md)** — YOLO/CNN champion tracking
- **[Win Probability Model](win-probability-model/README.md)** — Monte Carlo + gradient boosting
- **[Role Positional Normalization](role-positional-normalization/README.md)** — PCA-based role clustering
- **[Natural Language Generation](natural-language-generation/README.md)** — VAE + templates
- **[Build Adaptation Scoring](build-adaptation-scoring/README.md)** — RL-based item evaluation
