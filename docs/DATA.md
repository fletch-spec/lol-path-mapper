# Data Structures & Formats

## Positions Cache (`cache/positions_*.json`)

Format: JSON with metadata wrapper

```json
{
  "meta": {
    "summoner": "Player Name",
    "champion": "Ahri"
  },
  "positions": [
    [game_time, x, y],
    [game_time, x, y],
    ...
  ]
}
```

### Fields

- **meta.summoner** (string): Summoner name (from `riotIdGameName` or `summonerName`)
- **meta.champion** (string): Champion name (e.g., "Ahri", "Nunu and Willump")
- **positions** (array): List of movement samples

### Position Tuple

Each entry is a 3-tuple: `[game_time, x, y]`

- **game_time** (float): In-game timestamp in seconds (0.0 to ~1500.0)
- **x** (float): Map coordinate, X-axis
- **y** (float): Map coordinate, Y-axis (called `z` in the API)

**Coordinate system**:
- Origin (0, 0) is near the top-left corner of the map
- Blue nexus ≈ (400, 400)
- Red nexus ≈ (14000, 14000)
- Typical range: [0, ~14500]

### Example

```json
{
  "meta": {
    "summoner": "Ahri Main",
    "champion": "Ahri"
  },
  "positions": [
    [0.0, 8040.5, 145.3],
    [0.1, 8041.2, 146.1],
    [0.2, 8042.8, 147.4],
    [2.5, 8100.0, 200.0],
    [5.0, 8150.0, 250.0]
  ]
}
```

## Player Object

From `/liveclientdata/playerlist`:

```json
{
  "championName": "Ahri",
  "riotIdGameName": "PlayerName",
  "riotIdTagLine": "NA1",
  "summonerName": "Summoner Name",
  "team": "ORDER",
  "skinName": "Spirit Blossom Ahri",
  "level": 18,
  "stats": {
    "kills": 5,
    "deaths": 2,
    "assists": 12
  }
}
```

### Fields (relevant for this project)

- **championName** (string): Champion pick (e.g., "Ahri")
- **riotIdGameName** (string): Riot ID name component (preferred for display)
- **riotIdTagLine** (string): Riot ID tag (e.g., "NA1", "EUW1")
- **summonerName** (string): Legacy summoner name (fallback if Riot ID not available)
- **team** (string): `"ORDER"` (blue team) or `"CHAOS"` (red team)

## Playback State

From `/replay/playback`:

```json
{
  "time": 123.45,
  "length": 1234.56,
  "paused": false,
  "speed": 16.0
}
```

- **time** (float): Current playback position in seconds
- **length** (float): Total replay duration in seconds
- **paused** (boolean): Is replay paused?
- **speed** (float): Playback speed multiplier (1.0 = normal, 16.0 = 16×, etc.)

## Render State

From `/replay/render`:

```json
{
  "cameraAttached": true,
  "selectionName": "Ahri",
  "cameraPosition": {
    "x": 8040.5,
    "y": 145.3,
    "z": 6000.0
  },
  "cameraLookAt": {...},
  "mapSize": [14500, 14500]
}
```

### Fields (relevant for this project)

- **cameraAttached** (boolean): Is the camera following a unit?
- **selectionName** (string): Name of the unit camera is attached to
- **cameraPosition.x** (float): Map X coordinate
- **cameraPosition.z** (float): Map Y coordinate (note: called `z` in API)

**Important**: The API uses `z` for the vertical game axis, but in a 2D context it represents the Y-axis of the map.

## Map Coordinates

The Summoner's Rift map is ~14,500 × 14,500 units.

**Key locations**:
- Blue Nexus: (~400, ~400)
- Red Nexus: (~14,000, ~14,000)
- Dragon pit: (~9,800, ~4,500)
- Baron pit: (~5,000, ~9,500)
- Blue Base: (0, 0) to (~2,000, ~2,000)
- Red Base: (~12,500, ~12,500) to (~14,500, ~14,500)

## Output Image

Saved as PNG to `outputs/[MATCH_ID] champion - player (k/d/a).png`.

**Format**:
- RGBA PNG
- Downscaled 4× from 8192×8192 → 2048×2048
- Path drawn as gradient lines (blue → red)
- Line width: 3 pixels
- Line opacity: ~80%

## Error Cases

### Corrupted positions file

If `cache/positions_*.json` is malformed:
- Script exits with "Positions file could not be read"
- **Fix**: Delete the file and re-record

### Missing coordinates

If `x` or `y` is null/missing:
- That sample is skipped
- **Cause**: Brief network glitch or API stall
- **Impact**: Minor gap in path, usually imperceptible

### Timestamp gaps

If `game_time` jumps by > 0.1s:
- Indicates a network hiccup or API overload
- Path rendering bridges the gap (linear interpolation via line drawing)
- **Normal for polls > 0.1s**
