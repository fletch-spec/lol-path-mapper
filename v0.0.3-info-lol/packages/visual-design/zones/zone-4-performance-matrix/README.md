# Zone 4 – Advanced Performance Matrix: Analytical Deep-Dive

## Purpose

Provide a detailed, data-rich view of 4 interconnected aspects of performance: resource efficiency, combat effectiveness, objective control, and clutch moments.

## Layout

**2×2 Grid** of quadrants, each 200×200 pixels (450px total height including borders/labels)

| Quadrant | Focus | Metrics |
|----------|-------|---------|
| [A](quadrant-a-gold-xp/README.md) | Gold & XP Efficiency | GPM, effective gold, XP gap |
| [B](quadrant-b-combat-efficiency/README.md) | Combat Efficiency | Damage per gold, kill conversion, tankiness, CC score |
| [C](quadrant-c-objective-control/README.md) | Objective Control | Vision denial ratio, heatmap, roaming score |
| [D](quadrant-d-clutch-factor/README.md) | Clutch Factor | Low-health efficiency, comeback contribution, shutdowns, late-game activity |

## Design Principles

**Data Density:** Each quadrant packs 3-4 related metrics into one visualization  
**Comparability:** All metrics include role-average or global benchmarks for context  
**Actionability:** Insights highlight what the player did well or poorly  
**Visual Clarity:** Use tables, bar charts, sparklines — avoid overwhelming detail

## Example Insight (Cross-Quadrant)

*"Your Damage per Gold (Quad B: 6.2) is excellent, but your Kill Conversion (0.33) is bottom 15% — you're poking but not finishing. Consider holding abilities for execution thresholds."*

This insight synthesizes data across quadrants to provide actionable feedback.

## Boundaries

**Assumes:**
- Statistics & Algorithms provides accurate calculations for all 12+ metrics
- Role-specific benchmarks are available and current
- Comparisons (vs. role average, vs. global) are correct

**Constraints:**
- Each quadrant must fit its allocated 200×200px space
- Visual must be scannable in 10 seconds
- All metrics must include their calculation formula (via tooltip)

---

## Navigation

For detailed specifications of each quadrant, see:

- **[Quadrant A: Gold & XP Efficiency](quadrant-a-gold-xp/README.md)**
- **[Quadrant B: Combat Efficiency Ratios](quadrant-b-combat-efficiency/README.md)**
- **[Quadrant C: Objective Control & Roaming](quadrant-c-objective-control/README.md)**
- **[Quadrant D: The Clutch Factor](quadrant-d-clutch-factor/README.md)**
