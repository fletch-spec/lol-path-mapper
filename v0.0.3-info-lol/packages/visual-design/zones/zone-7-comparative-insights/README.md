# Zone 7 – Comparative & Predictive Insights: Learning & Improvement

## Purpose

Contextualize the match within broader player history and pro-level play. Provide actionable improvements, psychological closure (celebration), and next-game guidance.

## Visual 1: Percentile Rankings (Five Pillars)

**Table Format:** 5 rows, one for each pillar

| Metric | Your Value | Rank | Interpretation |
|--------|-----------|------|-----------------|
| Early Game (0-14) CSD@10 | +8 | 73rd percentile | Above average early CS. You gained gold advantage early. |
| Vision Score/min | 1.4 | 42nd percentile | Below average vision. Bot lane grouped mid; you warded less. |
| Damage Share (team %) | 29% | 81st percentile | Excellent damage output. You were primary threat. |
| Deaths per Game | 3.2 | 65th percentile | Above average (fewer deaths = better) | Low deaths, strong positioning. |
| Objective Damage | 4800 | 38th percentile | Below average objective focus. Focus on towers/dragons next game. |

**Comparison Pool:** Same champion, same rank (e.g., Diamond III), last 30 days

**Interpretation:**
- 80th+ percentile: Strength; lean on this in future games
- 40-80th percentile: Average; opportunities to improve
- <40th percentile: Weakness; targeted training needed

## Visual 2: "Shadow Match" – Predictive Mirror

**Concept:** Algorithm finds the most statistically similar game from pro play or high-elo (same champion, similar matchup, similar game state at 15 min).

**Example Output:**

*"Your game mirrors **Faker's Ahri vs. Zed** (LCK Summer 2024) at 15 min:*
- *Both: Even gold (within 200g)*
- *Both: Down 1 kill (enemy 1-0)*
- *Both: Similar itemization (Liandry's path)*

*Faker won with **78% probability** — his key differences:*
1. *3 extra roams bot pre-20 min (vs. your 0)*
2. *2% higher vision score (1.8 vs. your 1.4)*
3. *Charm land rate 72% (vs. your 68%)*

*Projection: If you matched Faker's roaming, your win prob would've increased to 71% (actual 58%). Next game: roam bot more aggressively 15-20 min window."*

**Data Source:** 
- Pro play games (LEC, LCS, LCK, etc.) for high-level examples
- High-elo soloQ (10k+ LP) for more relatable matches

**Matching Criteria:**
1. Same champion
2. Same vs. enemy champion (or similar type)
3. Similar gold differential at 15 min (±500g)
4. Similar kill score at 15 min (±1 kill)
5. Similar itemization direction

## Visual 3: Post-Game Improvement Prompt (Actionable)

**Generation:** Procedurally generated based on low-performing metrics

**Example 1 (Vision):**

*"Work on: **Mid-game vision**. Your vision score drops 40% between 15-25 min. Next game, buy a **Control Ward on every recall after 12 minutes** — aim for **1.8 vision score/min** (you averaged 1.4 this game). This 0.4 point gain = +2% average win rate over 100 games."*

**Example 2 (Objective Damage):**

*"Work on: **Objective pressure**. You dealt only 4.8k damage to objectives (38th percentile). When team groups, **auto-attack turrets** during teamfights (not just champions). A 3k damage increase would move you to 50th percentile — worth practicing."*

**Example 3 (Roaming):**

*"Work on: **Roaming impact**. Your roaming kills+assists = 2 in a 34-min game (0.06 per minute). Faker averages 0.18. Next game: **Plan 2-3 roams per 10 minutes** (0.3 roam windows). Target: 4-6 roaming k/a for a 34-min game (+100% improvement)."*

**Tone:** Encouraging but honest; avoid sugar-coating weaknesses

## Visual 4: Final Emotional Signature (The "Parting Shot")

**Format:** Single-sentence poetic summary generated from match data

**Examples:**

- *"A patient hunter who struck at the right moments, but left too many kills on the table. Your team's victory was built on your early pressure, not your late-game execution."*
- *"The unkillable demon king — 3 deaths in 34 minutes, elite positioning, and a heatmap that shows calculated, not reckless, aggression."*
- *"A ghost on the map. Your presence was felt globally through warding and rotations, but your damage says you stayed safe. Calculated strategy worked, but aggression would've been rewarding."*
- *"Victory stolen from defeat. Down 4k gold at 22 minutes, you positioned yourself for a clutch 4v5 teamfight and won a game that felt lost."*

**Generation:** Template-based + stylistic variation from language model fine-tuned on LCS broadcast commentary (see [Natural Language Generation](../../statistics-and-algorithms/natural-language-generation/README.md) for details)

**Purpose:** Memorable, emotionally resonant closing that synthesizes the game's narrative

## Accessibility

- **Table:** Clear column headers, numeric percentiles, text interpretations
- **Shadow Match:** Narrative text, readable comparisons, action items
- **Parting Shot:** Large, readable typography; poetic but unambiguous

## Interaction & Sharing

- **Click on Shadow Match:** Jump to replay moment (if in-client) or display side-by-side stats overlay
- **Copy Parting Shot:** Share on social media or save to player profile
- **Print Zone 7:** "Learning card" suitable for study/reflection

## Boundaries

**Assumes:**
- Percentile rankings are available from performance database (anonymized)
- Pro play/high-elo game database is available and searchable
- NLG model can generate contextually accurate improvement prompts
- Replay integration is available (optional, for click-through)

**Constraints:**
- Shadow Match must use only aggregated pro data (never another player's specific stats)
- Improvement prompts must be achievable in one or two areas (not 5 suggestions)
- Parting Shot must be non-condescending regardless of match outcome
