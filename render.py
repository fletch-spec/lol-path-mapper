"""Re-render a path image from a cached positions JSON file.

Usage:
    python render.py                              # picks the most recent positions file
    python render.py .dev/cache/positions_Ahri.json
    python render.py .dev/cache/positions_Ahri.json --downscale 2
"""

import argparse
import glob
import json
import os
import sys

from path_renderer import render_path

DEFAULT_MAP = os.path.join(os.path.dirname(__file__), ".dev", "summoners_rift.png")
CACHE_DIR = os.path.join(os.path.dirname(__file__), ".dev", "cache")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")


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
        positions = json.load(f)

    name = os.path.splitext(os.path.basename(path))[0].replace("positions_", "")
    print(f"Loaded {len(positions)} samples from {path}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output = args.output or os.path.join(OUTPUT_DIR, f"{name}.png")

    xy = [(x, y) for _, x, y in positions]
    render_path(args.map, xy, output, downscale=args.downscale)


if __name__ == "__main__":
    main()
