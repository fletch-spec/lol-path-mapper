# League of Legends Replay Path Visualizer

Records a champion's movement from a LoL replay and renders it as a color-gradient path overlay on the Summoner's Rift map.

## Overview

While a replay is playing, this tool polls the local LoL replay API to collect position samples for a chosen champion. It then draws a smooth path — blue at the start, red at the end — on top of the full 8192×8192 Summoner's Rift map image, saving the result as a PNG.

## Requirements

- Python 3.x
- `pip install -r requirements.txt`
- A Summoner's Rift map image at `.dev/summoners_rift.png` (8192×8192)
- League of Legends client with the replay API enabled (see [Setup](#setup))

## Setup

```bash
pip install -r requirements.txt
```

Place your `summoners_rift.png` map image in the `.dev/` directory.

### Enable the Replay API

The LoL client does not expose the replay API by default. To enable it:

1. Close the League of Legends client completely.
2. Open `game.cfg`, located at:
   ```
   C:\Riot Games\League of Legends\Config\game.cfg
   ```
3. Find the `[General]` section and add (or update) this line:
   ```ini
   [General]
   EnableReplayApi=1
   ```
4. Save the file and relaunch the client.

> If the API is not enabled, the tool will detect the game but print:
> `Game detected but Replay API not enabled.`

## Usage

### Record from a replay

Open a replay in the LoL client, then run:

```bash
python main.py [options]
```

The tool waits for the replay API to become available, lists all players, and prompts you to pick one. It attaches the camera to the selected champion, collects positions until the replay ends, caches them, and renders the output PNG.

**Options:**

| Flag | Default | Description |
|------|---------|-------------|
| `--player` | *(prompt)* | Champion name, summoner name, or list number |
| `--speed` | `8` | Replay playback speed multiplier |
| `--downscale` | `4` | Output downscale factor (4 → 2048×2048) |
| `--timeline` | none | Riot timeline JSON for exact ward tracking |
| `--output` | `outputs/<summoner>_<champion>.png` | Custom output path |
| `--map` | `.dev/summoners_rift.png` | Map background image |

**Examples:**

```bash
# Interactive player selection
python main.py

# Path + ward locations in the same run
python main.py --player Ahri --timeline .dev/cache/timeline_OC1_697009636.json

# Select by champion name, faster playback
python main.py --player Ahri --speed 16

# Full resolution output
python main.py --player 3 --downscale 1
```

When `--timeline` is provided, a second image is saved alongside the path image:
- `outputs/<summoner>_<champion>.png` — movement path
- `outputs/<summoner>_<champion>_wards.png` — ward placement dots

Ward positions are captured at the exact game timestamp from the timeline, accurate to within one poll interval (~0.1s real time at 8× speed = ~0.8s game time).

### Re-render from cached data

If you've already recorded a replay, you can re-render without replaying it:

```bash
# Re-render the most recent cached positions
python render.py

# Re-render a specific cache file
python render.py .dev/cache/positions_Ahri.json

# Re-render at higher resolution
python render.py .dev/cache/positions_Ahri.json --downscale 2
```

### Ward visualization

Generate a ward location map and vision heatmap from a Riot match timeline JSON:

```bash
# Auto-detect the most recent timeline in .dev/cache/
python wards.py

# Specific timeline file
python wards.py .dev/cache/timeline_OC1_697009636.json

# Blue team only, higher resolution
python wards.py .dev/cache/timeline_OC1_697009636.json --team blue --downscale 2

# Single player (participant ID 1-10)
python wards.py .dev/cache/timeline_OC1_697009636.json --participant 5
```

This produces two images in `outputs/`:
- `<match_id>_wards.png` — dots at each ward placement (blue team = blue, red team = red)
- `<match_id>_vision.png` — heatmap of accumulated vision coverage (~900 unit radius per ward)

Exact ward positions are read directly from the `WARD_PLACED` events in the Riot Match API v5 timeline. Older timeline files without position data automatically fall back to the creator's nearest 60-second frame position.

**Ward options:**

| Flag | Default | Description |
|------|---------|-------------|
| `timeline` | most recent `.dev/cache/timeline_*.json` | Riot match timeline JSON |
| `--team` | `both` | `blue`, `red`, or `both` |
| `--participant` | all | Single participant ID (1–10), overrides `--team` |
| `--downscale` | `4` | Output downscale factor |
| `--no-cache` | false | Re-extract even if ward cache exists |

The timeline JSON must be fetched separately from the [Riot Match API](https://developer.riotgames.com/) (requires an API key) and saved to `.dev/cache/` as `timeline_<matchId>.json`.

## Output

- PNGs are saved to `outputs/`
- Path images: `<summoner>_<champion>.png` — blue (start) → red (end) gradient
- Ward maps: `<match_id>_wards.png` — blue/red dots per team
- Vision heatmaps: `<match_id>_vision.png` — blue/red glow by team
- Position data cached to `.dev/cache/positions_<champion>.json`
- Ward event data cached to `.dev/cache/wards_<match_id>.json`

## Project Structure

```
main.py           # Entry point: connect to replay, record & render path
replay_api.py     # LoL replay API client
path_renderer.py  # PIL-based path rendering onto map image
render.py         # Re-render path from cached position data
ward_analyzer.py  # Extract ward events from Riot timeline JSON
ward_renderer.py  # PIL-based ward map and vision heatmap rendering
wards.py          # Entry point: generate ward visualizations
requirements.txt  # Python dependencies (Pillow, requests)
.dev/             # gitignored: map image, replay files, cache, keys
outputs/          # gitignored: generated PNGs
```
