# Zone 3 – Timeline Narrative: The Match as a Story Arc

## Purpose

Transform the match timeline into a narrative story with three synchronized tracks that show momentum, key events, and strategic turning points. The timeline is the emotional and analytical core of the graphic.

## Format

- **Desktop:** Horizontal scrollable timeline
- **Mobile:** Vertical-stacked layout
- **Height:** 500px
- **Time Span:** 0 minutes to end of game

## Track A – Momentum Wave (Primary Visual)

**Visual:** Continuous bezier curve representing **Gold Differential Delta**

**Data:** Your champion's gold vs. lane opponent, with +500g spikes for objectives (kills, dragons, towers)

**Color Gradient:**
- Deep Red (losing, e.g., -3000g differential)
- Gray (even, ≈0g differential)
- Gold (winning, e.g., +3000g differential)

**Annotations on curve:**
- 💀 **Death:** Small icon, position at death time
- 🏆 **Kill:** Sized by kill type (small solo kill → large pentakill)
- 🔥 **Objective Secured:** Dragon, Herald, Baron, Tower with your involvement
- ⚡ **Power Spike:** Vertical shaded band marking item completion moments

**Insight Examples:**
- Curve rises sharply at 6:14 (First Blood kill)
- Curve dips at 19:22 (death, -400g tempo loss)
- Curve spikes at 28:30 (quadra kill objective)

## Track B – Event Strip (Icons Only)

**Format:** Icons plotted horizontally at match minutes

**Event Types:**

| Icon | Event | Details |
|------|-------|---------|
| 🗡️ | Champion Kill | Size scales: small=solo, medium=double, large=multi+ |
| 💀 | Your Death | Position at exact death minute |
| 🏰 | Turret Destroyed | Colored border: gold=you participated, gray=you were absent |
| 🐉 | Dragon/Elder/Herald/Baron | Half-opacity if you were not present (vision-less) |
| ⏱️ | Power Spike Window | Shaded vertical band: "Lost Chapter (6:00)" → "Liandry's (14:30)" |

**Interaction:** Hover over any icon reveals tooltip with details and moment timestamp

## Track C – State Annotation (Auto-Generated Text Snippets)

**Format:** Natural language callouts for key turning points

**Examples:**

- *"8:14 — First Blood (solo kill on enemy Zed, 400g bounty collected)"*
- *"17:45 — Lost teamfight at dragon. Your charm missed priority target."*
- *"28:30 — Quadra kill! Turned baron fight from 3v5. Game flipped."*
- *"19:22 — Aggressive invade punished by unseen Lee Sin; baron conceded."*

**Generation:** Template-based with stylistic variation from trained models (see [Natural Language Generation](../../statistics-and-algorithms/natural-language-generation/README.md))

**Triggers:** Major events (first blood, deaths, multi-kills, objective teamfights, power spikes)

## Bottom of Timeline – Sentiment Arc

**Format:** Thin, color-coded band tracking **win probability impact** from your perspective

**Calculation:** 10,000 Monte Carlo simulations per game state to model win probability (calculated via XGBoost trained on 10M games)

**Visual:**
- Green spikes: Your action increased win chance by >5%
- Red dips: Your action decreased win chance by >5% (typically deaths)
- Yellow/neutral: Minor swings or maintaining status quo

**Example Insight:**

*"Your death at 19:22 dropped win probability by 18% — the largest negative swing of the match. Zed was unseen on minimap for 11 seconds prior."*

## Visual Hierarchy

1. **Momentum Wave (Track A)** – Primary visual, dominant space
2. **Event Icons (Track B)** – Secondary, annotation layer
3. **Sentiment Arc (Bottom)** – Subtle background, shows win prob impacts
4. **Text Callouts (Track C)** – Supporting narrative, triggered on demand

## Time Phases

**Laning Phase (0-14 min):** Tight gold differentials, early kill importance  
**Mid Game (14-25 min):** More volatile, objective swaps drive curves  
**Late Game (25+ min):** Steeper curves as individual fights swing game decisively

## Accessibility

- **Color:** Momentum gradient is colorblind-safe (red ≠ green distinction is hue+brightness)
- **Text:** All annotations are readable; sentiment arc has text legend
- **Interactivity:** Hover reveals details; click (if in-client) jumps replay to moment

## Boundaries

**Assumes:**
- Statistics & Algorithms provides win probability calculations via Monte Carlo / gradient-boosted models
- NLG system generates natural, contextual event descriptions
- Match timeline and event data are accurate from API

**Constraints:**
- Timeline must span entire game duration (0 to final minute)
- Momentum curve must be smooth (bezier interpolation) despite discrete events
- All visible events must correspond to actual in-game events (no invented drama)
