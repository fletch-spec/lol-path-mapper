"""
Cache management and CLI for League of Legends replay analysis.

Maintains cache/games.json as a human-readable index of all cached matches.
Each entry tracks what data is available and which renders have been produced.

Usage:
    python cache.py              # list all cached games (brief)
    python cache.py <match_id>   # detailed view with player roster and commands
"""

import json
import os
import re
import struct
import sys
from datetime import datetime, timezone

# Ensure Unicode output works on Windows terminals
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

_ROOT        = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR    = os.path.join(_ROOT, "cache")
OUTPUT_DIR   = os.path.join(_ROOT, "outputs")
GAMES_JSON   = os.path.join(CACHE_DIR, "games.json")
API_KEY_FILE = os.path.join(CACHE_DIR, "api_key.txt")

_INVALID_CHARS = re.compile(r'[<>:"/\\|?*]')

# Directories scanned for .rofl replay files (in priority order)
REPLAYS_DIR = os.path.join(_ROOT, "replays")
_REPLAY_DIRS = [
    REPLAYS_DIR,                                  # primary user location
    os.path.join(_ROOT, ".dev", "old_matches"),   # legacy fallback
    os.path.join(_ROOT, ".dev"),                  # legacy fallback (loose files)
]

# Riot API regional routing by platform prefix
_PLATFORM_ROUTING = {
    "BR1":  "americas",
    "EUN1": "europe",
    "EUW1": "europe",
    "JP1":  "asia",
    "KR":   "asia",
    "LA1":  "americas",
    "LA2":  "americas",
    "ME1":  "europe",
    "NA1":  "americas",
    "OC1":  "sea",
    "PH2":  "sea",
    "RU":   "europe",
    "SG2":  "sea",
    "TH2":  "sea",
    "TR1":  "europe",
    "TW2":  "sea",
    "VN2":  "sea",
}

_QUEUE_NAMES = {
    0:    "Custom",
    400:  "Normal Draft",
    420:  "Ranked Solo",
    430:  "Normal Blind",
    440:  "Ranked Flex",
    450:  "ARAM",
    900:  "URF",
    1020: "One for All",
}


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


def sanitize_filename(s):
    """Remove invalid filename chars and replace spaces with underscores."""
    return _INVALID_CHARS.sub("", str(s)).replace(" ", "_").strip()


def output_dir_for(match_id, champion=None):
    """Return the output directory for a match/champion combination.

    outputs/{match_id}/{Champion}/  — champion-specific renders
    outputs/{match_id}/             — team-level renders (no champion)
    outputs/unknown/                — no match_id known
    """
    if match_id:
        base = os.path.join(OUTPUT_DIR, sanitize_filename(match_id))
    else:
        base = os.path.join(OUTPUT_DIR, "unknown")
    if champion:
        return os.path.join(base, sanitize_filename(champion))
    return base


def _rofl_to_match_id(filename):
    """Convert a replay filename to a Riot match ID.
    OC1-697009636.rofl  →  OC1_697009636
    """
    return os.path.splitext(filename)[0].replace("-", "_")


def _match_id_to_rofl_stem(match_id):
    """Convert a Riot match ID to a replay filename stem.
    OC1_697009636  →  OC1-697009636
    """
    return match_id.replace("_", "-")


def find_rofl_files():
    """Scan replay directories for .rofl files.

    Returns a dict of {match_id: absolute_path}, scanning _REPLAY_DIRS in
    order — the first directory wins if the same match appears in multiple places.
    """
    result = {}
    for d in _REPLAY_DIRS:
        if not os.path.isdir(d):
            continue
        for fname in os.listdir(d):
            if fname.lower().endswith(".rofl"):
                mid = _rofl_to_match_id(fname)
                if mid not in result:
                    result[mid] = os.path.join(d, fname)
    return result


def _cache_status(match_id):
    """Return a dict of which cache files exist for a match_id."""
    return {
        "timeline":   os.path.exists(os.path.join(CACHE_DIR, f"timeline_{match_id}.json")),
        "match_json": os.path.exists(os.path.join(CACHE_DIR, f"match_{match_id}.json")),
        "wards":      os.path.exists(os.path.join(CACHE_DIR, f"wards_{match_id}.json")),
    }


# -- Internal helpers -----------------------------------------------------------

def _load_games():
    if not os.path.exists(GAMES_JSON):
        return []
    with open(GAMES_JSON, encoding="utf-8") as f:
        return json.load(f)


def _save_games(entries):
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(GAMES_JSON, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)


def _refresh_cache_flags(entry):
    match_id = entry.get("match_id")
    champion = entry.get("champion")
    entry["cache"] = {
        "positions":  bool(champion and os.path.exists(
                          os.path.join(CACHE_DIR, f"positions_{champion}.json"))),
        "timeline":   bool(match_id and os.path.exists(
                          os.path.join(CACHE_DIR, f"timeline_{match_id}.json"))),
        "match_json": bool(match_id and os.path.exists(
                          os.path.join(CACHE_DIR, f"match_{match_id}.json"))),
        "wards":      bool(match_id and os.path.exists(
                          os.path.join(CACHE_DIR, f"wards_{match_id}.json"))),
    }


def _enrich_from_match_json(entry, match_id):
    """Populate game metadata and all_players from match_{match_id}.json if available."""
    path = os.path.join(CACHE_DIR, f"match_{match_id}.json")
    try:
        with open(path, encoding="utf-8") as f:
            match = json.load(f)
        info = match.get("info", {})

        if entry.get("game_date") is None:
            creation = info.get("gameCreation")
            if creation:
                entry["game_date"] = datetime.fromtimestamp(
                    creation / 1000, tz=timezone.utc).isoformat()

        if entry.get("duration") is None:
            secs = info.get("gameDuration")
            if secs is not None:
                entry["duration"] = f"{int(secs) // 60}:{int(secs) % 60:02d}"

        if entry.get("queue") is None:
            qid = info.get("queueId")
            if qid is not None:
                entry["queue"] = _QUEUE_NAMES.get(qid, f"Queue {qid}")

        if entry.get("patch") is None:
            version = info.get("gameVersion", "")
            parts = version.split(".")
            if len(parts) >= 2:
                entry["patch"] = f"{parts[0]}.{parts[1]}"

        if entry.get("platform") is None:
            entry["platform"] = info.get("platformId")

        participants = info.get("participants", [])
        if participants:
            # Always overwrite — match JSON has champion names; rofl-only data does not
            entry["all_players"] = [
                {
                    "participant_id": p.get("participantId"),
                    "champion":  p.get("championName", ""),
                    "summoner":  p.get("riotIdGameName") or p.get("summonerName", ""),
                    "team":      "blue" if p.get("participantId", 0) <= 5 else "red",
                }
                for p in participants
            ]

        if entry.get("blue_wins") is None:
            for p in participants:
                if "win" in p:
                    entry["blue_wins"] = (p.get("teamId") == 100) == bool(p["win"])
                    break

    except (FileNotFoundError, KeyError, ValueError, TypeError):
        pass


# -- Riot API fetch -------------------------------------------------------------

def _load_api_key():
    """Return the Riot API key from cache/api_key.txt or $RIOT_API_KEY, or None."""
    key = os.environ.get("RIOT_API_KEY", "").strip()
    if key:
        return key
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, encoding="utf-8") as f:
            return f.read().strip()
    return None


def _fetch_riot_data(match_id, api_key):
    """Fetch and save match JSON and timeline JSON for one match.

    Skips files that already exist in cache/.
    Returns a list of result strings like ["match: saved", "timeline: already cached"].
    Raises requests.HTTPError on HTTP errors (403, 404, 429, etc.).
    """
    import requests as _req

    platform = match_id.split("_")[0].upper() if "_" in match_id else "NA1"
    region   = _PLATFORM_ROUTING.get(platform, "americas")
    base_url = f"https://{region}.api.riotgames.com"
    headers  = {"X-Riot-Token": api_key}

    results = []
    for label, suffix, fname in [
        ("match",    "",          f"match_{match_id}.json"),
        ("timeline", "/timeline", f"timeline_{match_id}.json"),
    ]:
        out_path = os.path.join(CACHE_DIR, fname)
        if os.path.exists(out_path):
            results.append(f"{label}: already cached")
            continue

        url  = f"{base_url}/lol/match/v5/matches/{match_id}{suffix}"
        resp = _req.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(resp.content)
        results.append(f"{label}: saved")
    return results


def load_replays():
    """Fetch Riot API data (match JSON + timeline) for every replay not yet cached.

    Reads the API key from cache/api_key.txt or $RIOT_API_KEY.
    After fetching, re-enriches games.json entries with champion names and metadata.
    """
    import time
    import requests as _req

    api_key = _load_api_key()
    if not api_key:
        print("No Riot API key found.")
        print()
        print("  Get a free key at:  https://developer.riotgames.com")
        print("  (Log in → scroll to bottom → click 'Generate API Key')")
        print("  Development keys work fine — they refresh every 24 hours.")
        print()
        try:
            raw = input("  Paste your key here (RGAPI-...): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled.")
            return
        if not raw.startswith("RGAPI-"):
            print("  That doesn't look like a Riot API key (should start with RGAPI-).")
            return
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(API_KEY_FILE, "w", encoding="utf-8") as f:
            f.write(raw)
        print(f"  Key saved to {API_KEY_FILE}\n")
        api_key = raw

    rofl_files = find_rofl_files()
    if not rofl_files:
        print("No replay files found in replays/.")
        return

    # Build list of match IDs that are missing at least one API file
    targets = [
        mid for mid in sorted(rofl_files)
        if not os.path.exists(os.path.join(CACHE_DIR, f"match_{mid}.json"))
        or not os.path.exists(os.path.join(CACHE_DIR, f"timeline_{mid}.json"))
    ]

    if not targets:
        print("All replays already have Riot API data cached.")
        return

    n = len(targets)
    print(f"Fetching Riot API data for {n} match{'es' if n != 1 else ''}...\n")
    print("  (Development keys: ~100 requests/2 min — rate-limited automatically)\n")

    failed    = []
    successes = 0
    for i, mid in enumerate(targets):
        print(f"  [{i + 1}/{n}]  {mid} ...", end=" ", flush=True)
        try:
            results = _fetch_riot_data(mid, api_key)
            print("  ".join(results))
            successes += 1
        except _req.HTTPError as e:
            code = e.response.status_code if e.response is not None else 0
            if code == 403:
                if successes > 0:
                    # Key is working — this match is likely private, old, or wrong region
                    print("403 — match may be private, from a different region, or no longer in the API. Skipping.")
                    failed.append(mid)
                else:
                    # No successes yet — key itself is probably the problem
                    print("403 Forbidden — key is invalid or expired.")
                    print()
                    print("  Development keys expire every 24 hours.")
                    print("  Get a new one at:  https://developer.riotgames.com")
                    print("  (Log in \u2192 scroll to bottom \u2192 Generate API Key)")
                    print()
                    try:
                        raw = input("  Paste new key to retry, or press Enter to stop: ").strip()
                    except (EOFError, KeyboardInterrupt):
                        raw = ""
                    if raw.startswith("RGAPI-"):
                        with open(API_KEY_FILE, "w", encoding="utf-8") as kf:
                            kf.write(raw)
                        api_key = raw
                        print("  Key updated. Retrying...\n")
                        try:
                            results = _fetch_riot_data(mid, api_key)
                            print(f"  [{i + 1}/{n}]  {mid} ... {'  '.join(results)}")
                            successes += 1
                        except Exception as e2:
                            print(f"  Still failed: {e2}")
                            failed.append(mid)
                    else:
                        # No key pasted — skip this match and keep going
                        failed.append(mid)
            elif code == 404:
                print("404 — match not found in Riot's API.")
                failed.append(mid)
            elif code == 429:
                print("429 Rate limited — waiting 120s...")
                time.sleep(120)
                try:
                    results = _fetch_riot_data(mid, api_key)
                    print(f"  Retry OK:  {'  '.join(results)}")
                except Exception as e2:
                    print(f"  Retry failed: {e2}")
                    failed.append(mid)
            else:
                print(f"HTTP {code}: {e}")
                failed.append(mid)
        except Exception as e:
            print(f"error: {e}")
            failed.append(mid)

        if i < len(targets) - 1:
            time.sleep(1.2)   # stay within development key rate limits

    # Ensure all fetched matches are in games.json and re-enrich
    entries    = _load_games()
    known_ids  = {e.get("match_id") for e in entries if e.get("match_id")}
    for mid in rofl_files:
        if mid not in known_ids:
            rofl_meta = parse_rofl_metadata(rofl_files[mid])
            all_players_rofl = []
            if rofl_meta and rofl_meta.get("participants"):
                for j, p in enumerate(rofl_meta["participants"]):
                    all_players_rofl.append({
                        "participant_id": j + 1,
                        "champion":       None,
                        "champion_id":    p.get("champion_id"),
                        "summoner":       p.get("summoner", ""),
                        "team":           p["team"],
                    })
            entry = {
                "match_id":    mid,
                "champion":    None,
                "summoner":    None,
                "team_color":  "",
                "recorded_at": datetime.now(tz=timezone.utc).isoformat(),
                "game_date":   None,
                "duration":    rofl_meta.get("duration") if rofl_meta else None,
                "queue":       None,
                "patch":       rofl_meta.get("patch") if rofl_meta else None,
                "platform":    mid.split("_")[0] if "_" in mid else None,
                "blue_wins":   rofl_meta.get("blue_wins") if rofl_meta else None,
                "cache":       {},
                "renders":     [],
                "all_players": all_players_rofl,
            }
            entries.append(entry)
            known_ids.add(mid)

    for entry in entries:
        mid = entry.get("match_id")
        if mid:
            _refresh_cache_flags(entry)
            _enrich_from_match_json(entry, mid)

    entries.sort(key=lambda e: e.get("recorded_at") or "", reverse=True)
    _save_games(entries)

    if failed:
        print(f"\nFailed ({len(failed)}): {', '.join(failed)}")
        print(f"Run  python cache.py  to see what was fetched.")
    else:
        print(f"\nDone. Run  python cache.py  to see the updated game list.\n")


# -- Public API -----------------------------------------------------------------

def upsert_game(match_id, champion, summoner="", team_color="", renders=None):
    """Create or update a game entry in games.json.

    match_id   — Riot match ID string, e.g. "OC1_697009636". None for unknown.
    champion   — Champion name (PascalCase). None for team-level ward entries.
    summoner   — Summoner/Riot ID game name.
    team_color — "blue", "red", "both", or "" if unknown.
    renders    — List of render type strings produced this run (e.g. ["path", "wards"]).
    """
    entries = _load_games()

    # Find or create the entry for this (match_id, champion) pair
    entry = next(
        (e for e in entries
         if e.get("match_id") == match_id and e.get("champion") == champion),
        None,
    )
    if entry is None:
        entry = {
            "match_id":   match_id,
            "champion":   champion,
            "summoner":   "",
            "team_color": "",
            "recorded_at": None,
            "game_date":  None,
            "duration":   None,
            "queue":      None,
            "patch":      None,
            "platform":   None,
            "blue_wins":  None,
            "cache":      {},
            "renders":    [],
            "all_players": [],
        }
        entries.append(entry)

    entry["recorded_at"] = datetime.now(tz=timezone.utc).isoformat()
    if summoner:
        entry["summoner"] = summoner
    if team_color:
        entry["team_color"] = team_color

    # Merge renders (deduplicate, preserve first-seen order)
    seen = set(entry["renders"])
    for r in (renders or []):
        if r not in seen:
            entry["renders"].append(r)
            seen.add(r)

    _refresh_cache_flags(entry)

    if match_id:
        _enrich_from_match_json(entry, match_id)

    # Sort most-recent first
    entries.sort(key=lambda e: e.get("recorded_at") or "", reverse=True)
    _save_games(entries)


# -- CLI display ----------------------------------------------------------------

def _divider(char="\u2550", width=70):
    return char * width


def _format_date(iso):
    if not iso:
        return ""
    try:
        return iso[:10]  # "YYYY-MM-DD"
    except Exception:
        return iso


def _recorded_champions(entries_for_match):
    """Return set of champion names that have a positions file."""
    return {e["champion"] for e in entries_for_match
            if e.get("cache", {}).get("positions")}


def _print_list(entries):
    """Brief listing of all cached games, followed by unprocessed replays."""
    recorded_ids = {e.get("match_id") for e in entries if e.get("match_id")}
    rofl_files   = find_rofl_files()

    if not entries and not rofl_files:
        print("\nNo replay files found.")
        print(f"  \u2192 Place .rofl replay files in:  replays/")
        print()
        print("Quick start")
        print("  1. Add .rofl files to replays/")
        print("  2. python cache.py               \u2014 see what's available")
        print("  3. Open a replay in the LoL client")
        print("  4. python main.py --player <name> \u2014 records positions, path, and wards")
        print("  5. python analyze.py  /  python wards.py  \u2014 generate charts")
        print(f"  \u2192 Check outputs/ for results\n")
        return

    # ── Cached games ──────────────────────────────────────────────────────────
    if entries:
        seen_matches = []
        match_groups = {}
        for e in entries:
            mid = e.get("match_id") or "unknown"
            if mid not in match_groups:
                seen_matches.append(mid)
                match_groups[mid] = []
            match_groups[mid].append(e)

        print(f"\nCached Games  ({GAMES_JSON})")
        for mid in seen_matches:
            group = match_groups[mid]
            g0 = group[0]
            date  = _format_date(g0.get("game_date") or g0.get("recorded_at"))
            dur   = g0.get("duration") or ""
            q     = g0.get("queue") or ""
            patch = f"Patch {g0['patch']}" if g0.get("patch") else ""
            win   = ("Blue wins" if g0.get("blue_wins") else "Red wins") if g0.get("blue_wins") is not None else ""
            meta  = "  |  ".join(x for x in [date, dur, q, patch, win] if x)

            print(_divider())
            print(f"Match  {mid}  |  {meta}" if meta else f"Match  {mid}")

            champ_strs = [
                f"{e['champion']} ({e.get('team_color', '?')})"
                for e in group if e.get("champion")
            ]
            if champ_strs:
                print(f"  Recorded:  {', '.join(champ_strs)}")

            cache_flags = []
            pos_champs = [e["champion"] for e in group
                          if e.get("cache", {}).get("positions") and e.get("champion")]
            if pos_champs:
                cache_flags.append(f"positions({', '.join(pos_champs)})")
            for key in ("timeline", "match_json", "wards"):
                if group[0].get("cache", {}).get(key):
                    cache_flags.append(key)
            if cache_flags:
                print(f"  Cache:  {',  '.join(cache_flags)}")
            print(f"  \u2514 python cache.py {mid}")

        print(_divider())
        n = len(seen_matches)
        print(f"{n} match{'es' if n != 1 else ''} total\n")

    # ── Unprocessed replays ───────────────────────────────────────────────────
    unprocessed = {mid: path for mid, path in rofl_files.items()
                   if mid not in recorded_ids}
    if unprocessed:
        print(f"\nAvailable Replays  (replays/)")
        print(_divider("-", 70))
        for mid in sorted(unprocessed):
            rofl_meta = parse_rofl_metadata(unprocessed[mid])
            parts = []
            if rofl_meta:
                if rofl_meta.get("duration"):
                    parts.append(rofl_meta["duration"])
                if rofl_meta.get("patch"):
                    parts.append(f"Patch {rofl_meta['patch']}")
                if rofl_meta.get("blue_wins") is not None:
                    parts.append("Blue wins" if rofl_meta["blue_wins"] else "Red wins")
            if not parts:
                cs = _cache_status(mid)
                cache_parts = [k for k in ("timeline", "match_json") if cs[k]]
                parts = cache_parts or ["no metadata"]
            print(f"  {mid:<28}  {'  |  '.join(parts)}")
            print(f"    \u2514 python cache.py {mid}")
        print(_divider("-", 70))
        u = len(unprocessed)
        print(f"{u} unprocessed replay{'s' if u != 1 else ''}")

    # ── Quick start (only when there are no recorded games yet) ───────────────
    if not entries:
        print()
        print("Quick start")
        print("  1. Open a replay in the LoL client")
        print("  2. python main.py --player <champion or summoner name>")
        print("     Records the game automatically \u2014 path image and ward map saved to outputs/")
        print("  3. python analyze.py  /  python wards.py  (optional \u2014 needs Riot API data)")
        print(f"  \u2192 Run: python cache.py <match_id>  for copy-paste commands\n")


def _print_detail_unprocessed(match_id, rofl_path):
    """Detail view for a replay that hasn't been recorded or analyzed yet."""
    W = 78
    cs       = _cache_status(match_id)
    rofl_rel = os.path.relpath(rofl_path, _ROOT).replace("\\", "/")
    rofl_meta = parse_rofl_metadata(rofl_path)

    print()

    # Header line
    meta_parts = []
    if rofl_meta:
        if rofl_meta.get("duration"):
            meta_parts.append(rofl_meta["duration"])
        if rofl_meta.get("patch"):
            meta_parts.append(f"Patch {rofl_meta['patch']}")
        if rofl_meta.get("blue_wins") is not None:
            meta_parts.append("Blue wins" if rofl_meta["blue_wins"] else "Red wins")
    header = f"Match  {match_id}"
    if meta_parts:
        header += f"  |  {'  |  '.join(meta_parts)}"
    print(header)
    print(_divider("\u2500", W))

    # Roster from rofl metadata — summoner names + teams (champion names need match JSON)
    participants = (rofl_meta or {}).get("participants", [])
    if participants:
        blue = [p for p in participants if p["team"] == "blue"]
        red  = [p for p in participants if p["team"] == "red"]
        for label, team in [("Blue Team", blue), ("Red Team", red)]:
            names = [p["summoner"] for p in team if p.get("summoner")]
            if names:
                print(f"\n{label}")
                for n in names:
                    print(f"    {n}")
        if not cs["match_json"]:
            print("\n  (champion names unavailable — download match JSON to see them)")
    else:
        print(f"\n  Replay:  {rofl_rel}")

    print()
    print(_divider("\u2500", W))

    # Step 1 — Record
    print(f"\nStep 1 — Open the replay in the LoL client, then record")
    print(f"\n  Open:    {rofl_rel}")
    print(f"  Record:  python main.py --player <champion or summoner name>")
    if cs["timeline"]:
        print(f"           Timeline auto-detected: cache/timeline_{match_id}.json")
    print(f"\n  Saves position data, renders the path map and ward map to outputs/.\n")

    # Step 2 — Analyze (only if timeline present)
    if cs["timeline"]:
        print(f"Step 2 — Analyze")
        print(f"\n  python analyze.py cache/timeline_{match_id}.json --champion <name>")
        print(f"  python wards.py cache/timeline_{match_id}.json\n")

    # Optional — Riot API data
    missing = [k for k in ("timeline", "match_json") if not cs[k]]
    if missing:
        print(f"Optional \u2014 Download Riot API data for ward maps and full analysis")
        if not cs["timeline"]:
            print(f"\n  Timeline  (ward events, kills, gold/XP per minute)")
            print(f"    GET /lol/match/v5/matches/{match_id}/timeline")
            print(f"    save as:  cache/timeline_{match_id}.json")
        if not cs["match_json"]:
            print(f"\n  Match data  (champion names, summoner names, queue type)")
            print(f"    GET /lol/match/v5/matches/{match_id}")
            print(f"    save as:  cache/match_{match_id}.json")
        if not cs["timeline"]:
            print(f"\n  Then run:  python analyze.py cache/timeline_{match_id}.json --champion <name>")
            print(f"             python wards.py cache/timeline_{match_id}.json")
        print()

    print(_divider("\u2500", W))
    print(f"Outputs  \u2192  outputs/{match_id}/\n")


def _print_detail(entries, match_id):
    """Detailed view for a single match: roster + commands."""
    group = [e for e in entries if e.get("match_id") == match_id]
    if not group:
        rofl_files = find_rofl_files()
        if match_id in rofl_files:
            _print_detail_unprocessed(match_id, rofl_files[match_id])
        else:
            print(f"No data found for match '{match_id}'.")
            print(f"  \u2192 Available matches: python cache.py")
        return

    g0 = group[0]
    date  = _format_date(g0.get("game_date") or g0.get("recorded_at"))
    dur   = g0.get("duration") or ""
    q     = g0.get("queue") or ""
    patch = f"Patch {g0['patch']}" if g0.get("patch") else ""
    win   = ("Blue wins" if g0.get("blue_wins") else "Red wins") if g0.get("blue_wins") is not None else ""
    meta  = "  |  ".join(x for x in [date, dur, q, patch, win] if x)

    W = 78
    print()
    print(f"Match  {match_id}  |  {meta}" if meta else f"Match  {match_id}")
    print(_divider("\u2500", W))

    # Player roster
    all_players = g0.get("all_players", [])
    recorded_champs = _recorded_champions(group)

    if all_players:
        blue = [p for p in all_players if p.get("team") == "blue"]
        red  = [p for p in all_players if p.get("team") == "red"]
        for team_label, team in [("Blue Team", blue), ("Red Team", red)]:
            print(f"\n{team_label}")
            for p in team:
                pid   = p.get("participant_id", "?")
                champ = p.get("champion") or ""
                summ  = p.get("summoner", "")
                marker = "  \u2190 recorded" if champ and champ in recorded_champs else ""
                print(f"  {pid:>2}  {champ:<16} {summ}{marker}")
        if not g0.get("cache", {}).get("match_json") and not any(p.get("champion") for p in all_players):
            print("\n  (champion names unavailable — download match JSON to see them)")
    else:
        # No match JSON or rofl metadata — show what we know from recorded entries
        print("\nPlayers  (full roster unavailable — download match JSON to see all 10)")
        for e in group:
            if e.get("champion"):
                print(f"  {e['champion']:<16} {e.get('summoner', '')}  ({e.get('team_color', '?')} team)")

    print()
    print(_divider("\u2500", W))
    print("\nCommands (copy-paste for this match_id)\n")

    tl_path = f"cache/timeline_{match_id}.json"
    has_tl  = g0.get("cache", {}).get("timeline")

    # Record path — timeline is auto-detected if present
    first_recorded = next((e["champion"] for e in group if e.get("champion")), None)
    if first_recorded:
        tl_note = "(timeline auto-detected)" if has_tl else "  (add timeline for ward map)"
        print(f"\n  Record path {tl_note}")
        print(f"    python main.py --player {first_recorded}")

    # Analyze (one block per recorded champion with renders)
    for e in group:
        champ = e.get("champion")
        if not champ:
            continue
        renders = e.get("renders", [])
        render_str = "  ".join(renders) if renders else "none yet"
        print(f"\n  Analyze ({champ})   renders: {render_str}")
        print(f"    python analyze.py {tl_path} --champion {champ}")

    # Re-render path (if positions exist)
    for e in group:
        champ = e.get("champion")
        if champ and e.get("cache", {}).get("positions"):
            print(f"\n  Re-render path ({champ})")
            print(f"    python render.py cache/positions_{champ}.json")

    # Ward maps
    print(f"\n  Ward map (all players)")
    print(f"    python wards.py {tl_path}")
    print(f"\n  Ward map (blue team)")
    print(f"    python wards.py {tl_path} --team blue")
    print(f"\n  Ward map (single player — replace N with participant ID 1-10)")
    print(f"    python wards.py {tl_path} --participant N")

    print()
    print(_divider("\u2500", W))
    print(f"Outputs  \u2192  outputs/{match_id}/\n")


# -- Scan ----------------------------------------------------------------------

def scan_replays():
    """Bootstrap games.json entries for every replay file not yet indexed.

    For each .rofl in replays/ (and legacy directories) that has no games.json
    entry, creates a stub entry and enriches it from any match JSON already
    present in cache/. Matches that already have at least one entry are skipped
    (their cache flags are still refreshed on the next tool run).

    Prints a summary of what was added.
    """
    entries    = _load_games()
    rofl_files = find_rofl_files()
    recorded   = {e.get("match_id") for e in entries if e.get("match_id")}

    new_ids = sorted(mid for mid in rofl_files if mid not in recorded)
    if not new_ids:
        print("All replay files are already indexed in games.json.")
        return

    print(f"Scanning {len(new_ids)} unindexed replay{'s' if len(new_ids) != 1 else ''}...\n")
    for mid in new_ids:
        rofl_meta = parse_rofl_metadata(rofl_files[mid])

        # Populate all_players from rofl (summoner names + teams; champion names filled later by match JSON)
        all_players_rofl = []
        if rofl_meta and rofl_meta.get("participants"):
            for i, p in enumerate(rofl_meta["participants"]):
                all_players_rofl.append({
                    "participant_id": i + 1,
                    "champion":       None,
                    "champion_id":    p.get("champion_id"),
                    "summoner":       p.get("summoner", ""),
                    "team":           p["team"],
                })

        entry = {
            "match_id":    mid,
            "champion":    None,
            "summoner":    None,
            "team_color":  "",
            "recorded_at": datetime.now(tz=timezone.utc).isoformat(),
            "game_date":   None,
            "duration":    rofl_meta.get("duration") if rofl_meta else None,
            "queue":       None,
            "patch":       rofl_meta.get("patch") if rofl_meta else None,
            "platform":    mid.split("_")[0] if "_" in mid else None,
            "blue_wins":   rofl_meta.get("blue_wins") if rofl_meta else None,
            "cache":       {},
            "renders":     [],
            "all_players": all_players_rofl,
        }
        entries.append(entry)
        _refresh_cache_flags(entry)
        _enrich_from_match_json(entry, mid)  # overwrites all_players with champion names if match JSON present

        meta_parts = []
        if entry.get("game_date"):
            meta_parts.append(entry["game_date"][:10])
        elif entry.get("duration"):
            meta_parts.append(entry["duration"])
        if entry.get("queue"):
            meta_parts.append(entry["queue"])
        if entry.get("patch"):
            meta_parts.append(f"Patch {entry['patch']}")
        if entry.get("blue_wins") is not None:
            meta_parts.append("Blue wins" if entry["blue_wins"] else "Red wins")
        meta = "  |  ".join(meta_parts) if meta_parts else "no metadata"
        cache_str = "  ".join(k for k, v in entry["cache"].items() if v) or "none"
        print(f"  + {mid}  |  {meta}")
        print(f"    cache: {cache_str}\n")

    entries.sort(key=lambda e: e.get("recorded_at") or "", reverse=True)
    _save_games(entries)
    print(f"Added {len(new_ids)} {'entry' if len(new_ids) == 1 else 'entries'} to games.json.")
    print(f"  \u2192 Run  python cache.py <match_id>  for details and recording commands.")


# -- Entry point ----------------------------------------------------------------

if __name__ == "__main__":
    import argparse as _ap
    p = _ap.ArgumentParser(
        description="Cache manager — list matches, inspect a match, or fetch API data.",
        formatter_class=_ap.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  python cache.py                list all cached matches and available replays\n"
            "  python cache.py OC1_697009636  detailed view with roster and commands\n"
            "  python cache.py --scan         index replay files in replays/ (no API calls)\n"
            "  python cache.py --load         fetch match + timeline JSON from Riot API\n"
            "\n"
            "API key (for --load):\n"
            f"  Save key to:  {API_KEY_FILE}\n"
            "  Or set env:   RIOT_API_KEY=RGAPI-xxx\n"
            "  Get a key:    https://developer.riotgames.com"
        ),
    )
    p.add_argument("match_id", nargs="?", help="Match ID to show details for")
    p.add_argument("--scan", action="store_true",
                   help="Index all replay files in replays/ into games.json (no API calls)")
    p.add_argument("--load", action="store_true",
                   help="Fetch match + timeline JSON from Riot API for all replays missing them")
    args = p.parse_args()

    if args.load:
        load_replays()
    elif args.scan:
        scan_replays()
    elif args.match_id:
        _print_detail(_load_games(), args.match_id)
    else:
        _print_list(_load_games())
