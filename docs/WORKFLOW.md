# Recording Workflow

## Overview

The script records a champion's movement by:
1. Waiting for a replay to load
2. Attaching the camera to a selected champion
3. Playing the replay at high speed while polling camera position
4. Rendering the collected positions as a gradient path overlay

## Step-by-Step

### 1. Wait for Replay

```
wait_for_replay()
```

- Polls `/liveclientdata/allgamedata` every 2 seconds
- Confirms `/replay/playback` API is enabled
- Blocks until both are reachable

**Why**: The API is only available while a replay is actively open. The script waits for you to open a `.rofl` file in the client.

### 2. Player Selection

```
players = get_players()
selected = select_player(players, args.player)
```

Displays:
```
Players:
   1. PlayerName#NA1          Ahri            (Blue)
   2. Enemy#NA1               Lux             (Red)
   ...
```

Selection modes:
- **Interactive** (no `--player` arg): prompts for a number
- **By index** (`--player 3`): selects player #3
- **By name** (`--player Ahri`): substring match on champion or summoner name

### 3. Camera Attachment & Verification

```
_attach_camera(champion_name, summoner_name)
```

The script:
1. Starts replay at 1× speed from t=5s (ensures champion is loaded)
2. Waits 3 seconds for the engine to render
3. Posts `cameraAttached: true` with the champion's name (tries multiple formats)
4. Verifies camera is moving by comparing positions at t, t+1.5s

**Why multiple name attempts?**
- The API may expect "Ahri" or "ahri" or "Ahri" depending on the region
- Multi-word champions like "Nunu and Willump" may need the summoner name instead

### 4. Position Collection

```
positions = collect_positions(champion_name, speed=16, summoner_name=summoner_name)
```

The script:
1. Rewinds to t=0.5s and pauses
2. Sets playback speed to `--speed` (default 16×) and unpauses
3. Polls `/replay/render` → `cameraPosition` every 0.1 seconds
4. Records `(game_time, x, y)` for each unique game_time
5. Continues until replay reaches end (game_length)

**Sample output**:
```
Collecting positions — 1234s game @ 16x speed (≈77s real time)
  100.0%  1234s / 1234s  | 1523 samples
Done: 1523 samples collected.
```

### 5. Save Positions

```
save_positions(positions, champion_name, summoner_name)
```

Writes to `cache/positions_{champion_name}.json`:
```json
{
  "meta": {
    "summoner": "Summoner Name",
    "champion": "Ahri"
  },
  "positions": [
    [0.0, 8040.5, 145.3],
    [0.1, 8041.2, 146.1],
    ...
  ]
}
```

### 6. Render Path

```
render_path(map_image, xy_positions, output_path, downscale=4)
```

The script:
1. Loads the Summoner's Rift map image
2. Draws lines between consecutive positions with a gradient color:
   - **Blue** (early game)
   - **Purple** (mid)
   - **Red** (late game)
3. Downscales the image 4× (8192×8192 → 2048×2048)
4. Saves to `outputs/[MATCH_ID] champion - player (k/d/a).png`

**Example output path**:
```
outputs/[OC1_697009636] Ahri - PlayerName (5/2/12).png
```

## Troubleshooting

### "Waiting for League replay..."

The script can't reach the replay API at `https://127.0.0.1:2999`.

**Fixes**:
- Open a `.rofl` file in the LoL client
- Ensure `EnableReplayApi=1` in `game.cfg`
- Check no firewall blocks port 2999
- Restart the client

### "Game detected but Replay API not enabled"

The replay is open, but the API is disabled.

**Fix**:
- Add `EnableReplayApi=1` to `game.cfg` and restart the replay

### "Could not load the player list"

The replay closed while the script was running.

**Fix**:
- Keep the replay open and running throughout
- Re-run the command

### "Camera not following {champion}"

The camera attachment failed.

**Possible causes**:
- Champion name doesn't match (try a different format or use index)
- Replay paused or crashed
- Camera still initializing (let it run a moment longer)

**Fix**:
- Re-run and try `--player <index>` instead of name

### Camera position is 0,0 or unchanged

The camera is attached but not moving.

**Possible causes**:
- Replay is paused
- The champion died and respawned (reset to base)
- API response is stale

**Fix**:
- Let the replay continue playing (don't pause)
- Try again from a different game state

### "Map image not found"

The script can't find `summoners_rift.png`.

**Fix**:
- Place the map image in the project root
- Or use `--map <path>` to specify a custom path
