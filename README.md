# League of Legends Replay Visualizer

Records and analyses a champion's game from a LoL replay. Produces map overlays and charts from the live replay API and Riot's match timeline.

---

## Quick Start

> Everything you need to go from a replay file to rendered outputs.

### 1. Install

```bash
python -m pip install -r requirements.txt
```

Place `summoners_rift.png` in the project root (8192×8192 recommended).

### 2. Add your replays

Copy `.rofl` replay files into the `replays/` folder, then check what you have:

```bash
python cache.py
```

### 3. Fetch game data (optional but recommended)

This downloads champion names, ward events, and match info from Riot's API automatically.

Get a free API key at **https://developer.riotgames.com** (log in → scroll to bottom → Generate API Key), then:

```bash
python cache.py --load
```

You'll be prompted to paste your key the first time. It's saved for future runs.
Development keys expire every 24 hours — just run `--load` again and paste a new one when prompted.

### 4. Enable the Replay API in the LoL client

Do this once. Open:
```
C:\Riot Games\League of Legends\Config\game.cfg
```
Under `[General]`, add:
```ini
EnableReplayApi=1
```
Save and relaunch the client.

### 5. Record a replay

Open a `.rofl` file in the LoL client, then run:

```bash
python main.py
```

Select your champion when prompted. The tool plays through the replay at speed and saves a path image to `outputs/`. Ward maps are included automatically if game data was loaded in step 3.

### 6. Generate analysis and ward maps

```bash
python cache.py OC1_000000000 --champion Ahri
python cache.py OC1_000000000
```

Replace `OC1_697009636` with your match ID and `Ahri` with the champion you recorded.
Run `python cache.py <match_id>` to get these commands pre-filled for any match.

### 7. Check your outputs

All images are saved to `outputs/<match_id>/<Champion>/`. Open them in any image viewer.

---

## Tools

### `cache.py` — Game index and command reference

The starting point for everything. Shows all your replays with game info (duration, patch, winner) and provides copy-paste commands for each match.

```bash
python cache.py                  # list all replays and recorded matches
python cache.py OC1_697009636    # full detail: roster, cache status, commands
python cache.py --load           # fetch match + timeline data from Riot API
python cache.py --scan           # index replay files without API calls
```

**`--load`** requires a Riot API key — you'll be prompted to paste it on first run. It fetches match and timeline JSON for every replay in `replays/` that doesn't have it yet, then updates `games.json` with champion names, queue type, and game metadata.

Development keys from the [Riot Developer Portal](https://developer.riotgames.com/) work fine — they allow 100 requests per 2 minutes, and `--load` paces itself automatically.

`games.json` is updated automatically every time you run any tool. The `← recorded` marker appears for any participant who has a positions file in `cache/`.

---

### `main.py` — Record from a live replay

Open a `.rofl` replay in the LoL client, then run:

```bash
python main.py [options]
```

The tool identifies the match automatically from the running replay, loads any cached timeline, lists all ten players, and prompts you to pick one (or pass `--player` to skip the prompt). It attaches the camera, plays through at high speed, saves position samples to `cache/`, and renders the path and ward images.

**Options:**

| Flag | Default | Description |
|------|---------|-------------|
| `--player` | *(prompt)* | Champion name, summoner name, or list number (1–10) |
| `--speed` | `16` | Replay playback speed multiplier |
| `--downscale` | `4` | Output downscale factor (4 → 2048×2048 from 8192×8192) |
| `--timeline` | auto | Override the auto-detected timeline path |
| `--output` | auto | Override output image path |
| `--map` | `summoners_rift.png` | Map background image |

**Examples:**

```bash
python main.py --player Ahri      # record Ahri (timeline auto-detected)
python main.py                    # interactive player selection
python main.py --player Ahri --speed 32
python main.py --player 3 --downscale 1   # full 8192×8192 output
```

**Outputs** (in `outputs/<match_id>/Ahri/`):

| File | Description |
|------|-------------|
| `path.png` | Movement path, blue start → red end |
| `wards.png` | Ward placement dots (rendered when timeline is available) |

**Cache written:** `cache/positions_<Champion>.json`

---

### `render.py` — Re-render from cached positions

Re-generate the path image without re-running a replay:

```bash
python render.py                                        # most recent positions file
python render.py cache/positions_Ahri.json
python render.py cache/positions_Ahri.json --downscale 2
```

**Output:** `outputs/<match_id>/Champion/path.png`

---

### `wards.py` — Ward placement visualization

Generate a ward dot map and vision heatmap from a Riot timeline JSON.

```bash
python wards.py cache/timeline_OC1_697009636.json
python wards.py cache/timeline_OC1_697009636.json --team blue
python wards.py cache/timeline_OC1_697009636.json --participant 8
python wards.py cache/timeline_OC1_697009636.json --start 0 --end 15
```

**Options:**

| Flag | Default | Description |
|------|---------|-------------|
| `timeline` | most recent `cache/timeline_*.json` | Riot match timeline JSON |
| `--team` | `both` | `blue`, `red`, or `both` |
| `--participant` | all | Single participant ID (1–10); overrides `--team` |
| `--start` | `0` | Exclude wards placed before this many minutes |
| `--end` | end | Exclude wards placed after this many minutes |
| `--downscale` | `4` | Output downscale factor |
| `--no-cache` | false | Re-extract from timeline even if ward cache exists |

**Outputs** (in `outputs/<match_id>/`):

| Scenario | Files |
|----------|-------|
| Both teams (default) | `wards_team.png`, `vision_team.png` |
| Single team | `wards_blue.png`, `vision_blue.png` |
| Single player | `<Champion>/wards.png`, `<Champion>/vision.png` |
| With time window | `wards_team_0m-15m.png`, etc. |

---

### `analyze.py` — Match insights

Generate four analytical images for a single player.

```bash
python analyze.py cache/timeline_OC1_697009636.json --champion Ahri
python analyze.py cache/timeline_OC1_697009636.json --participant 5
python analyze.py cache/timeline_OC1_697009636.json --champion Ahri --downscale 2
```

**Options:**

| Flag | Default | Description |
|------|---------|-------------|
| `timeline` | most recent `cache/timeline_*.json` | Riot match timeline JSON |
| `--champion` | — | Champion name (case-insensitive) |
| `--participant` | — | Participant ID 1–10 (alternative to `--champion`) |
| `--positions` | auto | Positions JSON path (overrides auto-detect) |
| `--map` | `summoners_rift.png` | Map background image |
| `--downscale` | `4` | Output downscale factor |

**Output images** (in `outputs/<match_id>/<Champion>/`):

| File | Description |
|------|-------------|
| `activity.png` | Activity strip, CS/gold per minute, event timeline, stats panel |
| `xp_heatmap.png` | Where XP was earned on the map (requires positions from `main.py`) |
| `fights.png` | Team fight and skirmish clusters across the map |
| `lane.png` | Laning-phase positions and aggression score (requires positions from `main.py`) |

---

## File structure

```
replays/              Add .rofl replay files here

cache/                Auto-managed — do not edit manually
  games.json            Index of all cached matches
  api_key.txt           Your Riot API key (never committed)
  timeline_<id>.json    Riot timeline data
  match_<id>.json       Riot match data
  positions_<champ>.json  Recorded position samples
  wards_<id>.json       Pre-extracted ward events

outputs/              Generated PNG images
  <match_id>/
    <Champion>/
      path.png  wards.png  activity.png  xp_heatmap.png  fights.png  lane.png
    wards_team.png  vision_team.png
```

---

## Technical reference

### Data sources

| Data | Source | How to get it |
|------|--------|---------------|
| Position samples | Local replay API at `https://127.0.0.1:2999` | Run `main.py` while a replay is open |
| Ward events, kills, XP | Riot Match API v5 timeline | `python cache.py --load` |
| Champion names, metadata | Riot Match API v5 match | `python cache.py --load` |

### Enable the Replay API

The LoL client does not expose the replay API by default:

1. Close the League of Legends client completely.
2. Open `C:\Riot Games\League of Legends\Config\game.cfg`
3. Under `[General]`, add:
   ```ini
   EnableReplayApi=1
   ```
4. Save and relaunch.

> If the API is not enabled, `main.py` will print: `Game detected but Replay API not enabled.`

### Riot API key

`cache.py --load` prompts for your key on first run and saves it to `cache/api_key.txt` (gitignored). You can also set `RIOT_API_KEY` as an environment variable. Development keys expire every 24 hours — run `--load` again and paste a new key when prompted.

Match IDs use the format `<platform>_<numericId>` (e.g. `OC1_697009636`). The platform prefix matches the region: `NA1`, `EUW1`, `OC1`, etc.
