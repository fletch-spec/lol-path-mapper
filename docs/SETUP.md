# Setup & Installation

## Prerequisites

- Python 3.7+
- League of Legends client with replay API enabled
- Map image file (`summoners_rift.png`, 8192×8192 recommended)

## Python Dependencies

```bash
pip install -r requirements.txt
```

(`requests`, `urllib3`, `Pillow`)

## Enable Replay API

The script communicates with LoL's local replay API at `https://127.0.0.1:2999`. This API is **disabled by default**.

### On Windows

1. Find your LoL installation directory (typically `C:\Riot Games\League of Legends`)
2. Locate `game.cfg` in the `Config` subfolder
3. Add or update the `[General]` section:
   ```ini
   [General]
   EnableReplayApi=1
   ```
4. Restart the client and replay

### Verify it's working

Open a replay. You should see no "Replay API not enabled" message when running the script.

## Map Image

Place a Summoner's Rift map image at the project root as `summoners_rift.png`.

**Recommended**: 8192×8192 pixels (native game resolution). Lower resolutions will reduce output quality.

Can be extracted from the client assets or sourced from community resources.
