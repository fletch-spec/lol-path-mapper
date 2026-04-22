# League of Legends Replay API

The script communicates with LoL's local replay API, available at `https://127.0.0.1:2999` while a replay is open.

**Note**: The API uses a self-signed certificate. The script disables certificate verification for localhost connections.

## Endpoints

### `/liveclientdata/allgamedata`

Returns the full game state object.

**Used for**: Confirming a replay is loaded, extracting game metadata.

**Response**:
```json
{
  "allPlayers": [...],
  "gameData": {
    "gameId": 1234567890,
    "mapId": 11,
    "gameMode": "CLASSIC",
    ...
  }
}
```

### `/liveclientdata/playerlist`

Returns the player roster for the current match.

**Used for**: Selecting which champion to track.

**Response**:
```json
[
  {
    "championName": "Ahri",
    "riotIdGameName": "PlayerName",
    "riotIdTagLine": "NA1",
    "summonerName": "Summoner Name",
    "team": "ORDER",  // or "CHAOS"
    ...
  },
  ...
]
```

Teams:
- `"ORDER"` = Blue team
- `"CHAOS"` = Red team

### `/replay/playback`

Get or set replay playback state.

**GET response**:
```json
{
  "time": 123.45,
  "length": 1234.56,
  "paused": false,
  "speed": 16.0
}
```

**POST parameters**:
```json
{
  "time": 0.5,
  "paused": false,
  "speed": 32.0
}
```

### `/replay/render`

Get or set camera attachment and position.

**GET response**:
```json
{
  "cameraAttached": true,
  "selectionName": "Ahri",
  "cameraPosition": {
    "x": 6000.0,
    "y": -9000.0,
    "z": 6000.0
  }
}
```

**POST parameters** (attach camera to a champion):
```json
{
  "selectionName": "Ahri",
  "cameraAttached": true
}
```

**Camera position**: `x` and `z` correspond to the in-game map coordinates (note: `z` is vertical in the API response, not `y`).

## Error Handling

### ReplayNotAvailable

Raised when:
- The client is unreachable (port 2999 not open)
- The replay has been closed
- A timeout occurs (default 5 seconds)

Typically means:
- The replay is not open
- The client has crashed or been closed
- The network is blocked (firewall, VPN)

### KeyError (missing field in API response)

Raised when the API returns an unexpected response structure.

Typically means:
- Replay API is not enabled (check game.cfg)
- The client version changed
- The API request succeeded but the structure changed

## Rate Limits

No explicit rate limit, but:
- Polling too frequently (< 0.05s) may stress the client
- Default poll interval is **0.1 seconds** (10 Hz)
- Playback can be set to 32x+ speed without issues
