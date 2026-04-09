# Quadrant C – Objective Control & Roaming: Map Impact

## Purpose

Measure how effectively the champion influenced objective ownership and map pressure outside their primary lane.

## Metrics

### 1. Vision Denial Ratio

**Definition:** `(Control Wards Placed + Sweeper Clears) / (Enemy Wards Placed in Your Jungle)`

**Interpretation:**
- >1: You out-visioned the enemy in objective areas (good)
- ~1: Vision parity
- <1: Enemy warded your jungle more than you swept (positioning weakness)

**Example:**
- Control wards placed: 8
- Sweeper clears: 12
- Enemy wards in your jungle: 15
- **Ratio:** (8 + 12) / 15 = 1.33 (winning vision battle)

**Insight:** *"You controlled vision in critical areas 1.33× better than the enemy — warding and sweeping was a strength."*

### 2. Objective Participation Heatmap

**Display:** Mini-map replica with circles scaled to your proximity to each objective

**What It Shows:**
- 10 seconds before each dragon/baron/turret died, where were you?
- Circle size: How close you were (larger = closer = more control)
- Circle color: Green if your team got it, red if enemy secured it

**Interpretation:**
- Clustered green circles: You're present for important objectives
- Scattered red circles: You missed objective windows (perhaps farming)
- Sidelanes with red circles: You didn't rotate fast enough; enemy secured objective unopposed

**Example Insight:** *"You were present for 5 of 8 dragons, but absent for the 4th (Elder attempt mid-game). Better rotations could have prevented that steal."*

### 3. Roaming Score

**Definition:** `(Roaming Kills + Assists) / (Game Minutes × 0.1)` with penalty for lost plates during roam

**Interpretation:**
- High: Roaming was productive; you secured kills while roaming
- Medium: Roaming happened but didn't always convert
- Low: Stayed in lane; minimal roaming impact

**Consideration:** If you lost CS/plates during roams that didn't convert to kills, the score is reduced.

**Example:**
- Roaming kills + assists: 8
- Game duration: 34 minutes
- Baseline: 34 × 0.1 = 3.4
- Score: 8 / 3.4 = 2.35 roaming score
- Adjustment: -0.3 for 2 turret plates lost during failed roams
- **Final Roaming Score:** 2.05

**Insight:** *"Your roaming generated 2+ kills/assists per roaming window — an aggressive, productive playstyle."*

## Visual Representation

**Display:** 
- Large heatmap of objectives (dragon/baron pits, turret lanes)
- Bars or numeric displays for vision denial and roaming scores
- Annotations highlighting key moments

## Accessibility

- **Color:** Objective heatmap uses colorblind-safe gradients (green ≠ red distinction via brightness too)
- **Text:** All scores labeled clearly

## Boundaries

**Assumes:**
- Map coordinates for objectives are accurate
- Ward placement and sweeper data are available from API
- Roaming events (leaves lane to other lane) are detected from positional data

**Constraints:**
- Vision ratio must only count objective-critical areas (jungle), not entire map
- Roaming score must exclude "walking through a lane" vs. "actively roaming to secure objective"
