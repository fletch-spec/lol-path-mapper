# Comprehensive Infographic Specification: "The Summoner's Chronicle"  
## *Post-Game Champion-Centric Analysis Graphic*

**Project:** info-lol (The Summoner's Chronicle)  
**Version:** 0.0.3 (Development)  
**Status:** Active Development — Core Infrastructure  
**Last Updated:** 2026-04-10

---

## I. OVERVIEW & PHILOSOPHY

**Purpose:** To transform raw post-game statistics into a narrative-driven, visually compelling story of a single champion's performance, contextualized within the broader match dynamics. The graphic serves both as a learning tool (identifying strengths/weaknesses) and a celebratory artifact (highlighting exceptional plays).

**Target Audience:** Players from Silver to Diamond who want actionable insights, plus casual viewers who appreciate dramatic data storytelling.

**Champion Selection:** The graphic focuses on **one champion per player**, generated on-demand (player chooses which champion to analyze post-game). The system defaults to the player's played champion unless overridden.

**Tone:** Analytical but accessible, dramatic but data-honest. Uses League lexicon without assuming deep statistical literacy.

---

## II. VISUAL HIERARCHY & LAYOUT DIMENSIONS

**Canvas Size:** 1920×2400 pixels (vertical scroll-friendly, printable as poster)

**Layout Zones (top to bottom):**

| Zone | Height | Content |
|------|--------|---------|
| 1. Header | 200px | Match context, result, role, champion identity |
| 2. Champion Portrait & Core Stats | 400px | Splash art + 5-ring performance dial |
| 3. Timeline Narrative | 500px | Chronological event strip with momentum arc |
| 4. Advanced Performance Matrix | 450px | Heatmaps, gold/xp differentials, efficiency ratios |
| 5. Positioning & Vision Intelligence | 350px | Theoretical CV-generated heatmap + vision denial zones |
| 6. Build & Ability Breakdown | 300px | Item spike windows, ability efficiency rating |
| 7. Comparative & Predictive Insights | 200px | Percentile rankings, "shadow match" comparison |

---

## III. ZONE-BY-ZONE CONTENT SPECIFICATION

### ZONE 1: HEADER — Match Context & Champion Identity

**Elements:**

- **Match Result Banner:** Full-width gradient (blue for win, red for loss) with "VICTORY" or "DEFEAT" typography. Subtle particle effects in background (falling laurels for win, shattered runes for loss).
- **Game ID & Timestamp:** Small text, bottom-left of banner. Format: `#NA1-4872291032 • 2025-01-15 • 23:42 UTC`
- **Role & Lane Assignment:** Icon + text (e.g., 🗡️ Mid Lane / 🛡️ Top / 🌟 Support). Algorithm-determined via 2-minute positional data (not player-reported).
- **Champion Name & Title:** Large display type. Example: *"AHRI • THE NINE-TAILED FOX"*
- **Player Summoner Name:** Subtle but prominent, below champion name.
- **Patch & Game Mode:** `Patch 15.1 • Ranked Solo/Duo • 34:21 match duration`

**Strategic Insight Callout (corner ribbon):**  
*"This match lasted 2:14 longer than your average Ahri game — late-game scaling mattered."*

---

### ZONE 2: CHAMPION PORTRAIT & CORE STATS — The Five-Ring Performance Dial

**Visual:** High-resolution splash art (slightly desaturated, framed in a runic circle) on the left. Right side displays a pentagon radar chart with five key metrics, normalized against the champion's *role-specific expected ranges* (not global averages).

**The Five Metrics (each with tooltip-on-hover definition):**

1. **Kill Participation** — `(Kills + Assists) / Team Total Kills`  
   *Benchmark: 50-60% average, >70% exceptional*

2. **Gold Efficiency** — `Gold Earned / (Game Duration in Minutes × 450)`  
   *Why 450? Average expected gold/min for a non-fed laner.*  
   > 1.2 = hyper-carrying, <0.7 = severely behind

3. **Map Pressure Index** — Composite of:  
   - Turret damage dealt (weighted 0.3)  
   - Enemy jungle invades (vision score in enemy jungle, weighted 0.25)  
   - Roaming participation pre-14 min (weighted 0.25)  
   - Herald/Dragon presence (weighted 0.2)  
   *Normalized 0-100 scale*

4. **Survivability Quotient** — `(Deaths / Team Total Deaths)⁻¹ × (Damage Mitigated / Champion HP Pool Average)`  
   *Higher is better. A tank with many deaths but massive mitigation scores well.*

5. **Momentum Impact** — Weighted sum of:  
   - First Blood participation (+15)  
   - Triple+ kills (+10 each)  
   - Objective steals (+20)  
   - Shutdown collection (+5 per 500g bounty)  
   *Displayed as "Momentum Points" with visual thunderbolt gauge*

**Central Dial Display:** The pentagon's center shows a single number — **Performance Score** (0-100, weighted combination of the five metrics, adjusted for matchup difficulty).

**Example Fill:**  
Ahri, 34-min game, 12/3/9, 67% KP, 1.15 Gold Efficiency → Performance Score = 84 ("Elite")

**Corner Insight:** *"Your Kill Participation (67%) is in the top 12% of Ahri players this patch — but your Map Pressure Index (41) suggests you stayed in lane too long post-14."*

---

### ZONE 3: TIMELINE NARRATIVE — The Match as a Story Arc

**Format:** Horizontal scrollable timeline (desktop) or vertical-stacked (mobile). 500px tall, with three parallel tracks.

**Track A — Momentum Wave (Primary Visual):**  
A continuous bezier curve representing **Gold Differential Delta** (your champion's gold vs. lane opponent, with +500g spikes for objectives). Color gradient: red (losing) → gray (even) → gold (winning).  
*Annotated peaks/troughs with small icons: 💀 for death, 🏆 for kill, 🔥 for objective secured.*

**Track B — Event Strip (Icons only):**  
Icons plotted at game minutes:  
- 🗡️ Champion kill (size scales with multikill: small for solo, large for pentakill)  
- 🏰 Turret destroyed (your involvement = colored border)  
- 🐉 Dragon/Elder/Herald/Baron (half-opacity if you were absent)  
- ⏱️ Power Spike Windows (shaded vertical bands: e.g., "Lost Chapter (6:00)" → "Liandry's (14:30)")

**Track C — State Annotation (Text snippets, auto-generated):**  
Key turning points with natural language:  
- *"8:14 — First Blood (solo kill on enemy Zed, 400g bounty collected)"*  
- *"17:45 — Lost teamfight at dragon. Your charm missed priority target."*  
- *"28:30 — Quadra kill! Turned baron fight from 3v5. Game flipped."*

**Bottom of Timeline — Sentiment Arc:**  
A thin, color-coded band tracking "win probability impact" from your perspective (calculated via 10,000 Monte Carlo simulations per game state). Green spikes = your action increased win chance by >5%, red dips = error.

**Insight Callout:** *"Your death at 19:22 dropped win probability by 18% — the largest negative swing of the match. Zed was unseen on minimap for 11 seconds prior."*

---

### ZONE 4: ADVANCED PERFORMANCE MATRIX

**Four quadrants, each 200×200px, arranged 2×2.**

**Quadrant A — Gold & XP Efficiency (Barrels & Bursts)**  

- **Gold per Minute (GPM) vs. Game Average:** Side-by-side bar: Your GPM (e.g., 428) vs. Role Average (e.g., 395) vs. Global Average (380).  
- **Effective Gold Earned:** `Total Gold - (Gold spent on items sold - Gold lost on death timers × 0.3)`  
  *Reasoning: A 60-second death at 35 min loses ~400g in pressure value.*  
- **XP Gap Over Time:** Line chart showing level differential vs. lane opponent. Annotate level 6, 11, 16 breakpoints.

**Quadrant B — Combat Efficiency Ratios**  

- **Damage per Gold Spent:** `Total Damage to Champions / Total Gold Earned`  
  *High = gold-efficient fighter, Low = item-reliant scaler*  
- **Kill Conversion Rate:** `(Kills + Assists) / (Team Fights Participated)`  
  *Above 0.8 = clean-up master, Below 0.4 = damage but no finish*  
- **Effective Tankiness:** `(Damage Taken + Damage Mitigated) / Deaths`  
  *Divide by 1000 for "tank points per death" — higher means you absorbed resources without feeding.*  
- **Crowd Control Score per Minute:** Standard metric, but normalized against champion average (e.g., Ahri's 0.35 cc/min is low vs Leona's 2.1).

**Quadrant C — Objective Control & Roaming**  

- **Vision Denial Ratio:** `(Control Wards Placed + Sweeper Clears) / (Enemy Wards Placed in Your Jungle)`  
  *Values >1 = you out-visioned.*  
- **Objective Participation Heatmap:** Mini-map replica with circles scaled to your proximity to each objective (dragon/baron/turret) 10s before it died.  
- **Roaming Score:** `(Roaming Kills + Assists) / (Game Minutes × 0.1)` with a penalty for lost plates during roam.

**Quadrant D — The "Clutch Factor" (Situational Aggregator)**  

- **Low-Health Efficiency:** Damage dealt while below 30% HP (as percentage of total damage). High = risk-taker.  
- **Comeback Contribution:** Gold earned after your team was down 4k+ gold.  
- **Shutdown Precision:** Percentage of enemy shutdowns (500g+ bounties) that you personally collected.  
- **Late-Game Activity Index:** K+P + damage share in last 8 minutes of game.

**Example Insight:** *"Your Damage per Gold (6.2) is excellent, but your Kill Conversion (0.33) is bottom 15% — you're poking but not finishing. Consider holding abilities for execution thresholds."*

---

### ZONE 5: POSITIONING & VISION INTELLIGENCE — Theoretical CV Heatmap

**This zone showcases a speculative but feasible computer vision application.**

**Visual Centerpiece:** A 600×600px Summoner's Rift map (simplified, lane/brush outlines only) overlaid with a **smooth gradient heatmap** showing your champion's position density across the match.

**Heatmap Color Scale:**  
- Deep Blue (0-2% of time) → Cyan → Yellow → Red (10%+ of time)  
- White hotspots = >15% of time (e.g., mid lane post-15 min)

**Three Sub-Layers (toggleable via mock UI buttons):**

1. **Laning Phase (0-14 min):** Hotspots show trading stance (e.g., Ahri favors river-side of mid lane, not brush-side — vulnerable to ganks).  
2. **Mid Game (14-25 min):** Show rotation patterns — did you path through enemy jungle or take safe river?  
3. **Late Game (25+ min):** Clustering around Baron/Dragon pits, sidelane pressure zones.

**Theoretical CV-Derived Metrics (displayed as cards around map):**

| Metric | Description | Insight Example |
|--------|-------------|------------------|
| **Brush Dwelling Time** | % of game spent in fog of war (unseen by enemies) | "You spent 18% of game in brush — 6% above Ahri average. Ambush-heavy playstyle." |
| **Proximity to Walls** | Avg distance to terrain (pixels) during teamfights | "Teamfight positioning: 72px from walls (safe), but no terrain used for charm angles." |
| **Mouse Click Dispersion** | (If CV could track cursor) — chaotic vs. deliberate movement | "Your click pattern suggests indecision in river skirmishes (high dispersion pre-engage)." |
| **Vision Line Crossings** | Number of times you moved from lit to unlit map areas | "You entered unwarded jungle 23 times — 11 of those preceded a death." |

**Ward Placement Intelligence:**  
- Small dots for each ward you placed (green = allied vision, red = swept/enemy cleared).  
- Lines connecting wards that created "vision chains" (continuous sightlines).  
- **Shadow Score:** `(Wards that revealed an enemy) / (Total Wards Placed)` — Higher = placement quality.

**Insight Callout:** *"Your heatmap shows a 'death valley' at the river pixel near Raptor camp — you lingered there 9% of mid-game, but died there twice. Adjust your reset pathing."*

---

### ZONE 6: BUILD & ABILITY BREAKDOWN — Efficiency Science

**Item Path Timeline (Horizontal Gantt-style):**

- Each item purchase shown as a bar spanning the minutes it was owned.  
- **Spike Detection:** Shaded vertical bands where your damage output (smoothed) increased >30% within 60 seconds of item completion.  
- **Mythic vs. Mythic Comparison:** Ghost line showing "expected damage" if you'd built a different mythic (based on 10,000 games of same matchup).

**Ability Efficiency Rating (AER) — Novel Statistic:**

For each ability (Q, W, E, R), compute:  
`(Damage Dealt + CC Duration × 200 + Utility Value) / (Mana Cost × Times Cast + Cooldown Seconds × 0.5)`

Normalized 0-100 scale per champion.

*Example: Ahri's Charm (E):*  
Land rate 68% → AER 82 (Excellent).  
Her Orb (Q): AER 54 (Poor — 23% of casts missed return damage).

**Advanced Resource Management:**  
- **Mana Waste Index:** `(Mana spent while at 100% mana) / (Total mana spent)` — Higher = inefficient early poking.  
- **Cooldown Utilization:** `(Ability casts / (Game Seconds / Avg Cooldown))` — Above 0.8 = spell rotation mastery.

**Build Adaptation Score:**  
- Compares your item order to "optimal" vs. enemy team composition (armor/MR needed, healing reduction necessity).  
- Example: *"You bought Oblivion Orb (healing reduction) 9 minutes after enemy Soraka hit level 11 — too slow (-12% effectiveness)."*

---

### ZONE 7: COMPARATIVE & PREDICTIVE INSIGHTS

**Percentile Rankings (Five Pillars):**

| Metric | Your Value | Rank (vs. same champion, same rank, last 30 days) |
|--------|------------|---------------------------------------------------|
| Early Game (0-14) CSD@10 | +8 | 73rd percentile |
| Vision Score/min | 1.4 | 42nd percentile |
| Damage Share (team %) | 29% | 81st percentile |
| Deaths per Game | 3.2 | 65th percentile (fewer deaths = better) |
| Objective Damage | 4800 | 38th percentile |

**"Shadow Match" — Predictive Mirror:**

- Algorithm finds the most statistically similar game from pro play or high-elo (same champion, similar matchup, similar game state at 15 min).  
- Displays: *"Your game mirrors Faker's Ahri vs. Zed (LCK Summer 2024) at 15 min (even gold, down 1 kill). Faker won with 78% probability — his key difference: 3 extra roams bot pre-20."*

**Post-Game Improvement Prompt (Actionable):**

Generative text based on your low-performing metrics:  
*"Work on: Mid-game vision. Your vision score drops 40% between 15-25 min. Next game, buy a Control Ward on every recall after 12 minutes — aim for 1.8 vision score/min."*

**Final Emotional Signature (The "Parting Shot"):**

A single-sentence poetic summary generated from match data:  
*"A patient hunter who struck at the right moments, but left too many kills on the table. Your team's victory was built on your early pressure, not your late-game execution."*

---

## IV. THEORETICAL STATISTICAL APPLICATIONS (Embedded Concepts)

These are not "how to build" but conceptual frameworks that could generate the insights above.

### A. Computer Vision for Positioning Heatmaps (As seen in Zone 5)

- **Method:** Post-process replay files with object detection models (YOLO or custom CNN) to track champion bounding boxes at 2 fps.  
- **Outputs:**  
  - Position density (Gaussian kernel density estimation, bandwidth = 300 units)  
  - Teamfight alignment vectors (direction your champion faced relative to enemy team centroid)  
  - "Panic score" — variance in movement speed during 3 seconds after first enemy appearance in FoW  
- **Validation:** Compare CV-derived positions to Riot's official API (when available) — expected error <15 units.

### B. Win Probability Impact Model (Timeline Zone)

- **Framework:** Gradient-boosted trees (XGBoost) trained on 10M solo queue games.  
  Features: gold diff, XP diff, tower diff, dragon/herald/baron count, champion composition synergy, death timers.  
- **Individual Action Attribution:** Counterfactual inference — "If this champion had died 5 seconds later, would win prob change?"  
- **Output:** Per-player "Responsibility Score" for win condition swings.

### C. Role-Positional Normalization (Five-Ring Dial)

- **Challenge:** A 10/0/5 ADC vs. 10/0/5 Support have vastly different expectations.  
- **Solution:** Cluster players into 6 role-based archetypes (using PCA on 20 match stats) then compute z-scores within each cluster.  
- **Dynamic Benchmarks:** Percentiles shift weekly based on patch changes (e.g., enchanter supports get lower damage expectations after durability patch).

### D. Natural Language Generation for Event Annotations (Timeline Track C)

- **Template-based + Variational Autoencoder (VAE) for style:**  
  - Template: `{timestamp} — {event_type} {qualifier} {outcome} {strategic_comment}`  
  - VAE trained on 100k manually annotated LCS broadcast transcripts to inject natural cadence.  
- **Example generation:** *"19:45 — Overstay at enemy raptors. No vision of Lee Sin. Death costs baron."* vs. *"19:45 — Aggressive jungle invade punished by unseen Lee Sin; baron conceded."*

### E. Build Adaptation Scoring (Item Zone)

- **Reinforcement Learning simulation:**  
  - State = gamestate at each recall (gold, enemy items, team comps)  
  - Action = item purchase  
  - Reward = win probability increase over next 5 minutes (calculated via oracle model)  
- **Player's Build Adaptation Score =** `(Actual Reward - Average Reward of All Possible Items at that State)`  
  - Positive = you chose well, Negative = suboptimal purchase.

---

## V. DATA SOURCES & PRIVACY NOTES (Informational Footer)

**Data Sources (theoretical but plausible):**  
- Riot Games API (match timeline, participant frames, events) — official  
- Replay file parsing (for CV heatmaps) — requires local client access  
- Opt-in performance database (for percentile ranks) — anonymized

**Privacy Guardrails:**  
- Heatmaps show only your champion, never enemy positions retroactively (unless de-identified).  
- "Shadow Match" comparisons use aggregated pro data, never another player's specific game.  
- All predictive insights are local (your device) or opt-in cloud.

---

## VI. ACCESSIBILITY & LOCALIZATION

- **Colorblind Modes:** Tritanopia/Protanopia palettes for heatmaps and momentum curves.  
- **Text-to-Speech Ready:** ARIA labels on all data visualizations.  
- **Localization:** Numbers, timestamps, and "Shadow Match" narratives translated to 14 languages (contextual numeral formatting — e.g., 1.234,56 for EU).

---

## VII. FINAL POLISH — The "Wow" Factors

- **Micro-interactions:** Hover over any stat → tooltip explains calculation and shows "pro tip" improvement.  
- **Shareable "Highlight Strip":** Click generates a 1200×630px summary card for Twitter/Discord with top 3 stats and champion portrait.  
- **Replay Sync (optional):** If viewed on client, clicking a timeline event jumps replay to that moment.  
- **Dynamic Titles:** The header's subtitle changes based on performance:  
  - *"The Unkillable Demon King"* (0 deaths, 15+ kills)  
  - *"The Ghost of the Rift"* (high kill participation, low damage share — cleanup artist)  
  - *"The Silent Anchor"* (high vision, low kills, high win prob impact — support main's pride)

---

## VIII. EXAMPLE COMPLETED GRAPHIC MOCK DESCRIPTION

*For an Ahri player in a 34-minute win:*  
- Header: Victory banner, "Ahri • The Nine-Tailed Fox", Summoner "VorpalFox"  
- Five-Ring Dial: Performance Score 84 (Elite). Weakness shown in Map Pressure (41).  
- Timeline: Momentum curve dips at 19:22 (death) then rockets after 28:30 quadra.  
- Heatmap: Red hotspot mid-lane, cold sidelanes — "You never left mid after 20 min."  
- Shadow Match: "Similar to Faker's 2024 game — but he roamed bot twice more."  
- Parting Shot: *"A fox who found her teeth too late, but when she did, the game ended."*

---

**End of Specification.** This graphic transforms League's numerical exhaust into a narrative, a learning tool, and a piece of art — one champion, one match, one unforgettable story.