"""Match insight generator.

Outputs for the selected player (in outputs/<match_id>/<champion>/):
  activity.png    — CS / gold / activity timeline chart
  xp_heatmap.png  — where XP was earned on the map
  fights.png      — team fight clusters (all 10 players)
  lane.png        — laning-phase positions + aggression score

Requires:
  - Riot Match API v5 timeline JSON  (cache/timeline_*.json)
  - Riot Match API v5 match JSON     (cache/match_*.json)  — for participant mapping
  - Cached position data             (cache/positions_<champion>.json)  — for XP heatmap / lane analysis

Usage:
    python analyze.py cache/timeline_OC1_697009636.json --champion Ahri
    python analyze.py cache/timeline_OC1_697009636.json --participant 5
    python analyze.py cache/timeline_OC1_697009636.json --champion Ahri --downscale 2

**Options:**

| Flag | Default | Description |
|------|---------|-------------|
| `timeline` | most recent `cache/timeline_*.json` | Riot match timeline JSON |
| `--champion` | — | Champion name (case-insensitive) |
| `--participant` | — | Participant ID 1–10 (alternative to `--champion`) |
| `--positions` | auto | Positions JSON path (overrides auto-detect) |
| `--map` | `summoners_rift.png` | Map background image |
| `--downscale` | `4` | Output downscale factor |
"""

import json
import os
import sys
import argparse

# Ensure Unicode output works on Windows terminals
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from cache import upsert_game, output_dir_for
from analysis.ward_analyzer import (
    build_participant_map,
    load_timeline,
    match_id_from_path,
    match_json_path_from_timeline,
    summoner_for_champion,
    CACHE_DIR,
)
from analysis.insights import (
    activity_stats,
    lane_aggression,
    per_minute_breakdown,
    per_15s_breakdown,
    player_event_times,
    team_fight_clusters,
    xp_gain_locations,
)
from renderers.insights_renderer import (
    render_activity_chart,
    render_lane_aggression,
    render_teamfight_clusters,
    render_xp_heatmap,
)

DEFAULT_MAP = os.path.join(os.path.dirname(__file__), "summoners_rift.png")


def _load_positions(champion_name, override_path=None):
    path = override_path or os.path.join(CACHE_DIR, f"positions_{champion_name}.json")
    if not os.path.exists(path):
        return None, path
    with open(path) as f:
        data = json.load(f)
    # Handle both new dict format {"meta": ..., "positions": [...]} and old raw-list format
    if isinstance(data, dict):
        return data.get("positions", []), path
    return data, path


def main():
    parser = argparse.ArgumentParser(description="Generate match insights for a player")
    parser.add_argument("timeline", nargs="?", help="Riot timeline JSON (default: most recent in cache/)")
    parser.add_argument("--champion",    default=None, help="Champion name")
    parser.add_argument("--participant", type=int, default=None, help="Participant ID 1-10")
    parser.add_argument("--positions",   default=None, help="Positions JSON path (overrides auto-detect)")
    parser.add_argument("--map",         default=DEFAULT_MAP)
    parser.add_argument("--downscale",   type=int, default=4)
    args = parser.parse_args()

    # Resolve timeline
    if not args.timeline:
        from analysis.ward_analyzer import latest_timeline_file
        args.timeline = latest_timeline_file()
    if not args.timeline or not os.path.exists(args.timeline):
        print("No timeline file found.")
        print("  → Run  python cache.py --load  to fetch it automatically (needs a Riot API key).")
        print("  → Or download manually from Riot Match API v5 and save to cache/timeline_<matchId>.json")
        sys.exit(1)

    if not os.path.exists(args.map):
        print(f"Map image not found: {args.map}")
        print("  → Place summoners_rift.png in the project root.")
        sys.exit(1)

    timeline    = load_timeline(args.timeline)
    match_id    = match_id_from_path(args.timeline)
    match_json  = match_json_path_from_timeline(args.timeline)
    part_map    = build_participant_map(match_json_path=match_json)
    if not part_map:
        print(f"Participant names unavailable — match JSON not found at {match_json}")
        print(f"  → Save match_{match_id}.json to cache/ for champion name lookup.")
        print(f"  → Use --participant 1-10 instead of --champion to continue without it.\n")

    # Resolve participant_id + champion_name
    if args.participant:
        participant_id = args.participant
        champion_name  = part_map.get(participant_id, f"Participant{participant_id}")
    elif args.champion:
        participant_id = next(
            (pid for pid, c in part_map.items() if c.lower() == args.champion.lower()), None
        )
        if not participant_id:
            print(f"'{args.champion}' not found. Available: {list(part_map.values())}")
            sys.exit(1)
        champion_name = args.champion
    else:
        print("Specify --champion <name> or --participant <1-10>")
        sys.exit(1)

    team = "ORDER" if participant_id <= 5 else "CHAOS"
    summoner = summoner_for_champion(match_json, champion_name)

    # Load positions (optional but needed for XP heatmap and lane analysis)
    positions, pos_path = _load_positions(champion_name, args.positions)
    if not positions:
        print(f"Note: no positions file found at {pos_path}")
        print("  XP heatmap and lane analysis will be skipped.")
        print("  Run  python main.py --player <champion>  to record a replay first.\n")

    out_dir = output_dir_for(match_id, champion_name)
    os.makedirs(out_dir, exist_ok=True)

    # ── Stats ──────────────────────────────────────────────────────────────────
    stats    = activity_stats(positions or [], timeline, participant_id, team)
    pm       = per_minute_breakdown(timeline, participant_id, positions or [], team)
    pm_15s   = per_15s_breakdown(timeline, participant_id, positions or [], team)
    ev_times = player_event_times(timeline, participant_id, positions or [], team)

    mins_str = f"{int(stats['duration_min'])}:{int(stats['duration_sec'] % 60):02d}"
    print(f"\n{'='*62}")
    print(f"  {champion_name}  (participant {participant_id}, {'Blue' if team == 'ORDER' else 'Red'} team)  —  {mins_str}")
    print(f"{'='*62}")
    print(f"  KDA          {stats['kills']}/{stats['deaths']}/{stats['assists']}  ({stats['kda']:.2f})")
    print(f"  CS           {stats['total_cs']}  ({stats['cs_per_min']}/min)")
    print(f"  Gold         {stats['gold_earned']:,}  ({int(stats['gold_per_min'])}/min)")
    print(f"  Towers       {stats['tower_participations']}")
    print(f"  Objectives   {stats['objective_participations']}")
    print(f"  Recalls      {stats['recalls']}  (at: {stats['recall_times_min']} min)")
    if stats["first_kill_min"] is not None:
        print(f"  First kill   {stats['first_kill_min']} min")
    if stats["first_death_min"] is not None:
        print(f"  First death  {stats['first_death_min']} min")
    print()

    # ── Activity chart ─────────────────────────────────────────────────────────
    activity_out = os.path.join(out_dir, "activity.png")
    render_activity_chart(stats, pm, champion_name, activity_out,
                          events_at_time=ev_times, per_15s=pm_15s)

    # ── XP heatmap ─────────────────────────────────────────────────────────────
    if positions:
        xp_locs  = xp_gain_locations(positions, timeline, participant_id)
        xp_out   = os.path.join(out_dir, "xp_heatmap.png")
        print(f"XP heatmap: {len(xp_locs)} data points")
        render_xp_heatmap(args.map, xp_locs, xp_out, downscale=args.downscale)

    # ── Team fight clusters ────────────────────────────────────────────────────
    fights = team_fight_clusters(timeline)
    tf_list = [f for f in fights if f["size"] >= 4]
    sk_list = [f for f in fights if f["size"] < 4]
    print(f"\nTeam fights ({len(tf_list)}) + Skirmishes ({len(sk_list)}) = {len(fights)} total")

    def _fight_row(i, fight):
        mins = int(fight["start_min"])
        secs = int((fight["start_min"] - mins) * 60)
        bd, rd = fight["blue_deaths"], fight["red_deaths"]
        # +N = kills scored by that team (= opponents who died)
        # bd/rd count deaths on each side, so each team's score is the other's death count
        blue_kills = rd  # blue killed this many red players
        red_kills  = bd  # red killed this many blue players
        if fight["winner"] == "blue":
            outcome = "BLUE  "
        elif fight["winner"] == "red":
            outcome = "RED   "
        else:
            outcome = "EVEN  "
        dur = fight["duration_sec"]
        print(f"  #{i:<2}  {mins}:{secs:02d}  x{fight['size']} kills  "
              f"Blue +{blue_kills}  Red +{red_kills}  ->  {outcome}  ({dur:.0f}s)")

    if tf_list:
        print("  -- Team Fights (4+ kills) --")
        for i, f in enumerate([x for x in fights if x["size"] >= 4], 1):
            _fight_row(i, f)
    if sk_list:
        print("  -- Skirmishes (2-3 kills) --")
        for i, f in enumerate([x for x in fights if x["size"] < 4], 1):
            _fight_row(i, f)

    fights_out = os.path.join(out_dir, "fights.png")
    render_teamfight_clusters(args.map, fights, fights_out, downscale=args.downscale)

    # ── Lane aggression ────────────────────────────────────────────────────────
    agg = None
    if positions:
        agg = lane_aggression(positions, team)
        if agg:
            print(f"\nLane: {agg['lane']}  |  "
                  f"Aggression: {agg['score']}/100  ({agg['description']})")
            lane_out = os.path.join(out_dir, "lane.png")
            render_lane_aggression(args.map, agg, lane_out, downscale=args.downscale)

    renders_produced = ["activity"]
    if positions:
        renders_produced.append("xp_heatmap")
    renders_produced.append("fights")
    if agg:
        renders_produced.append("lane")
    upsert_game(match_id, champion=champion_name, summoner=summoner,
                team_color="blue" if team == "ORDER" else "red",
                renders=renders_produced)

    print(f"\nOutputs in {out_dir}/")


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as e:
        fn = e.filename or ""
        print(f"\nFile not found: {fn}")
        if "timeline" in fn:
            print("  → Provide a timeline path: python analyze.py cache/timeline_<matchId>.json")
        elif "match_" in fn:
            print("  → Save the match JSON to cache/match_<matchId>.json for champion name lookup.")
        elif "summoners_rift" in fn:
            print("  → Place summoners_rift.png in the project root.")
        else:
            print("  → Check the path and try again.")
        sys.exit(1)
    except (ValueError, KeyError) as e:
        print(f"\nA JSON file could not be read: {e}")
        print("  → Timeline and match JSON must both be from Riot Match API v5 and the same match.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(0)
