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
CACHE_DIR = os.path.join(os.path.dirname(__file__), ".dev", "cache")


def _get(path, timeout=5):
    return requests.get(f"{BASE_URL}{path}", verify=False, timeout=timeout).json()


def _post(path, data, timeout=5):
    return requests.post(f"{BASE_URL}{path}", json=data, verify=False, timeout=timeout)


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
        except (requests.ConnectionError, requests.Timeout):
            pass
        time.sleep(2)


def get_players():
    """Return player list. Each entry has: championName, riotIdGameName, riotIdTagLine, team."""
    return _get("/liveclientdata/playerlist")


def get_playback():
    return _get("/replay/playback")


def set_playback(**fields):
    _post("/replay/playback", fields)


def get_render():
    return _get("/replay/render")


def set_render(**fields):
    _post("/replay/render", fields)


def _attach_camera(champion_name, summoner_name=None):
    """Attempt to attach the camera to a champion. Returns the render state on success."""
    # Try multiple name formats: champion name, summoner name, lowercase variants
    candidates = [champion_name]
    if summoner_name:
        candidates.append(summoner_name)
    candidates += [champion_name.lower(), champion_name.replace(" ", "")]

    for name in candidates:
        _post("/replay/render", {"selectionName": name, "cameraAttached": True})
        time.sleep(0.3)
        state = get_render()
        sel = state.get("selectionName", "")
        attached = state.get("cameraAttached", False)
        if sel and attached and sel.lower() != "":
            print(f"  Camera attached via selectionName='{sel}' (tried '{name}')")
            return state

    # Print full render state for debugging
    state = get_render()
    print(f"  Warning: camera may not be attached. Render state:")
    for k in ["selectionName", "cameraAttached", "cameraMode", "cameraPosition"]:
        print(f"    {k}: {state.get(k)}")
    return state


def collect_positions(champion_name, speed=8, poll_interval=0.1, summoner_name=None):
    """Play through the replay at high speed, polling camera position.

    Returns a list of (game_time, x, y) tuples.
    Camera is attached to the champion; cameraPosition (x, z) = game map (x, y).
    """
    # Rewind and pause
    set_playback(time=0.5, paused=True)
    time.sleep(1)

    # Attach camera
    print(f"Attaching camera to {champion_name}...")
    _attach_camera(champion_name, summoner_name)

    # Advance a few seconds so the champion has spawned, verify camera is moving
    set_playback(speed=1.0, paused=False)
    time.sleep(2)
    pos_a = get_render().get("cameraPosition", {})
    time.sleep(2)
    pos_b = get_render().get("cameraPosition", {})

    if pos_a == pos_b:
        print(f"  Warning: camera position is not changing — champion may not be tracked.")
        print(f"  Position: {pos_a}")
    else:
        print(f"  Camera is tracking. Position range: {pos_a} -> {pos_b}")

    # Rewind and run at full speed
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
        except (requests.ConnectionError, requests.Timeout):
            print("\n  Connection lost — stopping collection.")
            break

    print(f"\nDone: {len(positions)} samples collected.\n")
    set_playback(paused=True)
    return positions



def save_positions(positions, champion_name):
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, f"positions_{champion_name}.json")
    with open(path, "w") as f:
        json.dump(positions, f)
    print(f"Saved position data -> {path}")
    return path


def load_positions(path):
    with open(path) as f:
        return json.load(f)
