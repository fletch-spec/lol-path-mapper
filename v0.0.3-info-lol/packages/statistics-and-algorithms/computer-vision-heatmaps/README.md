# Computer Vision for Positioning Heatmaps

## Purpose

Extract champion positioning data from replay files using object detection, enabling spatial analysis and heatmap visualization.

## Method

**Post-process replay files** with object detection models (YOLO or custom CNN) to track champion bounding boxes at 2 frames per second.

### Technical Details

**Model Architecture:**
- YOLO v5/v8 or custom fine-tuned CNN
- Input: 30 fps replay video frames (downsampled to 2 fps for processing)
- Output: Bounding box coordinates (x, y, width, height) for each champion
- Confidence threshold: >0.85 to minimize false positives

**Training Data:**
- League champion sprites extracted from client
- 10k+ manually annotated frames showing champions in various game states
- Augmentation: Rotation, scaling, lighting variations to handle replay compression

**Preprocessing:**
- Normalize frame coordinates to map space (1920×1920 Summoner's Rift)
- Filter out-of-bounds coordinates (champions shouldn't exist outside map)
- Interpolate missing frames (<0.1% frames typically fail detection)

### Validation

**Expected Error:** <15 units (pixels) on Summoner's Rift  
**Validation Method:** Compare CV-derived positions to Riot's official API when available

**Error Sources:**
- Replay compression artifacts (low quality)
- Champion model clipping in terrain
- Fog of war boundaries (CV can't distinguish lit/dark in replays, uses minimap data)

## Outputs

### 1. Position Density Heatmap

**Calculation:** Gaussian kernel density estimation over tracked positions

- **Bandwidth:** 300 units (smoothing parameter)
- **Result:** Smooth probability density function showing where champion spent time
- **Visualization:** Color gradient (blue → cyan → yellow → red)

**Usage Zones:**
- [Zone 5: Positioning & Vision](../../visual-design/zones/zone-5-positioning-vision/README.md) — 600×600px heatmap display

### 2. Teamfight Alignment Vectors

**Calculation:** For each teamfight (5v5 or 4v4+):

1. Identify all positions during fight window (3-15 second cluster of combat)
2. Calculate enemy team centroid (average of all enemy positions)
3. Calculate direction vector: (player champion position) → (enemy centroid)
4. Compute angle relative to expected "attacking" direction (toward center)

**Output:** Direction vector (angle, 0-360°)

**Interpretation:**
- 0-90°: Facing toward enemy (aggressive)
- 90-180°: Perpendicular/kiting (balanced)
- 180-270°: Facing away (retreating/losing)

**Insight:** Pattern of angles reveals playstyle (aggressive, defensive, kiting-focused)

### 3. Panic Score

**Calculation:** Variance in movement speed during 3-second window after first enemy visibility

1. Detect moment when first unseen enemy appears (emerges from fog)
2. Extract movement speeds for 3 seconds post-reveal
3. Calculate standard deviation (variance in speed = panic indicator)

**Normalization:** Baseline = 0.60 (average player panic)

**Interpretation:**
- >0.60: High variance, indecision
- 0.40-0.60: Calm, deliberate movement
- <0.40: Extremely calm (possible passive play)

## Privacy & Security

**Privacy Guardrails:**
- Heatmaps are single-player only (your champion, never enemies)
- Replay processing happens client-side (optional, user must explicitly enable)
- No replay data is transmitted to servers

**Performance:**
- Processing time: ~60 seconds per 34-min game on modern CPU
- Can be run in background without impacting client

## Edge Cases

**Untraceable Frames:**
- Fog of war areas: CV still tracks position, but marked as "invisible to enemy"
- Turret/brush clipping: Position may jump; interpolation handles this
- Extreme zoom (locked camera): Coordinates normalized regardless

**Champion-Specific Challenges:**
- Invisible champions (Teemo stealth, Akali shroud): CV still detects, but visibility flag set
- Summoned units (Daisy, R.A.H. Turrets): Filtered out (only track champion)
- Wall-clipping champions (Sylas swinging): Coordinates snapped to valid map space

## Validation & Testing

**Unit Tests:**
- Position interpolation: Verify smoothness
- Density heatmap: Compare to manual ground truth regions
- Teamfight detection: Verify 5v5 clusters are identified

**Integration Tests:**
- Full replay processing: Measure speed (<2 min per game)
- Accuracy validation: Compare 10 replays against known ground truth

**Limitations:**
- Replay compression can introduce <15px error
- Fog of war boundaries estimated (not perfect)
- Extreme game speeds or lag can create artifacts

## Boundaries

**Assumes:**
- Replay files are available and accessible
- Map coordinate system is consistent (1920×1920)
- Summoner's Rift layout is static (no map changes mid-season)

**Provides:**
- Accurate position tracking for heatmap visualization
- Spatial metrics (brush time, wall proximity, panic score)
- Teamfight alignment analysis
