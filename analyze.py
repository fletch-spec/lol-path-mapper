"""Match insight generator.

Outputs for the selected player:
  <match_id>_<champion>_xp_heatmap.png  — where XP was earned on the map
  <match_id>_<champion>_fights.png      — team fight clusters (all 10 players)
  <match_id>_<champion>_activity.png    — CS / gold / activity timeline chart
  <match_id>_<champion>_lane.png        — laning-phase positions + aggression score

Requires:
  - Riot Match API v5 timeline JSON  (.dev/cache/timeline_*.json)
  - Riot Match API v5 match JSON     (.dev/cache/match_*.json)  — for participant mapping
  - Cached position data             (.dev/cache/positions_<champion>.json)  — for XP heatmap / lane analysis

Usage:
    python analyze.py .dev/cache/timeline_OC1_697009636.json --champion Ahri
    python analyze.py .dev/cache/timeline_OC1_697009636.json --participant 5
    python analyze.py .dev/cache/timeline_OC1_697009636.json --champion Ahri --downscale 2
"""

import json
import os
import sys
import argparse

from ward_analyzer import (
    build_participant_map,
    load_timeline,
    match_id_from_path,
    match_json_path_from_timeline,
    CACHE_DIR,
)
from insights import (
    activity_stats,
    lane_aggression,
    per_minute_breakdown,
    per_15s_breakdown,
    player_event_times,
    team_fight_clusters,
    xp_gain_locations,
)
from insights_renderer import (
    render_activity_chart,
    render_lane_aggression,
    render_teamfight_clusters,
    render_xp_heatmap,
)

DEFAULT_MAP = os.path.join(os.path.dirname(__file__), ".dev", "summoners_rift.png")
OUTPUT_DIR  = os.path.join(os.path.dirname(__file__), "outputs")


def _load_positions(champion_name, override_path=None):
    path = override_path or os.path.join(CACHE_DIR, f"positions_{champion_name}.json")
    if not os.path.exists(path):
        return None, path
    with open(path) as f:
        return json.load(f), path


def main():
    parser = argparse.ArgumentParser(description="Generate match insights for a player")
    parser.add_argument("timeline", nargs="?", help="Riot timeline JSON (default: most recent in .dev/cache/)")
    parser.add_argument("--champion",    default=None, help="Champion name")
    parser.add_argument("--participant", type=int, default=None, help="Participant ID 1-10")
    parser.add_argument("--positions",   default=None, help="Positions JSON path (overrides auto-detect)")
    parser.add_argument("--map",         default=DEFAULT_MAP)
    parser.add_argument("--downscale",   type=int, default=4)
    args = parser.parse_args()

    # Resolve timeline
    if not args.timeline:
        from ward_analyzer import latest_timeline_file
        args.timeline = latest_timeline_file()
    if not args.timeline or not os.path.exists(args.timeline):
        print("No timeline file found. Provide a path or place timeline_*.json in .dev/cache/")
        sys.exit(1)

    if not os.path.exists(args.map):
        print(f"Error: map image not found at {args.map}")
        sys.exit(1)

    timeline    = load_timeline(args.timeline)
    match_id    = match_id_from_path(args.timeline)
    match_json  = match_json_path_from_timeline(args.timeline)
    part_map    = build_participant_map(match_json_path=match_json)

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

    # Load positions (optional but needed for XP heatmap and lane analysis)
    positions, pos_path = _load_positions(champion_name, args.positions)
    if not positions:
        print(f"Note: no positions file found at {pos_path}")
        print("  XP heatmap and lane analysis will be skipped.")
        print("  Run  python main.py --player <champion>  to record a replay first.\n")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    prefix = os.path.join(OUTPUT_DIR, f"{match_id}_{champion_name}")

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
    activity_out = f"{prefix}_activity.png"
    render_activity_chart(stats, pm, champion_name, activity_out,
                          events_at_time=ev_times, per_15s=pm_15s)

    # ── XP heatmap ─────────────────────────────────────────────────────────────
    if positions:
        xp_locs  = xp_gain_locations(positions, timeline, participant_id)
        xp_out   = f"{prefix}_xp_heatmap.png"
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

    fights_out = f"{prefix}_fights.png"
    render_teamfight_clusters(args.map, fights, fights_out, downscale=args.downscale)

    # ── Lane aggression ────────────────────────────────────────────────────────
    if positions:
        agg = lane_aggression(positions, team)
        if agg:
            print(f"\nLane: {agg['lane']}  |  "
                  f"Aggression: {agg['score']}/100  ({agg['description']})")
            lane_out = f"{prefix}_lane.png"
            render_lane_aggression(args.map, agg, lane_out, downscale=args.downscale)

    print(f"\nOutputs in {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
