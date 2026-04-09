# Zone 2 – Champion Portrait & Core Stats: The Five-Ring Performance Dial

## Purpose

Combine visual identity (champion splash art) with a comprehensive performance summary via a pentagon radar chart showing 5 normalized performance metrics.

## Visual Layout

**Left Side:** High-resolution splash art (slightly desaturated, framed in a runic circle)

**Right Side:** Pentagon radar chart with performance data and central score

## The Five-Ring Performance Dial

A pentagon chart (5 axes, one per metric) normalized against the champion's role-specific expected ranges (not global averages).

### Metric 1: Kill Participation

**Definition:** `(Kills + Assists) / Team Total Kills`

**Role-Specific Benchmark:**
- Typical: 50-60% average for most roles
- Exceptional: >70%
- Poor: <40%

**Interpretation:** What percentage of your team's kills did you participate in? High = team enabler or frontline presence. Low = isolated playstyle.

**Tooltip Explanation:** *"Kill Participation measures your involvement in your team's successful fights. The higher the better — it indicates you're present for key moments."*

### Metric 2: Gold Efficiency

**Definition:** `Gold Earned / (Game Duration in Minutes × 450)`

**Reasoning:** 450 is the average expected gold/minute for a non-fed laner (baseline economy).

**Interpretation:**
- >1.2 = hyper-carrying, significantly ahead of expected
- 0.8-1.2 = on-pace, meeting expectations for your role
- <0.7 = severely behind, underfed relative to game time

**Tooltip Explanation:** *"Gold Efficiency compares your farming/killing to the expected rate. 1.0 = meeting role expectations; >1.0 = outperforming; <1.0 = underperforming."*

### Metric 3: Map Pressure Index

**Definition:** Composite of four weighted factors:
- Turret damage dealt (weighted 0.3)
- Enemy jungle vision (sweeper clears + control wards in enemy jungle, weighted 0.25)
- Roaming participation pre-14 minutes (weighted 0.25)
- Herald/Dragon presence within 10s before objective death (weighted 0.2)

**Normalization:** 0-100 scale

**Interpretation:** Did your champion exert pressure across the map or stay in one lane? Tanks and supports typically score higher. Farming-heavy champions may score lower.

**Tooltip Explanation:** *"Map Pressure Index measures your influence beyond your lane — vision, roams, objective participation. Higher = wider map impact."*

### Metric 4: Survivability Quotient

**Definition:** `(Deaths / Team Total Deaths)⁻¹ × (Damage Mitigated / Champion HP Pool Average)`

**Interpretation:** A composite of death-efficiency and damage mitigation. Tanks with many deaths but massive mitigation can score well (dying while tanking damage is their job).

**Tooltip Explanation:** *"Survivability balances deaths with mitigation. Tanks can score high even with deaths if they're soaking damage. Carries should minimize deaths."*

### Metric 5: Momentum Impact

**Definition:** Weighted sum of:
- First Blood participation: +15
- Triple+ kills: +10 each
- Objective steals (drake/baron/herald): +20
- Shutdown collection: +5 per 500g bounty

**Display:** "Momentum Points" with visual thunderbolt gauge (0-100)

**Interpretation:** Did your champion deliver game-changing moments? First blood, multi-kills, and shutdown collects swing momentum.

**Tooltip Explanation:** *"Momentum Impact measures game-swinging plays — first blood, multi-kills, steals, shutdowns. High = clutch performer."*

## Central Dial Display

**Center Value:** A single number — **Performance Score** (0-100)

**Calculation:** Weighted combination of all 5 metrics, adjusted for matchup difficulty (e.g., harder matchups reduce expected thresholds)

**Color Coding:**
- 0-20: Poor (Red)
- 21-40: Below Average (Orange)
- 41-60: Average (Yellow)
- 61-80: Good (Light Green)
- 81-100: Elite (Dark Green)

**Rating Labels:**
- 0-20: Struggling
- 21-40: Below Average
- 41-60: Average
- 61-80: Good
- 81-100: Elite

## Example

**Champion:** Ahri  
**Game Duration:** 34 minutes  
**Stats:** 12 Kills / 3 Deaths / 9 Assists  
**Kill Participation:** 67%  
**Gold Efficiency:** 1.15  
**Map Pressure Index:** 41 (lower due to staying in lane post-14)  
**Survivability:** 75 (2 deaths, good positioning)  
**Momentum Impact:** 72 (first blood, triple kill, shutdown)  

**Performance Score:** 84 ("Elite")

**Corner Insight Callout:** 

*"Your Kill Participation (67%) is in the top 12% of Ahri players this patch — but your Map Pressure Index (41) suggests you stayed in lane too long post-14."*

## Accessibility

- **Color:** Radar chart uses colorblind-safe gradients (not just red-green)
- **Text:** All metrics have large, readable labels and tooltip descriptions
- **Screen Readers:** Each metric value is readable via ARIA descriptions

## Boundaries

**Assumes:**
- Statistics & Algorithms provides accurate calculations for all 5 metrics
- Role-specific benchmarks are maintained and updated per patch
- Matchup difficulty adjustments are available from game data

**Constraints:**
- All 5 metrics must be normalized to 0-100 scale for consistent pentagon visualization
- Metrics should complement (not duplicate) each other
- Role-specific benchmarks must prevent cross-role comparisons (ADC 100 ≠ Support 100)
