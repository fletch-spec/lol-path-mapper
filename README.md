# League of Legends Replay Visualizer

Records and analyses a champion's game from a LoL replay. Produces map overlays and charts from both the live replay API and Riot's match timeline JSON.

## Overview

While a replay is playing, the tool polls the local LoL replay API to collect position samples for a chosen champion. It renders those positions as a smooth blue→red gradient path on the Summoner's Rift map. Additional outputs — ward maps, XP heatmap, team fight clusters, activity chart, lane aggression — are generated from Riot Match API v5 data cached in `.dev/cache/`.

## Requirements

- [Python](https://www.python.org/downloads/) 3.x
- `pip install -r requirements.txt`
- A Summoner's Rift map image at `.dev/summoners_rift.png` (8192×8192 recommended)
- League of Legends client with the replay API enabled (see [Setup](#setup))
- Riot API timeline JSON and match JSON saved to `.dev/cache/` (for insights)

## Setup

```bash
python -m pip install -r requirements.txt
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

---

## Usage

### Record from a replay — `main.py`

Open a replay in the LoL client, then run:

```bash
python main.py [options]
```

The tool waits for the replay API, lists all players, and prompts you to pick one. It attaches the camera to the selected champion, collects positions until the replay ends, caches them, and renders the output PNG.

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
- `outputs/<summoner>_<champion>_wards.png` — ward placement dots (exact positions from timeline)

---

### Re-render from cached data — `render.py`

If you've already recorded a replay, re-render without replaying it:

```bash
# Re-render the most recent cached positions
python render.py

# Re-render a specific cache file
python render.py .dev/cache/positions_Ahri.json

# Re-render at higher resolution
python render.py .dev/cache/positions_Ahri.json --downscale 2
```

---

### Ward visualization — `wards.py`

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

Produces two images in `outputs/`:
- `<match_id>_wards.png` — dots at each ward placement (blue team = blue, red team = red)
- `<match_id>_vision.png` — heatmap of accumulated vision coverage (~900 unit radius per ward)

Exact ward positions are read directly from `WARD_PLACED` events in the Riot Match API v5 timeline. Older files without position data fall back to the creator's nearest 60-second frame position automatically.

**Options:**

| Flag | Default | Description |
|------|---------|-------------|
| `timeline` | most recent `.dev/cache/timeline_*.json` | Riot match timeline JSON |
| `--team` | `both` | `blue`, `red`, or `both` |
| `--participant` | all | Single participant ID (1–10), overrides `--team` |
| `--downscale` | `4` | Output downscale factor |
| `--no-cache` | false | Re-extract even if ward cache exists |

---

### Match insights — `analyze.py`

Generate four analytical images for a single player using the Riot timeline JSON. Requires a Riot API match JSON and optionally a cached positions file from `main.py`.

```bash
# By champion name (auto-finds participant from match JSON)
python analyze.py .dev/cache/timeline_OC1_697009636.json --champion Ahri

# By participant ID
python analyze.py .dev/cache/timeline_OC1_697009636.json --participant 5

# Higher resolution output
python analyze.py .dev/cache/timeline_OC1_697009636.json --champion Ahri --downscale 2
```

Produces four images in `outputs/` and a stats summary in the console.

**Options:**

| Flag | Default | Description |
|------|---------|-------------|
| `timeline` | most recent `.dev/cache/timeline_*.json` | Riot match timeline JSON |
| `--champion` | — | Champion name (case-insensitive) |
| `--participant` | — | Participant ID 1–10 (alternative to --champion) |
| `--positions` | auto | Path to positions JSON (overrides auto-detect) |
| `--map` | `.dev/summoners_rift.png` | Map background image |
| `--downscale` | `4` | Output downscale factor |

#### `<match_id>_<champion>_activity.png` — Activity chart

A four-panel dark-theme chart:

- **CS per minute** — bar chart with average dashed line
- **Event timeline** — exact-timestamp markers for kills (▲), deaths (✕), assists (◆), towers (▼), objectives (★), recalls (●). These come directly from event timestamps, not 60-second frame snapshots.
- **Activity strip** — 15-second resolution colour bands: Farming / Fighting / Base / Roaming
- **Gold per minute** — bar chart
- **Stats panel** (right column) — KDA, CS, gold, tower/objective participations, recalls

#### `<match_id>_<champion>_xp_heatmap.png` — XP heatmap

Shows where the player earned XP across the map. Each minute's XP gain is distributed across all position samples from that 60-second window (~40–80 samples), giving ~1000–2000 weighted data points per game rather than one blob per minute. Rendered with the plasma colourmap (dark purple = low, yellow = high) and log normalization so lane farming stays visible alongside objective spikes. Includes a "Low XP / High XP" colorbar.

> Requires `positions_<champion>.json` from a recorded replay.

#### `<match_id>_<champion>_fights.png` — Team fight clusters

All champion kills from the match are grouped into skirmishes (2–3 kills) and team fights (4+ kills). Each cluster appears as a numbered circle on the map:

- Circle **radius** encodes kill count (cube-root scale — explained in the on-image legend)
- Circle **colour**: blue = blue team won, red = red team won, grey = even
- **Kill dots** inside the circle show exactly where each death occurred, coloured by the victim's team (blue dot = blue player died, red dot = red player died)
- Team fights (4+ kills) are filled; skirmishes are outlined and semi-transparent
- A **legend panel** (bottom-left) lists every fight: `# | TF/SK | time | ×kills | winner`

The circle numbers match the legend rows and the console output, making it easy to cross-reference all three.

#### `<match_id>_<champion>_lane.png` — Lane aggression

Shows where the player was positioned during the first 15 minutes:

- **Orange density cloud** — every sampled position during the laning phase
- **Orange circle marker** — average position across all laning samples
- **Aggression score (0–100)** — measures how far forward the player was positioned relative to the two bases. 0 = camped under own tower, 50 = neutral (river), 100 = always at enemy tower.
- A gauge bar and "Defensive ◀ ▶ Aggressive" axis labels are drawn on the image for quick reading.

> Requires `positions_<champion>.json` from a recorded replay.

---

## Data sources

| Data | Source | How to obtain |
|------|--------|---------------|
| Position samples | Live replay API (`/replay/render`) | Run `main.py` while a replay is open |
| Ward placements | Riot Match API v5 timeline | Save as `.dev/cache/timeline_<matchId>.json` |
| Participant names | Riot Match API v5 match data | Save as `.dev/cache/match_<matchId>.json` |

The Riot Match API requires an API key from the [Riot Developer Portal](https://developer.riotgames.com/).

---

## Output files

| File | Description |
|------|-------------|
| `outputs/<summoner>_<champion>.png` | Movement path (blue start → red end) |
| `outputs/<summoner>_<champion>_wards.png` | Single-player ward placement map |
| `outputs/<match_id>_wards.png` | All-player ward map from `wards.py` |
| `outputs/<match_id>_vision.png` | Ward vision heatmap |
| `outputs/<match_id>_<champion>_activity.png` | Activity & stats chart |
| `outputs/<match_id>_<champion>_xp_heatmap.png` | XP gain heatmap |
| `outputs/<match_id>_<champion>_fights.png` | Team fight cluster map |
| `outputs/<match_id>_<champion>_lane.png` | Lane aggression map |
| `.dev/cache/positions_<champion>.json` | Cached position samples |
| `.dev/cache/wards_<match_id>.json` | Cached ward events |

---

## Project structure

```
main.py               Entry point: connect to replay, record positions, render path + wards
replay_api.py         LoL replay API client (position polling, camera control, playback)
path_renderer.py      PIL path rendering; coordinate transform (game units -> pixels)
render.py             Re-render path from cached position data

ward_analyzer.py      Extract ward events from Riot timeline JSON; participant mapping
ward_renderer.py      PIL ward dot map and vision heatmap rendering
wards.py              Entry point: generate ward visualizations from timeline

insights.py           Pure-computation analysis: XP locations, activity classification,
                        lane aggression score, team fight clustering, event timestamps
insights_renderer.py  PIL/matplotlib rendering for all insight outputs
analyze.py            Entry point: generate all four insight images for a player

requirements.txt      Python dependencies (Pillow, requests, matplotlib, numpy)
.dev/                 gitignored: map image, timeline/match JSON cache, API keys
outputs/              gitignored: generated PNG images
```
