"""Re-render a path image from a cached positions JSON file.

Usage:
    python render.py                              # picks the most recent positions file
    python render.py cache/positions_Ahri.json
    python render.py cache/positions_Ahri.json --downscale 2
"""

import argparse
import glob
import json
import os
import sys

# Ensure Unicode output works on Windows terminals
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from renderers.path_renderer import render_path
from analysis.ward_analyzer import latest_timeline_file, match_id_from_path
from cache import CACHE_DIR, output_dir_for, upsert_game

DEFAULT_MAP = os.path.join(os.path.dirname(__file__), "summoners_rift.png")


def latest_positions_file():
    files = glob.glob(os.path.join(CACHE_DIR, "positions_*.json"))
    if not files:
        return None
    return max(files, key=os.path.getmtime)


def main():
    parser = argparse.ArgumentParser(description="Re-render path from cached positions JSON")
    parser.add_argument("positions", nargs="?", help="Path to positions JSON (default: most recent)")
    parser.add_argument("--map", default=DEFAULT_MAP, help="Map background image")
    parser.add_argument("--output", default=None, help="Output image path")
    parser.add_argument("--downscale", type=int, default=4,
                        help="Downscale factor (default: 4 → 2048x2048)")
    args = parser.parse_args()

    path = args.positions or latest_positions_file()
    if not path or not os.path.exists(path):
        print("No positions file found. Run main.py first to record a replay.")
        sys.exit(1)

    with open(path) as f:
        data = json.load(f)

    # Handle both new dict format {"meta": ..., "positions": [...]} and old raw-list format
    if isinstance(data, dict):
        meta      = data.get("meta", {})
        summoner  = meta.get("summoner", "")
        champion  = meta.get("champion", "")
        positions = data.get("positions", [])
    else:
        positions = data
        champion  = os.path.splitext(os.path.basename(path))[0].replace("positions_", "")
        summoner  = ""

    if not positions:
        print("Positions file is empty — no movement data was recorded.")
        print("  → Re-record the replay with main.py and try again.")
        sys.exit(1)

    print(f"Loaded {len(positions)} samples from {path}")

    if not os.path.exists(args.map):
        print(f"Map image not found: {args.map}")
        print("  → Place summoners_rift.png in the project root.")
        sys.exit(1)

    # Best-effort match ID from the most recent cached timeline
    timeline = latest_timeline_file()
    match_id = match_id_from_path(timeline) if timeline else ""

    if args.output:
        output = args.output
    else:
        folder = output_dir_for(match_id or None, champion)
        os.makedirs(folder, exist_ok=True)
        output = os.path.join(folder, "path.png")

    xy = [(x, y) for _, x, y in positions]
    render_path(args.map, xy, output, downscale=args.downscale)
    upsert_game(match_id or None, champion=champion, summoner=summoner, renders=["path"])


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as e:
        fn = e.filename or ""
        print(f"\nFile not found: {fn}")
        if "positions" in fn:
            print("  → Run main.py first to record a replay, then retry.")
        elif "summoners_rift" in fn:
            print("  → Place summoners_rift.png in the project root.")
        else:
            print("  → Check the path and try again.")
        sys.exit(1)
    except (ValueError, KeyError) as e:
        print(f"\nPositions file could not be read: {e}")
        print("  → It may be corrupted. Delete it from cache/ and re-record with main.py.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(0)
