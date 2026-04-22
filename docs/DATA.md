# Data Structures & Formats

## Positions Cache

Filename: `cache/positions_{match_id}_{champion}_{summoner}.json`

The key includes `match_id` so two different replays of the same champion (or same player) don't collide. `match_id` is the Live Client `gameId` when non-zero; otherwise a 10-char sha1 hash of the sorted roster + game length (stable across reloads of the same replay).

```json
{
  "meta": {
    "match_id": "f2d548e465",
    "summoner": "Player Name",
    "champion": "Ahri",
    "kda": [5, 2, 12]
  },
  "positions": [
    [game_time, x, y],
    [game_time, x, y],
    ...
  ]
}
```

### Fields

- **meta.match_id** (string): See above
- **meta.summoner** (string): Summoner name (from `riotIdGameName` or `summonerName`)
- **meta.champion** (string): Champion name (e.g., "Ahri", "Nunu and Willump")
- **meta.kda** (array of 3 ints, optional): `[kills, deaths, assists]` snapshot taken after the recording finished, so cached re-renders get correct stats without replaying the game
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
    "match_id": "f2d548e465",
    "summoner": "Ahri Main",
    "champion": "Ahri",
    "kda": [5, 2, 12]
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
  "scores": {
    "kills": 5,
    "deaths": 2,
    "assists": 12,
    "creepScore": 180,
    "wardScore": 12.3
  }
}
```

### Fields (relevant for this project)

- **championName** (string): Champion pick (e.g., "Ahri")
- **riotIdGameName** (string): Riot ID name component (preferred for display)
- **riotIdTagLine** (string): Riot ID tag (e.g., "NA1", "EUW1")
- **summonerName** (string): Legacy summoner name (fallback if Riot ID not available)
- **team** (string): `"ORDER"` (blue team) or `"CHAOS"` (red team)
- **scores** (object): `kills`, `deaths`, `assists`, etc. — note: this field is `scores`, not `stats`. The script falls back to `stats` defensively for older API versions.

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

Saved as PNG to `outputs/[MATCH_ID] champion - player (k-d-a).png`.

**Format**:
- RGB PNG (RGBA overlay composited onto the map, then flattened)
- Downscaled 4× from 8192×8192 → 2048×2048
- Path drawn as gradient lines (blue → red) per segment
- Line width: `max(4, img_width // 300)` pixels (≈27px at 8192, ≈7px after downscale)
- Line opacity: 230/255 (~90%)
- Segments split on jumps > 3000 game units (recalls/teleports)
- Small white arrows at each segment boundary, each pointing at the other end of the jump
- Green dot at first sample, red dot at last sample

### Coordinate transform

Game world `(x, z)` → image pixels:

```
px = (x - MIN_X) / (MAX_X - MIN_X) * width
py = (1 - (z - MIN_Y) / (MAX_Y - MIN_Y)) * height - Y_SHIFT
```

Where `MIN_X/MAX_X = -120/14870`, `MIN_Y/MAX_Y = -120/14980`, and `Y_SHIFT = round(140 / 2048 * height)` — an empirical correction because the playfield sits ~140px higher than the raw bounds predict at 2048px resolution.

## Error Cases

### Corrupted positions file

If a `cache/positions_*.json` file is malformed, `load_positions` returns `None` and the script falls through to re-recording. Delete the file manually if you want to force a clean re-record.

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
