# Ward Placement Intelligence: Vision Strategy Analysis

## Purpose

Analyze the player's warding strategy, map vision control, and the quality/impact of ward placements.

## Visual Representation on Zone 5 Heatmap

**Ward Markers:**
- **Green dots:** Allied wards you placed (detected via API, visualized on heatmap)
- **Red dots:** Wards that were swept or cleared by enemy
- **Lines:** Connections showing "vision chains" (overlapping vision ranges creating continuous sightlines)

## Key Metrics

### 1. Vision Denial Ratio (Cross-Reference with Quadrant C)

**Definition:** `(Control Wards Placed + Sweeper Clears) / (Enemy Wards Placed in Your Jungle)`

**Interpretation:**
- >1: You controlled vision better than enemy
- <1: Enemy dominated vision

**Insight Example:** *"Vision denial ratio 1.33: You swept/cleared 1.33× more wards than enemies placed. Excellent defensive warding."*

### 2. Shadow Score

**Definition:** `(Wards that revealed an enemy) / (Total Wards Placed)`

**Calculation:** 
- Track each ward placed
- Check: Did this ward ever have an enemy champion in its range during its duration?
- Ratio: successful wards / total wards

**Interpretation:**
- High (>60%): Excellent placement quality; most wards caught enemies
- Medium (30-60%): Mix of strategic (deep) and defensive (safe) wards
- Low (<30%): Wards placed in low-traffic areas or poor timing

**Example:**
- 12 total wards placed
- 7 wards revealed at least one enemy during their lifetime
- **Shadow Score:** 7/12 = 58%

**Insight:** *"Shadow Score: 58% — solid placement. You're balancing aggressive deep wards (low immediate value) with defensive wards (high immediate value)."*

### 3. Vision Chain Detection

**Definition:** Connected wards that together create continuous sightline coverage of critical areas

**Display:**
- Map shows lines connecting wards with overlapping vision ranges
- Highlights long, unbroken vision chains

**Interpretation:**
- Strong vision chains indicate strategic planning (not reactive warding)
- Example chain: Ward in river → Ward in enemy jungle → Ward near baron pit = continuous sightline

**Insight Example:** *"You created 2 major vision chains during mid-game. Pro players average 1.5 chains — you're thinking strategically about vision continuity."*

### 4. Ward Placement by Game Phase

**Breakdown:** Distribution of wards across game phases

| Phase | Recommended | Your Count | Quality |
|-------|-------------|-----------|---------|
| Laning (0-14) | 3-5 | 4 | Average |
| Mid (14-25) | 6-10 | 8 | Good |
| Late (25+) | 8-12 | 7 | Below Average |

**Insight:** *"You under-warded late game (7 vs. recommended 8-12). Increased late-game ward count to secure Baron/Dragon control could've swung teamfights."*

### 5. Control Ward Efficiency

**Definition:** `(Enemies revealed by control wards) / (Control Wards Placed)`

**Interpretation:**
- High: Control wards were placed in high-traffic enemy paths
- Low: Control wards were placed defensively but never interrupted enemies

**Example:** *"Control Ward Efficiency: 0.75 — 3 out of 4 control wards revealed an enemy. Excellent proactive warding."*

## Heatmap Visualization

**Green dots overlay:** Each green dot is a ward you placed, sized and colored by:
- **Brightness:** How long the ward was alive (dim = cleared quickly, bright = lasted entire phase)
- **Position:** Exact location on map

**Red dots overlay:** Cleared/swept wards (visual feedback that enemy contested vision)

**Lines overlay:** Vision chains connecting overlapping ward ranges

## Accessibility

- **Color:** Green (wards placed) vs. Red (cleared) with text labels
- **Interactivity:** Click any ward dot to see: placement time, reveal count, duration
- **Text:** All metrics have readable descriptions

## Boundaries

**Assumes:**
- Ward placement and destruction data are accurate from API
- Enemy ward data is available (Riot API provides this)
- Vision range calculations are accurate (typically 1100 units for standard wards)

**Constraints:**
- Shadow Score only applies if wards were alive when enemy was in range (not historical checking)
- Vision chains require at least 2 wards to overlap
- Control wards have different vision range (typically 900 units) — must be tracked separately
