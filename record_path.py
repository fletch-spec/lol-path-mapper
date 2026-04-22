"""Record a champion's movement path from a live LoL replay and render it.

Usage:
    python record_path.py
"""

import json
import os
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

import requests
import urllib3

# Suppress the self-signed certificate warning from the local API
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Ensure Unicode output works on Windows terminals
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_URL = "https://127.0.0.1:2999"
DEFAULT_MAP = os.path.join(os.path.dirname(__file__), "summoners_rift.png")
OUTPUT_DIRECTORY = "outputs"
CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")


class ReplayNotAvailable(ConnectionError):
    """Raised when the local replay API is unreachable or returns an error."""
    pass


def _get(path: str, timeout: int = 5) -> Dict[str, Any]:
    """GET a replay API endpoint and return parsed JSON."""
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


def _post(path: str, data: Dict[str, Any], timeout: int = 5) -> requests.Response:
    """POST to a replay API endpoint."""
    try:
        return requests.post(f"{BASE_URL}{path}", json=data, verify=False, timeout=timeout)
    except requests.exceptions.Timeout:
        raise ReplayNotAvailable(f"The LoL client stopped responding ({path}).")
    except requests.exceptions.ConnectionError:
        raise ReplayNotAvailable(f"Could not reach the LoL client ({path}).")


def wait_for_replay() -> None:
    """Block until both liveclientdata and the replay API are reachable."""
    print("Waiting for League replay... (open a .rofl file in the client)")
    while True:
        try:
            data = _get("/liveclientdata/allgamedata")
            if "allPlayers" in data:
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


def get_game_data() -> Dict[str, Any]:
    """Return the gameData object from allgamedata, or {} on failure."""
    try:
        return _get("/liveclientdata/allgamedata").get("gameData", {})
    except (ReplayNotAvailable, KeyError, TypeError, AttributeError):
        return {}


def get_players() -> List[Dict[str, Any]]:
    """Return player list."""
    return _get("/liveclientdata/playerlist")


def get_playback() -> Dict[str, Any]:
    return _get("/replay/playback")


def set_playback(**fields) -> None:
    _post("/replay/playback", fields)


def get_render() -> Dict[str, Any]:
    return _get("/replay/render")


def set_render(**fields) -> None:
    _post("/replay/render", fields)


def _attach_camera(champion_name: str, summoner_name: Optional[str] = None) -> Dict[str, Any]:
    """Attach the camera to a champion, retrying up to 3 times."""
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
    return state


def collect_positions(
    champion_name: str,
    speed: int = 16,
    poll_interval: float = 0.1,
    summoner_name: Optional[str] = None,
) -> List[Tuple[float, float, float]]:
    """Play through the replay at high speed, polling camera position."""
    set_playback(time=5.0, paused=False, speed=1.0)
    time.sleep(3)

    print(f"Attaching camera to {champion_name}...")
    _attach_camera(champion_name, summoner_name)

    pos_a = get_render().get("cameraPosition", {})
    time.sleep(1.5)
    pos_b = get_render().get("cameraPosition", {})

    if pos_a == pos_b:
        print(f"  Warning: camera is not following {champion_name} — position is not changing.")
    else:
        print(f"  Camera is tracking.")

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


def save_positions(positions: List[Tuple[float, float, float]], champion_name: str, summoner_name: str = "") -> str:
    """Save positions to cache."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, f"positions_{champion_name}.json")
    with open(path, "w") as f:
        json.dump({"meta": {"summoner": summoner_name, "champion": champion_name},
                   "positions": positions}, f)
    print(f"Saved position data -> {path}")
    return path


def load_positions(champion_name: str) -> Optional[List[Tuple[float, float, float]]]:
    """Load cached positions if they exist, otherwise return None."""
    path = os.path.join(CACHE_DIR, f"positions_{champion_name}.json")
    if not os.path.exists(path):
        return None
    try:
        with open(path) as f:
            data = json.load(f)
        # Handle both new dict format and old raw-list format
        if isinstance(data, dict):
            return data.get("positions", [])
        return data
    except (json.JSONDecodeError, ValueError):
        return None


def render_path(
    map_image: str,
    positions: List[Tuple[float, float]],
    output_path: str,
    downscale: int = 4,
) -> None:
    """Render a path overlay onto the map image."""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("Error: PIL/Pillow is required for rendering.")
        print("  Install with: pip install Pillow")
        sys.exit(1)

    if not os.path.exists(map_image):
        raise FileNotFoundError(f"Map image not found: {map_image}")

    img = Image.open(map_image)
    draw = ImageDraw.Draw(img, "RGBA")

    # Draw path with gradient coloring: blue (t=0) to red (t=1)
    if len(positions) > 1:
        for i in range(len(positions) - 1):
            x1, y1 = positions[i]
            x2, y2 = positions[i + 1]

            # Gradient: blue (0) → purple → red (1)
            t = i / max(len(positions) - 1, 1)
            if t < 0.5:
                r = int(128 * (t * 2))
                g = 0
                b = int(255 - 128 * (t * 2))
            else:
                r = int(128 + 127 * ((t - 0.5) * 2))
                g = 0
                b = int(128 - 128 * ((t - 0.5) * 2))

            draw.line([(x1, y1), (x2, y2)], fill=(r, g, b, 200), width=3)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if downscale > 1:
        new_size = (img.width // downscale, img.height // downscale)
        img = img.resize(new_size, Image.Resampling.LANCZOS)

    img.save(output_path)
    print(f"Path rendered -> {output_path}")


def select_player(players: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Display player list and return interactive selection."""
    print("Players:")
    for i, p in enumerate(players, 1):
        name = p.get("riotIdGameName") or p.get("summonerName", "Unknown")
        tag = p.get("riotIdTagLine", "")
        champ = p["championName"]
        team = "Blue" if p["team"] == "ORDER" else "Red"
        display = f"{name}#{tag}" if tag else name
        print(f"  {i:2d}. {display:<25s} {champ:<15s} ({team})")

    while True:
        try:
            choice = int(input(f"\nSelect player (1-{len(players)}): "))
            if 1 <= choice <= len(players):
                return players[choice - 1]
        except (ValueError, EOFError):
            pass
        print("Invalid choice.")


def make_output_filename(match_id: str, champion: str, player_name: str, kda: Tuple[int, int, int]) -> str:
    """Build filename: [MATCH_ID] champion - player (k/d/a).png"""
    # Sanitize player name: keep only alphanumeric, spaces, hyphens, underscores
    safe_player = "".join(c for c in player_name if c.isalnum() or c in " _-").rstrip()
    k, d, a = kda
    return f"[{match_id}] {champion} - {safe_player} ({k}/{d}/{a}).png"


def main():
    if not os.path.exists(DEFAULT_MAP):
        print(f"Map image not found: {DEFAULT_MAP}")
        print("  → Place summoners_rift.png in the project root (8192×8192 recommended).")
        sys.exit(1)

    wait_for_replay()

    # Get match ID from game data
    game_data = get_game_data()
    match_id = str(game_data.get("gameId", "UNKNOWN"))

    try:
        players = get_players()
    except ReplayNotAvailable:
        print("Could not load the player list — the replay may have been closed or paused.")
        print("  → Keep the replay playing and try again.")
        sys.exit(1)

    selected = select_player(players)
    champ = selected["championName"]
    summoner = selected.get("riotIdGameName") or selected.get("summonerName", "unknown")

    # Extract KDA from player stats
    stats = selected.get("stats", {})
    kda = (stats.get("kills", 0), stats.get("deaths", 0), stats.get("assists", 0))

    print(f"\nTracking: {champ} ({summoner}) - KDA: {kda[0]}/{kda[1]}/{kda[2]}\n")

    # Check if positions are already cached
    cached_positions = load_positions(champ)
    if cached_positions:
        print(f"Found {len(cached_positions)} cached position samples for {champ}")
        use_cached = input("Use cached positions? (y/n): ").strip().lower()
        if use_cached == 'y':
            print("Using cached positions.\n")
            positions = cached_positions
        else:
            print("Re-recording positions...\n")
            positions = collect_positions(champ, speed=16, summoner_name=summoner)
            save_positions(positions, champ, summoner_name=summoner)
    else:
        positions = collect_positions(champ, speed=16, summoner_name=summoner)
        save_positions(positions, champ, summoner_name=summoner)

    # Use naming convention: [MATCH_ID] champion - player (k/d/a).png
    filename = make_output_filename(match_id, champ, summoner, kda)
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
    output = os.path.join(OUTPUT_DIRECTORY, filename)

    print(f"Path output: {output}")
    xy = [(x, y) for _, x, y in positions]
    render_path(DEFAULT_MAP, xy, output, downscale=4)


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
        else:
            print("  → Check the path and try again.")
        sys.exit(1)
    except KeyError as e:
        print(f"\nThe replay API returned unexpected data (missing field {e}).")
        print("  → Try restarting the replay or re-enabling the Replay API in game.cfg.")
        sys.exit(1)
    except ValueError as e:
        print(f"\nCould not parse data: {e}")
        print("  → Check the replay API response or re-run the command.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(0)
