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
| `--output` | `outputs/<summoner>_<champion>.png` | Custom output path |
| `--map` | `.dev/summoners_rift.png` | Map background image |

**Examples:**

```bash
# Interactive player selection
python main.py

# Select by champion name, faster playback
python main.py --player Ahri --speed 16

# Full resolution output
python main.py --player 3 --downscale 1
```

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

## Output

- PNGs are saved to `outputs/` as `<summoner>_<champion>.png`
- Path color: blue (game start) → red (game end)
- Green dot = starting position, red dot = ending position
- Position data is cached to `.dev/cache/positions_<champion>.json` for re-rendering

## Project Structure

```
main.py          # Entry point: connect to replay, record & render
replay_api.py    # LoL replay API client
path_renderer.py # PIL-based path rendering onto map image
render.py        # Re-render from cached position data
requirements.txt # Python dependencies (Pillow, requests)
.dev/            # gitignored: map image, replay files, cache, keys
outputs/         # gitignored: generated path visualization PNGs
```
