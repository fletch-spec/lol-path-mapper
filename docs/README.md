# Documentation

## Quick Start

1. **[SETUP.md](SETUP.md)** — Install dependencies and enable the Replay API
2. Run the script: `python record_path.py`
3. Open a replay in the LoL client
4. Select a player when prompted
5. Output saved to `outputs/[MATCH_ID] champion - player (k/d/a).png`

## Workflow

The script:

1. **Waits** for a replay to load in the LoL client
2. **Lists players** and prompts for interactive selection
3. **Attaches** the replay camera to the selected champion
4. **Records** their movement throughout the game at 16× speed (~77 seconds for a 20-minute game)
5. **Saves** position data to `cache/positions_{champion}.json`
6. **Renders** a gradient path visualization onto the map (blue = early, red = late)
7. **Outputs** the final image to `outputs/[MATCH_ID] champion - player (k/d/a).png`

## Documentation

- **[WORKFLOW.md](WORKFLOW.md)** — Detailed step-by-step workflow and troubleshooting
- **[API.md](API.md)** — LoL Replay API endpoints and error handling
- **[DATA.md](DATA.md)** — Data structures (positions cache, player objects, coordinates)

## Troubleshooting

See **[WORKFLOW.md § Troubleshooting](WORKFLOW.md#troubleshooting)** for common issues and fixes.
