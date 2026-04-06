"""
Entry point: record a champion's path from a live replay and render it.

Workflow:
  1. Wait for the LoL client to have an active replay loaded.
  2. List all players; let the user pick one (or pass --player on the CLI).
  3. Attach the replay camera to the selected champion and play through at speed.
  4. Save the collected (game_time, x, y) positions to cache/positions_<champion>.json.
  5. Render a blue→red gradient path overlay onto the Summoner's Rift map.
  6. If --timeline is provided, also render a ward placement dot map.

Usage:
    python main.py
    python main.py --player Ahri
    python main.py --player Ahri --speed 32
    python main.py --player 3 --downscale 1
    python main.py --player Ahri --timeline cache/timeline_OC1_697009636.json

**Options:**

| Flag | Default | Description |
|------|---------|-------------|
| `--player` | *(prompt)* | Champion name, summoner name, or list number (1–10) |
| `--speed` | `16` | Replay playback speed multiplier |
| `--downscale` | `4` | Output downscale factor (4 → 2048×2048 from 8192×8192) |
| `--timeline` | auto | Override the auto-detected timeline path |
| `--output` | auto | Override output image path |
| `--map` | `summoners_rift.png` | Map background image |
"""

import argparse
import os
import sys

# Ensure Unicode output works on Windows terminals
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from api.replay_api import wait_for_replay, get_game_data, get_players, collect_positions, save_positions, ReplayNotAvailable
from cache import CACHE_DIR, find_rofl_files, output_dir_for, upsert_game
from renderers.path_renderer import render_path
from renderers.ward_renderer import render_ward_map

DEFAULT_MAP = os.path.join(os.path.dirname(__file__), "summoners_rift.png")


def make_output_path(champion, match_id=None, type_="path"):
    """Build output path: outputs/{match_id}/{Champion}/{type}.png"""
    folder = output_dir_for(match_id, champion)
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, f"{type_}.png")


def select_player(players, player_arg):
    print("Players:")
    for i, p in enumerate(players, 1):
        name = p.get("riotIdGameName") or p.get("summonerName", "Unknown")
        tag = p.get("riotIdTagLine", "")
        champ = p["championName"]
        team = "Blue" if p["team"] == "ORDER" else "Red"
        display = f"{name}#{tag}" if tag else name
        print(f"  {i:2d}. {display:<25s} {champ:<15s} ({team})")

    if player_arg:
        # Try numeric index first, then substring match on champion / summoner name
        try:
            idx = int(player_arg) - 1
            if 0 <= idx < len(players):
                p = players[idx]
                print(f"\nSelected: {p['championName']}")
                return p
        except ValueError:
            pass
        query = player_arg.lower()
        for p in players:
            name = (p.get("riotIdGameName") or p.get("summonerName", "")).lower()
            if query in p["championName"].lower() or query in name:
                print(f"\nSelected: {p['championName']}")
                return p
        print(f"No match for '{player_arg}'")

    while True:
        try:
            choice = int(input(f"\nSelect player (1-{len(players)}): "))
            if 1 <= choice <= len(players):
                return players[choice - 1]
        except (ValueError, EOFError):
            pass
        print("Invalid choice.")


def main():
    parser = argparse.ArgumentParser(description="LoL Replay Pathing Visualizer")
    parser.add_argument("--player", help="Champion name, summoner name, or number")
    parser.add_argument("--output", default=None, help="Output image path")
    parser.add_argument("--map", default=DEFAULT_MAP, help="Map background image")
    parser.add_argument("--speed", type=int, default=16,
                        help="Replay playback speed multiplier (default: 16). "
                             "The in-game UI caps at 8x but the API accepts any value; "
                             "32x+ works but may desync camera position on slower machines.")
    parser.add_argument("--downscale", type=int, default=4,
                        help="Downscale factor for output (default: 4 → 2048x2048 from 8192x8192)")
    parser.add_argument("--timeline", default=None,
                        help="Riot match timeline JSON for exact ward tracking (cache/timeline_*.json)")
    args = parser.parse_args()

    if not os.path.exists(args.map):
        print(f"Map image not found: {args.map}")
        print("  → Place summoners_rift.png in the project root (8192×8192 recommended).")
        sys.exit(1)

    wait_for_replay()

    # Auto-detect match ID from the running replay
    game_id  = get_game_data().get("gameId")
    match_id = None
    if game_id:
        for mid in find_rofl_files():
            if str(game_id) in mid:
                match_id = mid
                break

    # Auto-detect cached timeline if --timeline not specified
    timeline_path = args.timeline
    if not timeline_path and match_id:
        candidate = os.path.join(CACHE_DIR, f"timeline_{match_id}.json")
        if os.path.exists(candidate):
            timeline_path = candidate
            print(f"Timeline auto-detected: {candidate}\n")

    try:
        players = get_players()
    except ReplayNotAvailable:
        print("Could not load the player list — the replay may have been closed or paused.")
        print("  → Keep the replay playing and try again.")
        sys.exit(1)
    selected = select_player(players, args.player)
    champ = selected["championName"]
    summoner = selected.get("riotIdGameName") or selected.get("summonerName", "unknown")
    print(f"\nTracking: {champ} ({summoner})\n")

    positions = collect_positions(champ, speed=args.speed, summoner_name=summoner)
    save_positions(positions, champ, summoner_name=summoner)

    # Derive match ID from timeline path as fallback (if game_id lookup failed)
    if not match_id and timeline_path:
        match_id = os.path.splitext(os.path.basename(timeline_path))[0].replace("timeline_", "")

    output = args.output or make_output_path(champ, match_id, "path")
    print(f"Path output: {output}")
    xy = [(x, y) for _, x, y in positions]
    render_path(args.map, xy, output, downscale=args.downscale)

    # Ward map: extract exact positions from timeline if available
    if timeline_path and os.path.exists(timeline_path):
        from analysis.ward_analyzer import (
            build_participant_map, extract_ward_events,
            load_timeline, match_json_path_from_timeline,
        )
        timeline = load_timeline(timeline_path)
        match_json = match_json_path_from_timeline(timeline_path)
        participant_map = build_participant_map(match_json_path=match_json, players=players)
        participant_id = next((pid for pid, c in participant_map.items() if c == champ), None)
        if participant_id is not None:
            ward_events = [e for e in extract_ward_events(timeline) if e["creator_id"] == participant_id]
            ward_output = make_output_path(champ, match_id, "wards")
            print(f"\nWard output ({len(ward_events)} placements): {ward_output}")
            render_ward_map(args.map, ward_events, ward_output, downscale=args.downscale)
            renders_produced = ["path", "wards"]
        else:
            print(f"Warning: {champ} not found in timeline participant map — ward image skipped")
            renders_produced = ["path"]
    elif timeline_path:
        print(f"Warning: timeline not found at {timeline_path} — ward image skipped")
        renders_produced = ["path"]
    else:
        renders_produced = ["path"]

    team_color = "blue" if selected.get("team") == "ORDER" else "red"
    upsert_game(match_id, champion=champ, summoner=summoner,
                team_color=team_color, renders=renders_produced)


if __name__ == "__main__":
    try:
        main()
    except ReplayNotAvailable as e:
        print(f"\n{e}")
        print("  → Keep the replay open and running, then try again.")
        sys.exit(1)
    except FileNotFoundError as e:
        fn = e.filename or ""
        print(f"\nFile not found: {fn}")
        if "summoners_rift" in fn:
            print("  → Place summoners_rift.png in the project root.")
        elif "timeline" in fn:
            print("  → Download the timeline from Riot Match API v5 and save to cache/timeline_<matchId>.json")
        else:
            print("  → Check the path and try again.")
        sys.exit(1)
    except KeyError as e:
        print(f"\nThe replay API returned unexpected data (missing field {e}).")
        print("  → Try restarting the replay or re-enabling the Replay API in game.cfg.")
        sys.exit(1)
    except ValueError as e:
        print(f"\nCould not read a data file: {e}")
        print("  → A JSON file in cache/ may be corrupted — delete it and re-record.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(0)
