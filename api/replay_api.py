"""
LoL replay API client.

Wraps the local League of Legends replay API at https://127.0.0.1:2999.
The API is only available while a replay is open in the client and requires
'EnableReplayApi=1' in game.cfg under [General].

Key endpoints used:
  /liveclientdata/allgamedata  — confirms a game is loaded (no special config needed)
  /liveclientdata/playerlist   — full roster with champion names and team assignments
  /replay/playback             — controls and reads playback state (time, speed, paused)
  /replay/render               — controls camera and reads cameraPosition (x, z = map x, y)
"""

import json
import os
import time

import requests
import urllib3

# Suppress the self-signed certificate warning from the local API
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://127.0.0.1:2999"
CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "cache")


class ReplayNotAvailable(ConnectionError):
    """Raised when a request to the local replay API fails (client closed, not loaded, etc.)."""
    pass


def _get(path, timeout=5):
    """GET a replay API endpoint and return parsed JSON.
    Raises ReplayNotAvailable on any connection or timeout failure."""
    try:
        return requests.get(f"{BASE_URL}{path}", verify=False, timeout=timeout).json()
    except requests.exceptions.Timeout:
        raise ReplayNotAvailable(
            f"The LoL client stopped responding ({path}). "
            "The replay may have ended or the client is busy."
        )
    except requests.exceptions.ConnectionError:
        raise ReplayNotAvailable(
            f"Could not reach the LoL client ({path}). "
            "Make sure a replay is open and the client hasn't closed."
        )


def _post(path, data, timeout=5):
    """POST to a replay API endpoint.
    Raises ReplayNotAvailable on any connection or timeout failure."""
    try:
        return requests.post(f"{BASE_URL}{path}", json=data, verify=False, timeout=timeout)
    except requests.exceptions.Timeout:
        raise ReplayNotAvailable(
            f"The LoL client stopped responding ({path})."
        )
    except requests.exceptions.ConnectionError:
        raise ReplayNotAvailable(
            f"Could not reach the LoL client ({path})."
        )


def wait_for_replay():
    """Block until both liveclientdata and the replay API are reachable."""
    print("Waiting for League replay... (open a .rofl file in the client)")
    while True:
        try:
            # liveclientdata works without EnableReplayApi
            data = _get("/liveclientdata/allgamedata")
            if "allPlayers" in data:
                # Also check the replay API is enabled
                pb = _get("/replay/playback")
                if "errorCode" in pb:
                    print("  Game detected but Replay API not enabled.")
                    print("  Ensure 'EnableReplayApi=1' is in game.cfg [General], then restart the replay.")
                    time.sleep(5)
                    continue
                print("Replay detected!\n")
                return
        except ReplayNotAvailable:
            pass
        time.sleep(2)


def get_players():
    """Return player list. Each entry has: championName, riotIdGameName, riotIdTagLine, team."""
    return _get("/liveclientdata/playerlist")


def get_playback():
    return _get("/replay/playback")


def set_playback(**fields):
    _post("/replay/playback", fields)


def get_game_data():
    """Return the gameData object from allgamedata, or {} on failure."""
    try:
        return _get("/liveclientdata/allgamedata").get("gameData", {})
    except (ReplayNotAvailable, KeyError, TypeError, AttributeError):
        return {}


def get_render():
    return _get("/replay/render")


def set_render(**fields):
    _post("/replay/render", fields)


def _attach_camera(champion_name, summoner_name=None):
    """Attach the camera to a champion, retrying up to 3 times with a delay between attempts.

    Tries several name formats each round (champion name, summoner name, lowercase, no-space).
    Returns the final render state whether or not attachment succeeded.
    """
    candidates = [champion_name]
    if summoner_name:
        candidates.append(summoner_name)
    candidates += [champion_name.lower(), champion_name.replace(" ", "")]

    for attempt in range(3):
        for name in candidates:
            _post("/replay/render", {"selectionName": name, "cameraAttached": True})
            time.sleep(0.3)
            state = get_render()
            if state.get("cameraAttached") and state.get("selectionName", "").strip():
                print(f"  Camera attached to '{state['selectionName']}'")
                return state

        if attempt < 2:
            print(f"  Not attached yet, retrying... ({attempt + 1}/3)")
            time.sleep(1.5)

    state = get_render()
    print(f"  Warning: failed to attach camera after 3 attempts.")
    print(f"    selectionName: {state.get('selectionName')!r}")
    print(f"    cameraAttached: {state.get('cameraAttached')}")
    return state


def collect_positions(champion_name, speed=8, poll_interval=0.1, summoner_name=None):
    """Play through the replay at high speed, polling camera position.

    Returns a list of (game_time, x, y) tuples.
    Camera is attached to the champion; cameraPosition (x, z) = game map (x, y).
    """
    # Play from a few seconds in at 1× speed so champion entities are loaded
    # before the attach attempt (attaching at t=0 while paused fails to select anything)
    set_playback(time=5.0, paused=False, speed=1.0)
    time.sleep(3)  # let the engine render ~3 seconds of live gameplay

    # Attach camera now that the champion is on the map
    print(f"Attaching camera to {champion_name}...")
    _attach_camera(champion_name, summoner_name)

    # Verify the camera is actually following the champion
    pos_a = get_render().get("cameraPosition", {})
    time.sleep(1.5)
    pos_b = get_render().get("cameraPosition", {})

    if pos_a == pos_b:
        print(f"  Warning: camera is not following {champion_name} — position is not changing.")
        print(f"  Position: {pos_a}")
    else:
        print(f"  Camera is tracking.")

    # Rewind to the start and run at full collection speed
    set_playback(time=0.5, paused=True)
    time.sleep(0.5)
    set_playback(speed=float(speed), paused=False)
    time.sleep(0.5)

    game_length = get_playback()["length"]
    est_seconds = game_length / speed
    print(f"Collecting positions — {game_length:.0f}s game @ {speed}x speed (≈{est_seconds:.0f}s real time)\n")

    positions = []
    last_time = -1

    while True:
        try:
            render = get_render()
            pb = get_playback()
            game_time = pb["time"]

            cam = render.get("cameraPosition", {})
            x, y = cam.get("x"), cam.get("z")

            if x is not None and y is not None and game_time != last_time:
                positions.append((round(game_time, 2), round(x, 1), round(y, 1)))
                last_time = game_time

            pct = min(game_time / game_length * 100, 100)
            print(f"\r  {pct:5.1f}%  {game_time:6.0f}s / {game_length:.0f}s  |  {len(positions)} samples", end="", flush=True)

            if game_time >= game_length - 1:
                break

            time.sleep(poll_interval)
        except ReplayNotAvailable:
            print("\n  Connection lost — stopping collection.")
            break

    print(f"\nDone: {len(positions)} samples collected.\n")
    set_playback(paused=True)
    return positions



def save_positions(positions, champion_name, summoner_name=""):
    """Save positions to cache, wrapped with metadata for output filename construction."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, f"positions_{champion_name}.json")
    with open(path, "w") as f:
        json.dump({"meta": {"summoner": summoner_name, "champion": champion_name},
                   "positions": positions}, f)
    print(f"Saved position data -> {path}")
    return path


def load_positions(path):
    """Load positions from cache. Returns (meta_dict, positions_list).

    Handles both the new dict format {"meta": ..., "positions": [...]}
    and the old raw-list format for backward compatibility.
    """
    with open(path) as f:
        data = json.load(f)
    if isinstance(data, dict):
        return data.get("meta", {}), data.get("positions", [])
    # Old format: raw list — derive champion name from filename
    name = os.path.splitext(os.path.basename(path))[0].replace("positions_", "")
    return {"summoner": "", "champion": name}, data
