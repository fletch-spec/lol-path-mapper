# Data Sources: APIs, Replays, and Databases

## Purpose

Define the data sources that feed the graphic, their reliability, update frequency, and fallback mechanisms.

## Primary Data Sources

### 1. Riot Games API (Official)

**Purpose:** Authoritative match timeline, participant frames, game events

**Endpoints:**
- `GET /lol/match-v5/matches/{matchId}` – Full match data (stats, timeline, participants)
- `GET /lol/summoner-v4/summoners/{summonerName}` – Player profile (tier, LP)
- `GET /lol/static-data/...` – Champion, item, ability definitions

**Data Provided:**
- Match timeline (minute-by-minute state)
- Participant stats (kills, deaths, CS, gold, damage, etc.)
- Events (kills, deaths, objectives, level-ups)
- Team composition, bans, itemization
- Game duration, mode, patch version

**Reliability:**
- SLA: 99.5% uptime
- Rate limits: 100 requests per 2 minutes (per API key)
- Latency: <200ms typical (p99: <1s)

**Update Frequency:**
- Match data: Available within 5 minutes of game end
- Static data (items, champions): Updated per patch (bi-weekly)

**Fallback:** If API unavailable, show cached data from last successful fetch (up to 7 days old with "outdated" warning)

### 2. Replay Files (Local Client)

**Purpose:** Extract champion positioning data via computer vision

**Data Provided:**
- Video frames (30 fps, 1920×1920)
- Minimap overlay (vision data)
- Terrain/brush overlay

**Storage:**
- Location: Client replay cache (typically `LeagueClient/Replays/`)
- Size: ~500 MB per 30-minute game
- Retention: Auto-managed by client (typically 30 days)

**Access:** 
- Local-only: No transmission over network
- Opt-in: User must explicitly enable CV heatmap processing
- Processing: Client-side ML (YOLO on CPU, ~60 seconds per 30-min game)

**Reliability:**
- Replays available only after player has closed game (not real-time)
- Replay corruption rare (<0.1%) but possible with client crashes

### 3. Match Performance Database (Cloud)

**Purpose:** Store historical player stats for percentile rankings and role-normalization

**Data Stored:**
- Aggregated stats per player per champion (anonymized IDs)
- Role archetype classifications (PCA-based)
- Percentile rankings (updated weekly)

**Examples:**
- "Ahri mid players in Diamond, last 30 days: KP average 52%, std dev 11%"
- "Top 12% of Ahri players have >62% KP"

**Update Frequency:** Weekly (post-major patches; daily for smaller stats)

**Data Retention:**
- Current season: Full granularity (daily percentiles)
- Previous season: Monthly aggregates only
- Older: Deleted after 2 years

**Privacy:** 
- Individual player data is never stored
- Only aggregates (50+ games minimum per bucket) are retained
- Player names, IDs are hashed (one-way)

### 4. Pro Play Game Database (Cloud, Public)

**Purpose:** Feed Shadow Match comparisons and benchmark analysis

**Data Stored:**
- 10,000+ professional games per year (LEC, LCS, LCK, Worlds, etc.)
- Full match timelines, team compositions, play-by-play
- Publicly available via Riot API

**Licensing:** Public data; attribution required

**Update Frequency:** Per-day (new games ingested daily)

## Secondary Data Sources

### Champion & Item Definitions

**Source:** Riot Data Dragon (static data)  
**Update:** Per patch (bi-weekly)  
**Content:** Champion abilities, item stats, ability ratios, costs

### Talent/Pro Player Stats

**Source:** Leaderboards API + pro leagues data  
**Update:** Daily  
**Use:** Identify "similar pro player" for Shadow Match

## Data Validation

**Sanity Checks:**
- Match duration: 0-60 minutes (flag <8 min as "FF" or >60 min as "Long game")
- Participant counts: Exactly 10 players per match
- Gold values: >1000 gold per game (flag <1000 as suspicious)
- Death count: Max 20 deaths per player (flag >20 as possible data error)

**Error Handling:**
- If data fails validation, show "Data unavailable" and fall back to cached version
- Log errors for investigation

## Data Latency & Caching

**Caching Strategy:**

| Data | Cache Duration | Freshness Strategy |
|------|---------------|--------------------|
| Match data (timeline) | 7 days | Use immediately; validate against API |
| Replay file | 30 days | Process only if file still exists on disk |
| Percentile rankings | 7 days | Update weekly; serve cached immediately |
| Pro play database | 1 day | Update batch nightly |
| Static data (items/champs) | 14 days | Fetch new patch immediately |

**On Network Error:** Serve cached data with "outdated" warning (if available)

## Geographic Distribution

**API Regional Endpoints:**
- NA: api.na1.leagueoflegends.com
- EU: api.euw1.leagueoflegends.com
- APAC: api.ap1.leagueoflegends.com

**Cloud Services:**
- Match database: Multi-region (US-East, EU-West, APAC, backup in each)
- Pro play database: CDN-backed (edge servers in all major regions)

**Latency Targets:**
- US: <100ms
- EU: <100ms
- APAC: <200ms (longer distances)

## Bandwidth & Quota

**Riot API:**
- Rate limit: 100 requests per 2 minutes
- Per-match bandwidth: ~50 KB (typical match data)

**Replay Processing:**
- Bandwidth: 0 (local-only; no transmission)
- Computation: ~500 MB RAM, 1 CPU core for 60 seconds

**Cloud Processing:**
- Bandwidth per match: ~5 MB (after compression)
- Storage per match: ~100 KB (aggregated stats)

## Fallback & Degradation

**If API Unavailable:**
- Show cached match data (up to 7 days old) with warning
- NLG/insights use cached percentiles (less accurate but functional)

**If Replay Unavailable:**
- Skip heatmap generation; show message "Replay not available for positioning analysis"
- All other zones still functional

**If Cloud Databases Offline:**
- Show player's current season percentiles (best guess)
- Flag as "estimated" rather than official

## Boundaries

**Assumes:**
- Riot API is reliable and accurate
- Replays are available for most recent games
- User has internet access for cloud features (optional)

**Provides:**
- Authoritative match data for all computations
- Comprehensive historical context for benchmarking
- Pro-level comparison data
