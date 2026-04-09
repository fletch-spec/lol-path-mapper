print("[LOADING]: Util modules...", end="")

import json
import struct
import os

def parse_rofl_metadata(path):
    """Parse the metadata JSON embedded in a .rofl replay file.

    Reads only the fixed header + metadata JSON (a few KB), not the game payload.

    .rofl binary layout:
    0x000  4 B   magic "RIOT"
    0x004  256 B  RSA signature
    0x104  2 B   uint16  headerLength
    0x106  4 B   uint32  fileLength
    0x10A  4 B   uint32  metadataOffset
    0x10E  4 B   uint32  metadataLength
    0x112  4 B   uint32  payloadHeaderOffset
    0x116  4 B   uint32  payloadHeaderLength
    0x11A  4 B   uint32  payloadOffset

    Returns a dict with:
    game_id      — int (numeric match ID)
    duration     — "mm:ss" string, or None
    patch        — "major.minor" string, or None
    participants — list of {summoner, team, champion_id, win}
    blue_wins    — True / False / None
    Returns None if the file cannot be parsed.
    """
    try:
        with open(path, "rb") as f:
            if f.read(4) != b"RIOT":
                return None
            f.seek(260)  # skip 256-byte signature
            _header_len     = struct.unpack("<H", f.read(2))[0]
            _file_len       = struct.unpack("<I", f.read(4))[0]
            metadata_offset = struct.unpack("<I", f.read(4))[0]
            metadata_length = struct.unpack("<I", f.read(4))[0]
            if metadata_length == 0 or metadata_length > 2_000_000:
                return None
            f.seek(metadata_offset)
            raw = f.read(metadata_length)
        meta = json.loads(raw.decode("utf-8", errors="replace"))
    except (OSError, struct.error, json.JSONDecodeError, ValueError):
        return None

    result = {"game_id": meta.get("gameId")}

    # Duration — rofl gameLength is in ms for modern clients
    gl = meta.get("gameLength", 0)
    secs = gl / 1000 if gl > 10_000 else gl   # >10 000 → ms, else already seconds
    if 60 < secs < 10_800:                     # sanity: 1 min – 3 hrs
        result["duration"] = f"{int(secs) // 60}:{int(secs) % 60:02d}"
    else:
        result["duration"] = None

    # Patch from gameVersion "14.6.634.xxx"
    version = meta.get("gameVersion", "")
    parts   = version.split(".")
    result["patch"] = f"{parts[0]}.{parts[1]}" if len(parts) >= 2 else None

    # Per-participant win/loss from statsJson (a JSON-string-inside-JSON)
    stats_list = []
    stats_raw  = meta.get("statsJson")
    if isinstance(stats_raw, str):
        try:
            stats_list = json.loads(stats_raw)
        except (json.JSONDecodeError, ValueError):
            pass

    participants = []
    for i, p in enumerate(meta.get("participants", [])):
        team_id = p.get("teamId", 0)
        win     = stats_list[i].get("WIN") == "Win" if i < len(stats_list) else None
        participants.append({
            "summoner":    p.get("riotIdGameName") or p.get("summonerName", ""),
            "team":        "blue" if team_id == 100 else "red",
            "champion_id": p.get("championId"),
            "win":         win,
        })
    result["participants"] = participants

    blue_wins = None
    for p in participants:
        if p["win"] is not None:
            blue_wins = (p["team"] == "blue") == p["win"]
            break
    result["blue_wins"] = blue_wins

    return result

def get_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.cfg")
    config = {}
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, sep, value = line.partition("=")
                    if sep:
                        config[key.strip()] = value.strip()
    return config

# def get_api_key():
#     """Read the Riot API key from the cache directory."""
#     api_key_path = os.path.join(CACHE_DIR, "api_key.txt")
#     if os.path.exists(api_key_path):
#         with open(api_key_path, "r", encoding="utf-8") as f:
#             return f.read().strip()
#     return None

print('good')