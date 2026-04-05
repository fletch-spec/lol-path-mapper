"""Ward placement visualizer.

Generates two images from a Riot match timeline JSON:
  <match_id>_wards.png  — dot map showing where each ward was placed
  <match_id>_vision.png — heatmap of accumulated ward vision coverage

Exact ward positions are read directly from the WARD_PLACED events in the
Riot Match API v5 timeline. Older timeline files without position data fall
back to the creator's 60-second frame snapshot position automatically.

Usage:
    python wards.py                                          # most recent timeline in .dev/cache/
    python wards.py .dev/cache/timeline_OC1_697009636.json
    python wards.py ... --team blue
    python wards.py ... --participant 5
    python wards.py ... --downscale 2
    python wards.py ... --no-cache
"""

import argparse
import os
import sys

from ward_analyzer import (
    CACHE_DIR,
    extract_ward_events,
    latest_timeline_file,
    load_timeline,
    load_ward_events,
    match_id_from_path,
    save_ward_events,
)
from ward_renderer import render_vision_heatmap, render_ward_map

DEFAULT_MAP = os.path.join(os.path.dirname(__file__), ".dev", "summoners_rift.png")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")


def main():
    parser = argparse.ArgumentParser(description="Ward placement visualizer")
    parser.add_argument("timeline", nargs="?", help="Riot timeline JSON path (default: most recent in .dev/cache/)")
    parser.add_argument("--map", default=DEFAULT_MAP, help="Map background image")
    parser.add_argument("--downscale", type=int, default=4,
                        help="Downscale factor for output (default: 4 → 2048x2048)")
    parser.add_argument("--team", choices=["blue", "red", "both"], default="both",
                        help="Filter by team (default: both)")
    parser.add_argument("--participant", type=int, default=None,
                        help="Filter by participant ID 1-10 (overrides --team)")
    parser.add_argument("--no-cache", action="store_true",
                        help="Ignore cached ward events and re-extract from timeline")
    args = parser.parse_args()

    timeline_path = args.timeline or latest_timeline_file()
    if not timeline_path or not os.path.exists(timeline_path):
        print("No timeline file found. Provide a path or place timeline_*.json in .dev/cache/")
        sys.exit(1)

    if not os.path.exists(args.map):
        print(f"Error: map image not found at {args.map}")
        sys.exit(1)

    match_id = match_id_from_path(timeline_path)
    cache_path = os.path.join(CACHE_DIR, f"wards_{match_id}.json")

    if not args.no_cache and os.path.exists(cache_path):
        print(f"Loading cached ward events from {cache_path}")
        ward_events = load_ward_events(cache_path)
    else:
        print(f"Extracting ward events from {timeline_path}...")
        ward_events = extract_ward_events(load_timeline(timeline_path))
        save_ward_events(ward_events, cache_path)
        print(f"Extracted {len(ward_events)} ward placements → cached at {cache_path}")

    # Apply filters
    if args.participant is not None:
        ward_events = [e for e in ward_events if e["creator_id"] == args.participant]
        print(f"Filtered to participant {args.participant}: {len(ward_events)} wards")
    elif args.team == "blue":
        ward_events = [e for e in ward_events if e["creator_id"] <= 5]
        print(f"Filtered to blue team: {len(ward_events)} wards")
    elif args.team == "red":
        ward_events = [e for e in ward_events if e["creator_id"] > 5]
        print(f"Filtered to red team: {len(ward_events)} wards")
    else:
        print(f"Using all {len(ward_events)} ward placements (both teams)")

    if not ward_events:
        print("No ward events after filtering.")
        sys.exit(0)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    suffix = (f"_p{args.participant}" if args.participant is not None
              else f"_{args.team}" if args.team != "both" else "")

    ward_out = os.path.join(OUTPUT_DIR, f"{match_id}_wards{suffix}.png")
    vision_out = os.path.join(OUTPUT_DIR, f"{match_id}_vision{suffix}.png")

    print(f"\nRendering ward map...")
    render_ward_map(args.map, ward_events, ward_out, downscale=args.downscale)

    print(f"\nRendering vision heatmap...")
    render_vision_heatmap(args.map, ward_events, vision_out, downscale=args.downscale)

    print(f"\nDone.\n  {ward_out}\n  {vision_out}")


if __name__ == "__main__":
    main()
