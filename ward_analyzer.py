import glob
import json
import os

CACHE_DIR = os.path.join(os.path.dirname(__file__), ".dev", "cache")


def load_timeline(path):
    with open(path) as f:
        return json.load(f)


def extract_ward_events(timeline):
    """Extract ward placements from the timeline.

    Uses the exact position on the WARD_PLACED event when available (Riot Match
    API v5 includes position, ward_type, and creator). Falls back to the creator's
    participantFrame position for older timeline data that lacks the position field.

    Returns a list of dicts: {timestamp, creator_id, ward_type, x, y}
    """
    frames = timeline["info"]["frames"]
    events = []

    for frame in frames:
        pf = frame.get("participantFrames", {})
        frame_positions = {
            int(pid): (data["position"]["x"], data["position"]["y"])
            for pid, data in pf.items()
        }

        for event in frame.get("events", []):
            if event["type"] != "WARD_PLACED":
                continue
            creator_id = event.get("creatorId", 0)
            if creator_id == 0:
                continue

            pos = event.get("position")
            if pos:
                x, y = pos["x"], pos["y"]
            else:
                # Fallback: use the creator's frame snapshot position
                frame_pos = frame_positions.get(creator_id)
                if frame_pos is None:
                    continue
                x, y = frame_pos

            events.append({
                "timestamp": event["timestamp"],
                "creator_id": creator_id,
                "ward_type": event.get("wardType", "UNKNOWN"),
                "x": x,
                "y": y,
            })

    return events


def save_ward_events(events, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(events, f)


def load_ward_events(path):
    with open(path) as f:
        return json.load(f)


def latest_timeline_file():
    files = glob.glob(os.path.join(CACHE_DIR, "timeline_*.json"))
    if not files:
        return None
    return max(files, key=os.path.getmtime)


def match_id_from_path(path):
    name = os.path.splitext(os.path.basename(path))[0]
    return name.replace("timeline_", "")


def match_json_path_from_timeline(timeline_path):
    """Derive the expected match JSON path from a timeline path."""
    match_id = match_id_from_path(timeline_path)
    return os.path.join(CACHE_DIR, f"match_{match_id}.json")


def build_participant_map(match_json_path=None, players=None):
    """Build a {participant_id (int): champion_name (str)} mapping.

    Tries the match JSON first (exact mapping from Riot match data).
    Falls back to the live player list order: ORDER team = 1-5, CHAOS = 6-10.
    """
    if match_json_path and os.path.exists(match_json_path):
        with open(match_json_path) as f:
            match = json.load(f)
        participants = match.get("info", {}).get("participants", [])
        if participants:
            return {p["participantId"]: p["championName"] for p in participants}

    if players:
        mapping = {}
        blue = [p for p in players if p.get("team") == "ORDER"]
        red = [p for p in players if p.get("team") == "CHAOS"]
        for i, p in enumerate(blue, start=1):
            mapping[i] = p["championName"]
        for i, p in enumerate(red, start=6):
            mapping[i] = p["championName"]
        return mapping

    return {}
