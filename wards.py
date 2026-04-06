"""Ward placement visualizer.

Generates two images from a Riot match timeline JSON:
  <match_id>_wards.png  — dot map showing where each ward was placed
  <match_id>_vision.png — heatmap of accumulated ward vision coverage

Exact ward positions are read directly from the WARD_PLACED events in the
Riot Match API v5 timeline. Older timeline files without position data fall
back to the creator's 60-second frame snapshot position automatically.

Usage:
    python wards.py                                          # most recent timeline in cache/
    python wards.py cache/timeline_OC1_697009636.json
    python wards.py ... --team blue
    python wards.py ... --participant 5
    python wards.py ... --downscale 2
    python wards.py ... --no-cache
"""

import argparse
import os
import sys

# Ensure Unicode output works on Windows terminals
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from analysis.ward_analyzer import (
    CACHE_DIR,
    build_participant_map,
    extract_ward_events,
    latest_timeline_file,
    load_timeline,
    load_ward_events,
    match_id_from_path,
    match_json_path_from_timeline,
    save_ward_events,
    summoner_for_champion,
)
from cache import output_dir_for, upsert_game
from renderers.ward_renderer import render_vision_heatmap, render_ward_map

DEFAULT_MAP = os.path.join(os.path.dirname(__file__), "summoners_rift.png")


def main():
    parser = argparse.ArgumentParser(description="Ward placement visualizer")
    parser.add_argument("timeline", nargs="?", help="Riot timeline JSON path (default: most recent in cache/)")
    parser.add_argument("--map", default=DEFAULT_MAP, help="Map background image")
    parser.add_argument("--downscale", type=int, default=4,
                        help="Downscale factor for output (default: 4 → 2048x2048)")
    parser.add_argument("--team", choices=["blue", "red", "both"], default="both",
                        help="Filter by team (default: both)")
    parser.add_argument("--participant", type=int, default=None,
                        help="Filter by participant ID 1-10 (overrides --team)")
    parser.add_argument("--start", type=float, default=0,
                        help="Exclude wards placed before this many minutes (default: 0)")
    parser.add_argument("--end", type=float, default=None,
                        help="Exclude wards placed after this many minutes (default: end of game)")
    parser.add_argument("--no-cache", action="store_true",
                        help="Ignore cached ward events and re-extract from timeline")
    args = parser.parse_args()

    timeline_path = args.timeline or latest_timeline_file()
    if not timeline_path or not os.path.exists(timeline_path):
        print("No timeline file found.")
        print("  → Run  python cache.py --load  to fetch it automatically (needs a Riot API key).")
        print("  → Or download manually from Riot Match API v5 and save to cache/timeline_<matchId>.json")
        sys.exit(1)

    if not os.path.exists(args.map):
        print(f"Map image not found: {args.map}")
        print("  → Place summoners_rift.png in the project root.")
        sys.exit(1)

    match_id = match_id_from_path(timeline_path)

    # Resolve champion and summoner for --participant mode
    part_champion = part_summoner = None
    part_team_color = ""
    if args.participant is not None:
        match_json = match_json_path_from_timeline(timeline_path)
        part_map = build_participant_map(match_json_path=match_json)
        part_champion = part_map.get(args.participant)
        if part_champion:
            part_summoner = summoner_for_champion(match_json, part_champion)
        part_team_color = "blue" if args.participant <= 5 else "red"

    cache_path = os.path.join(CACHE_DIR, f"wards_{match_id}.json")

    if not args.no_cache and os.path.exists(cache_path):
        print(f"Loading cached ward events from {cache_path}")
        ward_events = load_ward_events(cache_path)
    else:
        print(f"Extracting ward events from {timeline_path}...")
        ward_events = extract_ward_events(load_timeline(timeline_path))
        save_ward_events(ward_events, cache_path)
        print(f"Extracted {len(ward_events)} ward placements -> cached at {cache_path}")

    # Drop structure/ability wards that have no meaningful placement position
    ward_events = [e for e in ward_events if e["ward_type"] != "UNDEFINED"]
    print(f"Excluded UNDEFINED (structure/ability) wards: {len(ward_events)} remaining")

    # Apply time window filter
    start_ms = int(args.start * 60_000)
    end_ms = int(args.end * 60_000) if args.end is not None else None
    if start_ms > 0 or end_ms is not None:
        ward_events = [
            e for e in ward_events
            if e["timestamp"] >= start_ms and (end_ms is None or e["timestamp"] < end_ms)
        ]
        window = f"{args.start:.0f}m" + (f"-{args.end:.0f}m" if args.end else "+")
        print(f"Time window {window}: {len(ward_events)} wards")

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

    time_suffix = ""
    if args.start > 0 or args.end is not None:
        time_suffix = f"_{args.start:.0f}m" + (f"-{args.end:.0f}m" if args.end else "plus")

    if args.participant is not None and part_champion:
        # Champion-specific → champion subdir
        out_dir = output_dir_for(match_id, part_champion)
        ward_rname, vision_rname = "wards", "vision"
        ward_out   = os.path.join(out_dir, f"wards{time_suffix}.png")
        vision_out = os.path.join(out_dir, f"vision{time_suffix}.png")
    elif args.team != "both":
        # Team-filtered → match dir
        out_dir = output_dir_for(match_id)
        ward_rname   = f"wards_{args.team}"
        vision_rname = f"vision_{args.team}"
        ward_out   = os.path.join(out_dir, f"wards_{args.team}{time_suffix}.png")
        vision_out = os.path.join(out_dir, f"vision_{args.team}{time_suffix}.png")
    else:
        # Both teams → match dir
        out_dir = output_dir_for(match_id)
        ward_rname, vision_rname = "wards_team", "vision_team"
        ward_out   = os.path.join(out_dir, f"wards_team{time_suffix}.png")
        vision_out = os.path.join(out_dir, f"vision_team{time_suffix}.png")
    os.makedirs(out_dir, exist_ok=True)

    print(f"\nRendering ward map...")
    render_ward_map(args.map, ward_events, ward_out, downscale=args.downscale)

    print(f"\nRendering vision heatmap...")
    render_vision_heatmap(args.map, ward_events, vision_out, downscale=args.downscale)

    upsert_game(match_id, champion=part_champion,
                summoner=part_summoner or "",
                team_color=part_team_color or args.team,
                renders=[ward_rname, vision_rname])

    print(f"\nDone.\n  {ward_out}\n  {vision_out}")


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as e:
        fn = e.filename or ""
        print(f"\nFile not found: {fn}")
        if "timeline" in fn:
            print("  → Download from Riot Match API v5 and save to cache/timeline_<matchId>.json")
        elif "wards_" in fn:
            print("  → The ward cache may be missing. Run with --no-cache to re-extract from the timeline.")
        elif "summoners_rift" in fn:
            print("  → Place summoners_rift.png in the project root.")
        else:
            print("  → Check the path and try again.")
        sys.exit(1)
    except (ValueError, KeyError) as e:
        print(f"\nTimeline JSON could not be read: {e}")
        print("  → Re-download from Riot API, or run with --no-cache if the ward cache is corrupted.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(0)
