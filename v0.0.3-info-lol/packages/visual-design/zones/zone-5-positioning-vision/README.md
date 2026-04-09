# Zone 5 – Positioning & Vision Intelligence: Spatial Heatmap & Ward Strategy

## Purpose

Showcase a speculative but feasible computer vision application that reveals champion positioning patterns and ward placement intelligence.

## Visual Centerpiece: Summoner's Rift Heatmap

**Visual:** 600×600px Summoner's Rift map (simplified, lane/brush outlines only) overlaid with a smooth gradient heatmap

**Data Source:** Post-process replay files with object detection (YOLO or custom CNN) to track champion bounding boxes at 2 fps

**Heatmap Color Scale:**
- Deep Blue (0-2% of time spent) → Cyan → Yellow → Red (10%+ of time)
- White hotspots: >15% of time spent in that location
  - Example: Mid lane post-15 min for a mid laner

## Three Sub-Layers (Toggleable UI Buttons)

### Layer 1: Laning Phase (0-14 minutes)

**Content:** Positioning density during early game

**Insights:**
- Hotspots show trading stance (e.g., Ahri favors river-side of mid lane over brush, suggesting gank vulnerability awareness)
- Color intensity reveals time spent defending vs. pushing
- Interaction: Hover over hotspots reveals stat cards

**Example Analysis:** *"You spent 18% of laning phase near enemy raptors (aggressive). Compare to Ahri average (8%) — you pushed harder than expected."*

### Layer 2: Mid Game (14-25 minutes)

**Content:** Rotation patterns and mid-game positioning

**Insights:**
- Pathings shown: Did you rotate through enemy jungle (risky) or safe river (passive)?
- Clustering indicates grouping for objectives
- Isolated positions reveal sidelane pressure or jungler coordination

**Example:** *"Your rotation pattern shows river pathing (safe) but inconsistent — sometimes you cut through jungle. 2 of 3 deaths occurred during jungle cuts."*

### Layer 3: Late Game (25+ minutes)

**Content:** Baron/Dragon pit positioning and sidelane pressure

**Insights:**
- Clustering around pit areas shows positioning for high-stakes fights
- Sidelane presence reveals split-push vs. grouping strategy

**Example:** *"Clustered around Dragon pit (70% of late game spent within 800 units) — strong objective focus. No sidelane pressure, but team appreciated grouped defense."*

## Theoretical CV-Derived Metrics

**Display:** Cards positioned around the heatmap showing advanced positional stats

| Metric | Description | Example Insight |
|--------|-------------|-----------------|
| [Brush Dwelling Time](computer-vision-heatmap/README.md) | % of game spent in fog of war (unseen by enemies) | "You spent 18% of game in brush — 6% above Ahri average. Ambush-heavy playstyle." |
| [Proximity to Walls](computer-vision-heatmap/README.md) | Avg distance to terrain (pixels) during teamfights | "Teamfight positioning: 72px from walls (safe), but no terrain used for charm angles." |
| [Mouse Click Dispersion](computer-vision-heatmap/README.md) | Movement click pattern variance (chaotic vs. deliberate) | "Your click pattern suggests indecision in river skirmishes (high dispersion pre-engage)." |
| [Vision Line Crossings](computer-vision-heatmap/README.md) | Times you moved from lit to unlit map areas | "You entered unwarded jungle 23 times — 11 of those preceded a death." |

For full technical details, see [Computer Vision Heatmap](computer-vision-heatmap/README.md).

## Ward Placement Intelligence

**Display:** Small dots on map for each ward placed

**Visual Encoding:**
- **Green dots:** Allied wards you placed (successful vision)
- **Red dots:** Swept/enemy-cleared wards (unsuccessful)
- **Lines:** Connecting wards that created "vision chains" (continuous sightlines)

### Shadow Score

**Definition:** `(Wards that revealed an enemy) / (Total Wards Placed)`

**Interpretation:**
- High (>60%): Excellent ward placement quality; most wards saw enemy action
- Medium (30-60%): Mix of good and defensive wards
- Low (<30%): Wards placed but rarely revealed enemies (poor positioning or timing)

**Example:** *"Your Shadow Score: 58% — out of 12 wards placed, 7 revealed enemy champions. Strong placement sense."*

## Insight Callout Examples

*"Your heatmap shows a 'death valley' at the river pixel near Raptor camp — you lingered there 9% of mid-game, but died there twice. Adjust your reset pathing."*

*"Contrast: Pro players spend only 2% of mid-game in this risky position. You found a playstyle advantage here (1 solo kill), but the 2-death swing is rough. Lesson: Reduce visits to 3-4% to maintain risk/reward."*

## Accessibility

- **Color:** Heatmap uses colorblind-safe gradient (blue → yellow → red has brightness separation)
- **Toggle buttons:** Layer selection is keyboard-navigable
- **Text:** All metric cards have ARIA labels and descriptions

## Boundaries

**Assumes:**
- [Computer Vision](computer-vision-heatmap/README.md) methods can extract champion positions from replay files with <15px error
- Brush/terrain data is accurate for map
- Tooltip data (enemy reveals, hotspot meanings) is provided

**Constraints:**
- Heatmap shows only your champion position, never enemy positions retroactively (unless de-identified)
- All metrics are local calculation (your device) or opt-in cloud processing
- Must respect privacy (no player-tracking across games without consent)

---

## Sub-Packages

See [Computer Vision Heatmap](computer-vision-heatmap/README.md) and [Ward Placement Intelligence](ward-placement-intelligence/README.md) for detailed metric specifications.
