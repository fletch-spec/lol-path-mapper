# Computer Vision Heatmap: Position Tracking & Metrics

## Purpose

Extract champion positioning data from replay files using computer vision and generate advanced spatial metrics that reveal playstyle patterns.

## Technical Foundation

**Method:** Post-process replay files with object detection models (YOLO or custom CNN) to track champion bounding boxes at 2 frames per second.

**Validation:** Compare CV-derived positions to Riot's official API (when available) — expected error <15 units.

## Outputs

### 1. Position Density (Gaussian KDE)

**Calculation:** Gaussian kernel density estimation over tracked positions, bandwidth = 300 units

**Result:** Smooth heatmap showing where champion spent most time

**Interpretation Zones:**
- Laning phase hotspots reveal neutral vs. aggressive stance
- Mid-game clusters indicate pathing preferences (river vs. jungle)
- Late-game concentration shows fight participation (grouped vs. split-push)

### 2. Teamfight Alignment Vectors

**Calculation:** For each teamfight, calculate direction your champion faced relative to enemy team centroid

**Interpretation:**
- Aligned toward enemy backline: Aggressive positioning, targeting priority targets
- Perpendicular to frontline: Kiting/disengage, maintaining safe distance
- Facing away: Disengaging, backpedaling (indicates losing fight)

**Insight Example:** *"In the 3 teamfights you won, your average angle was 45° toward enemy damage dealers. In the 2 you lost, you faced 120° away. Reposition to face threats even when retreating."*

### 3. Panic Score

**Calculation:** Variance in movement speed during 3 seconds after first enemy appearance in fog of war (sudden enemy encounter)

**Interpretation:**
- High variance: Erratic movement; indecision or panic
- Low variance: Smooth, deliberate movement; calm decision-making

**Insight Example:** *"When ambushed, your panic score is 0.45 (average = 0.60). You respond calmly — a strength."*

## Advanced Metrics

### Brush Dwelling Time

**Definition:** Percentage of game spent in fog of war (unseen by enemies)

**Role Context:**
- Mid laners: ~5-10% (roaming out of fog)
- Junglers: ~40-60% (clearing camps unseen)
- Supports: ~15-25% (warding, roaming)
- ADCs: ~3-8% (lane presence)

**Example:** *"You spent 18% of game in brush — 6% above Ahri average (12%). Suggests ambush-heavy, aggressive roaming playstyle."*

### Proximity to Walls

**Definition:** Average distance to terrain (pixels) during teamfights

**Calculation:** For each teamfight frame, calculate distance to nearest wall/terrain

**Interpretation:**
- Close to walls (40-80px): Using terrain for protection, good positioning
- Medium (80-120px): Balanced spacing
- Far from walls (>120px): Exposed, vulnerable in fights

**Example:** *"Teamfight positioning: 72px from walls (safe), but analysis shows you never positioned around walls to land charm angles. Opportunity: Use walls for zoning."*

### Mouse Click Dispersion

**Definition:** (If CV could track cursor) Variance in click positions during skirmishes

**Calculation:** Standard deviation of click coordinate differences (chaotic vs. deliberate)

**Interpretation:**
- Low dispersion: Deliberate, planned movements (rotate then fight)
- High dispersion: Chaotic, reactive movements (panic kiting)

**Example:** *"Your click pattern suggests high indecision in river skirmishes (dispersion = 0.72 vs. average 0.50). Take time to commit to one direction."*

### Vision Line Crossings

**Definition:** Number of times you moved from lit map areas to dark (unlit) areas

**Calculation:** Frame-by-frame check: is champion in visible area? Track transitions to dark

**Interpretation:**
- Each unlit visit is a risk; if enemy ward was there, you're caught
- Correlate with deaths: How many deaths preceded unlit area entries?

**Example:** *"You entered unwarded jungle 23 times. Of those, 11 preceded deaths (48% death rate). Safe entry count: 12 (52% safe). Practice river roaming instead."*

## Display in Zone 5

**Heatmap:** 600×600px showing density gradient  
**Toggles:** 3 layer buttons (laning/mid/late)  
**Metrics Cards:** 4 stat cards around map showing advanced metrics  
**Annotations:** Hotspots labeled with %time and interpretation

## Privacy & Limitations

**Privacy:** Heatmaps show only your champion, never enemy positions (unless de-identified historical pro data)

**Limitations:**
- CV detection error is <15px but can accumulate over long games
- Fog of war determination relies on accurate map data (brush/vision radius)
- Terrain proximity assumes accurate wall coordinates

## Boundaries

**Assumes:**
- Replay files are available locally for post-processing
- YOLO/CNN model is trained on League champion sprites
- Map terrain and brush data are accurate

**Constraints:**
- Processing must happen client-side or with explicit opt-in (privacy)
- CV must be fast enough to process entire replay within reasonable time
- Error bars (<15px) must be acknowledged in metric displays
