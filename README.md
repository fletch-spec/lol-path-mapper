# LoL Path Mapper

Record and visualize champion movement paths from League of Legends live replays.

## Quick Start

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Enable Replay API**: Add `EnableReplayApi=1` to `game.cfg` (see [SETUP.md](docs/SETUP.md))
3. **Place map image**: `summoners_rift.png` in the project root
4. **Run**: `python record_path.py`
5. **Follow prompts**:
   - Wait for replay to load
   - Select a player from the list
   - Set follow camera on player (after speed up starts)
   - Script records movement and renders path
6. **Output**: Saved to `outputs/[MATCH_ID] champion - player (k-d-a).png` (opens automatically on Windows)

## Usage

```bash
python record_path.py
```

The script will:
1. Wait for a replay to load in the LoL client
2. List all players and prompt for selection
3. Attach the camera to the selected champion
4. Record their movement throughout the game (cached to disk — skip this step on re-run)
5. Render a gradient path (blue → red) with white arrows marking each recall/teleport, and start/end dots

## Documentation

- **[docs/README.md](docs/README.md)** - Documentation index
- **[docs/SETUP.md](docs/SETUP.md)** - Installation and configuration
- **[docs/WORKFLOW.md](docs/WORKFLOW.md)** - Detailed workflow and troubleshooting
- **[docs/API.md](docs/API.md)** - LoL Replay API reference
- **[docs/DATA.md](docs/DATA.md)** - Data structures and formats
