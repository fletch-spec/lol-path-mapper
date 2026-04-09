"""
Match insight computations.

All functions are pure data transformations — no rendering, no file I/O.

Input types:
  positions  — list of (game_time_sec, x, y) tuples collected by replay_api.py
  timeline   — Riot Match API v5 timeline dict (loaded from timeline_*.json)
  participant_id — integer 1–10 (1–5 = blue/ORDER, 6–10 = red/CHAOS)
  team       — "ORDER" (blue) or "CHAOS" (red)
"""

import math

BLUE_BASE = (603, 611)
RED_BASE = (14103, 14195)
BASE_RADIUS = 1500  # units around spawn counted as "in base"


# ── helpers ───────────────────────────────────────────────────────────────────

def get_position_at_time(positions, target_sec):
    """Binary search for the position sample closest to target_sec."""
    if not positions:
        return None
    lo, hi = 0, len(positions) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if positions[mid][0] < target_sec:
            lo = mid + 1
        else:
            hi = mid
    return (positions[lo][1], positions[lo][2])


def _all_events(timeline):
    return [e for frame in timeline["info"]["frames"] for e in frame.get("events", [])]


def _participant_frame(timeline, participant_id, frame_index):
    return timeline["info"]["frames"][frame_index]["participantFrames"].get(str(participant_id), {})


# ── XP heatmap ────────────────────────────────────────────────────────────────

def xp_gain_locations(positions, timeline, participant_id):
    """Distribute each 60s frame's XP gain across all position samples in that window.

    The Riot timeline only snapshots XP once per minute, but position data is sampled
    at ~0.8s game-time resolution. By spreading each minute's XP equally across every
    position sample within that window we go from ~35 coarse blobs to thousands of
    weighted points, giving ~75x better spatial fidelity.

    Returns [(x, y, xp_per_sample)] — many small-weighted samples.
    """
    frames = timeline["info"]["frames"]
    result = []
    prev_xp = 0
    prev_ts_sec = 0.0

    for frame in frames:
        ts_sec = frame["timestamp"] / 1000.0
        pf = frame["participantFrames"].get(str(participant_id))
        if not pf:
            prev_ts_sec = ts_sec
            continue

        gain = pf["xp"] - prev_xp
        prev_xp = pf["xp"]

        if gain > 0:
            window = [(x, y) for t, x, y in positions if prev_ts_sec < t <= ts_sec]
            if window:
                per_sample = gain / len(window)
                for x, y in window:
                    result.append((x, y, per_sample))
            else:
                # No positions in window — fall back to single point at frame time
                pos = get_position_at_time(positions, ts_sec)
                if pos:
                    result.append((pos[0], pos[1], gain))

        prev_ts_sec = ts_sec

    return result


# ── activity stats ────────────────────────────────────────────────────────────

def detect_recalls(positions, team):
    """Detect recalls: large jumps (>3000 units) landing within BASE_RADIUS of spawn.
    Returns list of game times (seconds)."""
    base = BLUE_BASE if team == "ORDER" else RED_BASE
    recalls = []
    for i in range(1, len(positions)):
        pt, px, py = positions[i - 1]
        ct, cx, cy = positions[i]
        if math.hypot(cx - px, cy - py) > 3000:
            if math.hypot(cx - base[0], cy - base[1]) < BASE_RADIUS:
                recalls.append(ct)
    return recalls


def activity_stats(positions, timeline, participant_id, team):
    """Compute a stats summary dict for the selected player."""
    frames = timeline["info"]["frames"]
    events = _all_events(timeline)
    last_pf = _participant_frame(timeline, participant_id, -1)
    duration_sec = frames[-1]["timestamp"] / 1000.0

    total_cs = last_pf.get("minionsKilled", 0) + last_pf.get("jungleMinionsKilled", 0)

    kills   = [e for e in events if e["type"] == "CHAMPION_KILL" and e.get("killerId") == participant_id]
    deaths  = [e for e in events if e["type"] == "CHAMPION_KILL" and e.get("victimId") == participant_id]
    assists = [e for e in events if e["type"] == "CHAMPION_KILL"
               and participant_id in e.get("assistingParticipantIds", [])]

    tower_events = [e for e in events if e["type"] == "BUILDING_KILL"
                    and e.get("buildingType") == "TOWER_BUILDING"
                    and (e.get("killerId") == participant_id
                         or participant_id in e.get("assistingParticipantIds", []))]

    objective_events = [e for e in events if e["type"] == "ELITE_MONSTER_KILL"
                        and (e.get("killerId") == participant_id
                             or participant_id in e.get("assistingParticipantIds", []))]

    recalls = detect_recalls(positions, team) if positions else []
    mins = duration_sec / 60

    return {
        "duration_sec": duration_sec,
        "duration_min": mins,
        "total_cs": total_cs,
        "cs_per_min": round(total_cs / mins, 1) if mins else 0,
        "kills": len(kills),
        "deaths": len(deaths),
        "assists": len(assists),
        "kda": round((len(kills) + len(assists)) / max(len(deaths), 1), 2),
        "tower_participations": len(tower_events),
        "objective_participations": len(objective_events),
        "recalls": len(recalls),
        "recall_times_min": [round(t / 60, 1) for t in recalls],
        "gold_earned": last_pf.get("totalGold", 0),
        "gold_per_min": round(last_pf.get("totalGold", 0) / mins, 0) if mins else 0,
        "first_kill_min": round(kills[0]["timestamp"] / 60000, 1) if kills else None,
        "first_death_min": round(deaths[0]["timestamp"] / 60000, 1) if deaths else None,
    }


def per_minute_breakdown(timeline, participant_id, positions, team):
    """Return per-60s-frame activity data for charting.
    Each entry: {minute, activity, cs_gained, xp_gained, gold_gained}
    Activity: Fighting | Farming | Base | Roaming
    """
    frames = timeline["info"]["frames"]
    events = _all_events(timeline)
    base = BLUE_BASE if team == "ORDER" else RED_BASE

    rows = []
    prev_cs, prev_xp, prev_gold = 0, 0, 0

    for i, frame in enumerate(frames):
        pf = frame["participantFrames"].get(str(participant_id), {})
        cs    = pf.get("minionsKilled", 0) + pf.get("jungleMinionsKilled", 0)
        xp    = pf.get("xp", 0)
        gold  = pf.get("totalGold", 0)

        if i == 0:
            prev_cs, prev_xp, prev_gold = cs, xp, gold
            continue

        ts_ms      = frame["timestamp"]
        prev_ts_ms = frames[i - 1]["timestamp"]

        interval = [e for e in events if prev_ts_ms < e["timestamp"] <= ts_ms]

        fought = any(
            e["type"] == "CHAMPION_KILL"
            and (e.get("killerId") == participant_id
                 or e.get("victimId") == participant_id
                 or participant_id in e.get("assistingParticipantIds", []))
            for e in interval
        )

        pos = get_position_at_time(positions, ts_ms / 1000.0) if positions else None
        in_base = pos and math.hypot(pos[0] - base[0], pos[1] - base[1]) < BASE_RADIUS

        cs_gain = cs - prev_cs
        if fought:
            activity = "Fighting"
        elif in_base:
            activity = "Base"
        elif cs_gain > 0:
            activity = "Farming"
        else:
            activity = "Roaming"

        rows.append({
            "minute":     int(ts_ms / 60000),
            "activity":   activity,
            "cs_gained":  cs_gain,
            "xp_gained":  xp - prev_xp,
            "gold_gained": gold - prev_gold,
        })
        prev_cs, prev_xp, prev_gold = cs, xp, gold

    return rows


# ── lane aggression ───────────────────────────────────────────────────────────

def lane_aggression(positions, team):
    """Score lane aggression (0–100) during the first 15 minutes.

    0 = camped under own tower, 50 = neutral, 100 = always at enemy tower.
    Also detects the player's lane from their average early-game position.
    """
    laning = [(x, y) for t, x, y in positions if t <= 900]
    if len(laning) < 10:
        return None

    avg_x = sum(p[0] for p in laning) / len(laning)
    avg_y = sum(p[1] for p in laning) / len(laning)

    # Lane detection: TOP = high y, BOT = low y, MID = middle
    if avg_y > 9500:
        lane = "TOP"
    elif avg_y < 4500:
        lane = "BOT"
    else:
        lane = "MID"

    own_base   = BLUE_BASE if team == "ORDER" else RED_BASE
    enemy_base = RED_BASE  if team == "ORDER" else BLUE_BASE

    own_dist   = math.hypot(avg_x - own_base[0],   avg_y - own_base[1])
    enemy_dist = math.hypot(avg_x - enemy_base[0],  avg_y - enemy_base[1])
    total      = own_dist + enemy_dist
    # Score = fraction of the base-to-base distance that the player was away from their own base.
    # 0 = at own base, 50 = equidistant (river), 100 = at enemy base.
    score      = int(own_dist / total * 100) if total > 0 else 50

    return {
        "lane": lane,
        "score": score,
        "description": "Aggressive" if score >= 58 else "Defensive" if score <= 42 else "Neutral",
        "avg_pos": (avg_x, avg_y),
        "laning_positions": laning,
    }


def player_event_times(timeline, participant_id, positions, team):
    """Exact timestamps (minutes) for each key event type for the given player.

    Returns a dict of lists used by the activity chart to plot events on the timeline.
    """
    events = _all_events(timeline)
    recall_secs = detect_recalls(positions, team) if positions else []
    return {
        "kills":      [e["timestamp"] / 60000 for e in events
                       if e["type"] == "CHAMPION_KILL" and e.get("killerId") == participant_id],
        "deaths":     [e["timestamp"] / 60000 for e in events
                       if e["type"] == "CHAMPION_KILL" and e.get("victimId") == participant_id],
        "assists":    [e["timestamp"] / 60000 for e in events
                       if e["type"] == "CHAMPION_KILL"
                       and participant_id in e.get("assistingParticipantIds", [])],
        "towers":     [e["timestamp"] / 60000 for e in events
                       if e["type"] == "BUILDING_KILL"
                       and e.get("buildingType") == "TOWER_BUILDING"
                       and (e.get("killerId") == participant_id
                            or participant_id in e.get("assistingParticipantIds", []))],
        "objectives": [e["timestamp"] / 60000 for e in events
                       if e["type"] == "ELITE_MONSTER_KILL"
                       and (e.get("killerId") == participant_id
                            or participant_id in e.get("assistingParticipantIds", []))],
        "recalls":    [t / 60 for t in recall_secs],
    }


def per_15s_breakdown(timeline, participant_id, positions, team):
    """15-second resolution activity classification.

    Improves on the 60s-frame limit by using exact event timestamps for Fighting
    and position data for Base detection. Farming/Roaming falls back to whether
    the enclosing 60s frame gained CS (best available granularity for that stat).

    Returns [{time_min, activity}] — 4× more buckets than per_minute_breakdown.
    """
    frames = timeline["info"]["frames"]
    events = _all_events(timeline)
    base   = BLUE_BASE if team == "ORDER" else RED_BASE

    if not frames:
        return []

    # CS data is only available at 60s frame boundaries, so we pre-mark which
    # whole minutes saw any CS gain. All four 15s buckets within that minute
    # inherit the "Farming" label unless a fight or base event overrides them.
    farming_minutes = set()
    prev_cs = 0
    for frame in frames[1:]:
        pf = frame["participantFrames"].get(str(participant_id), {})
        cs = pf.get("minionsKilled", 0) + pf.get("jungleMinionsKilled", 0)
        if cs > prev_cs:
            farming_minutes.add(int(frame["timestamp"] / 60000))  # ms → whole-minute bucket
        prev_cs = cs

    duration_sec = frames[-1]["timestamp"] / 1000.0
    WINDOW = 15  # seconds per bucket
    result = []
    t = 0.0

    while t < duration_sec:
        t_end   = t + WINDOW
        t_ms    = t * 1000
        t_end_ms = t_end * 1000

        fought = any(
            e["type"] == "CHAMPION_KILL"
            and t_ms < e["timestamp"] <= t_end_ms
            and (e.get("killerId") == participant_id
                 or e.get("victimId") == participant_id
                 or participant_id in e.get("assistingParticipantIds", []))
            for e in events
        )

        pos = get_position_at_time(positions, (t + t_end) / 2) if positions else None
        in_base = pos and math.hypot(pos[0] - base[0], pos[1] - base[1]) < BASE_RADIUS
        farming  = int(t / 60) in farming_minutes

        if fought:
            activity = "Fighting"
        elif in_base:
            activity = "Base"
        elif farming:
            activity = "Farming"
        else:
            activity = "Roaming"

        result.append({"time_min": t / 60, "activity": activity})
        t += WINDOW

    return result


# ── team fight clusters ───────────────────────────────────────────────────────

def team_fight_clusters(timeline, time_window_sec=45, distance=3000, min_kills=2):
    """Group champion kill events into skirmishes/team fights.

    Two kills belong to the same fight if they occur within time_window_sec AND
    the new kill is within `distance` units of the current cluster centroid.

    Returns list of cluster dicts sorted by start time.
    """
    kills = []
    for frame in timeline["info"]["frames"]:
        for e in frame.get("events", []):
            if e["type"] == "CHAMPION_KILL" and "position" in e:
                kills.append({
                    "time":   e["timestamp"] / 1000.0,
                    "x":      e["position"]["x"],
                    "y":      e["position"]["y"],
                    "killer": e.get("killerId", 0),
                    "victim": e.get("victimId", 0),
                })
    kills.sort(key=lambda k: k["time"])

    used = [False] * len(kills)
    clusters = []

    for i in range(len(kills)):
        if used[i]:
            continue
        # Start a new candidate cluster from this kill
        group = [i]
        used[i] = True

        for j in range(i + 1, len(kills)):
            if used[j]:
                continue
            # Kills are sorted by time, so once the gap exceeds the window
            # no later kill can ever join this cluster — early exit is safe
            if kills[j]["time"] - kills[group[0]]["time"] > time_window_sec:
                break
            # Recompute the running centroid and check spatial proximity
            cx = sum(kills[k]["x"] for k in group) / len(group)
            cy = sum(kills[k]["y"] for k in group) / len(group)
            if math.hypot(kills[j]["x"] - cx, kills[j]["y"] - cy) <= distance:
                group.append(j)
                used[j] = True

        if len(group) < min_kills:
            continue

        members    = [kills[k] for k in group]
        cx         = sum(m["x"] for m in members) / len(members)
        cy         = sum(m["y"] for m in members) / len(members)
        # Victims with IDs 1-5 are blue-team players; 6-10 are red-team
        blue_dead  = sum(1 for m in members if 1 <= m["victim"] <= 5)
        red_dead   = sum(1 for m in members if 6 <= m["victim"] <= 10)

        clusters.append({
            "members":    members,
            "centroid":   (cx, cy),
            "size":       len(group),
            "blue_deaths": blue_dead,
            "red_deaths":  red_dead,
            # The team with fewer deaths won the exchange
            "winner":     "blue" if red_dead > blue_dead else "red" if blue_dead > red_dead else "even",
            "start_min":  round(members[0]["time"] / 60, 1),
            "duration_sec": members[-1]["time"] - members[0]["time"],
        })

    return sorted(clusters, key=lambda c: c["members"][0]["time"])
