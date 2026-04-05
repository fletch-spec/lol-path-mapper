import argparse
import os
import re
import sys

from replay_api import wait_for_replay, get_players, collect_positions, save_positions
from path_renderer import render_path

DEFAULT_MAP = os.path.join(os.path.dirname(__file__), ".dev", "summoners_rift.png")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")


def make_output_path(summoner, champion):
    def clean(s):
        return re.sub(r"[^\w\-]", "_", s).strip("_")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    return os.path.join(OUTPUT_DIR, f"{clean(summoner)}_{clean(champion)}.png")


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
    parser.add_argument("--speed", type=int, default=8, help="Replay playback speed (default: 8)")
    parser.add_argument("--downscale", type=int, default=4,
                        help="Downscale factor for output (default: 4 → 2048x2048 from 8192x8192)")
    args = parser.parse_args()

    if not os.path.exists(args.map):
        print(f"Error: Map image not found at {args.map}")
        sys.exit(1)

    wait_for_replay()
    players = get_players()
    selected = select_player(players, args.player)
    champ = selected["championName"]
    summoner = selected.get("riotIdGameName") or selected.get("summonerName", "unknown")
    print(f"\nTracking: {champ} ({summoner})\n")

    positions = collect_positions(champ, speed=args.speed, summoner_name=summoner)
    save_positions(positions, champ)

    output = args.output or make_output_path(summoner, champ)
    print(f"Output: {output}")
    xy = [(x, y) for _, x, y in positions]
    render_path(args.map, xy, output, downscale=args.downscale)


if __name__ == "__main__":
    main()
