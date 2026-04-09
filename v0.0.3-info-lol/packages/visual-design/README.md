# Visual Design – Layout & Hierarchy

## Canvas Dimensions

**Canvas Size:** 1920×2400 pixels (vertical scroll-friendly, printable as poster)

This vertical format supports both web scrolling and poster-style printing, making the graphic flexible across distribution channels.

## Layout Zones (Top to Bottom)

The graphic is divided into 7 distinct zones, each with specific content and visual responsibilities:

| Zone | Height | Primary Content |
|------|--------|-----------------|
| 1. Header | 200px | Match context, result, role, champion identity |
| 2. Champion Portrait & Core Stats | 400px | Splash art + 5-ring performance dial |
| 3. Timeline Narrative | 500px | Chronological event strip with momentum arc |
| 4. Advanced Performance Matrix | 450px | Heatmaps, gold/xp differentials, efficiency ratios |
| 5. Positioning & Vision Intelligence | 350px | Theoretical CV-generated heatmap + vision denial zones |
| 6. Build & Ability Breakdown | 300px | Item spike windows, ability efficiency rating |
| 7. Comparative & Predictive Insights | 200px | Percentile rankings, "shadow match" comparison |

**Total:** 2400px (all zones sum to visual canvas)

## Design Philosophy

- **Hierarchical:** Information density increases from top (summary) to middle (analysis) to bottom (learning)
- **Narrative:** Each zone builds on the previous, telling a coherent story of the champion's journey
- **Accessibility:** Colorblind-friendly palettes, text-to-speech support, meaningful labels throughout
- **Interactive:** Hover tooltips reveal calculations; click-through to replay moments (when available)

## Detailed Zone Specifications

See [Zones Package](zones/README.md) for complete specifications of each zone's content and interactivity.

## Boundaries

**Assumes from downstream packages:**
- Statistics & Algorithms will provide accurate computations that feed into visual elements
- Infrastructure will handle data loading and caching efficiently to support interactivity

**Boundaries others must respect:**
- Visual Design defines the physical layout and zones — no content should violate zone boundaries
- Zones are ordered intentionally (summary → detail → learning) — reordering changes narrative flow
- Canvas dimensions (1920×2400) are fixed to support printable posters
