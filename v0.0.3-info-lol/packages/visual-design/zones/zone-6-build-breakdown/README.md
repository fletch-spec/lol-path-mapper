# Zone 6 – Build & Ability Breakdown: Item Efficiency & Ability Usage

## Purpose

Display the champion's itemization path, identify power spike windows, and evaluate ability usage efficiency through a novel Ability Efficiency Rating (AER) system.

## Visual 1: Item Path Timeline (Gantt-Style)

**Format:** Horizontal timeline showing each item as a bar spanning minutes it was owned

**Visual Elements:**
- **Item icons:** Displayed left-to-right chronologically
- **Bar length:** Duration from purchase to sell/consumption
- **Shading:** Color-coded by item type (damage, defensive, utility)
- **Spike bands:** Vertical shaded areas (20-30 min wide) marking power spikes

## Power Spike Detection

**Calculation:** Smoothed damage output; track when damage increases >30% within 60 seconds of item completion

**Visual:** Vertical shaded bands labeled with item name and time

**Example:**
- 6:00 — *"Lost Chapter"* (light blue band) — Damage +15% (mana sustain spike)
- 14:30 — *"Liandry's"* (red band) — Damage +32% (mythic spike)
- 22:00 — *"Deathcap"* (purple band) — Damage +18% (scaling spike)

**Insight:** *"Your first power spike came early (6:00 Lost Chapter vs. typical 7:30). This pressure advantage was critical."*

## Mythic Comparison

**Display:** Ghost line showing expected damage if you'd built a different mythic (based on 10,000 games of same matchup)

**Example:**
- Actual mythic: Liandry's (14:30) → damage curve shown
- Alternative: Luden's tempo (14:30) → ghost curve shown in translucent color

**Comparison Insight:** *"Building Liandry's over Luden's gained +8% damage by 25min (due to flat pen + burn vs. burst), validating your choice."*

## Visual 2: Ability Efficiency Rating (AER)

**Novel Statistic** designed to measure how effectively each ability was used

### AER Formula

For each ability (Q, W, E, R):

```
AER = (Damage Dealt + CC Duration × 200 + Utility Value) / (Mana Cost × Times Cast + Cooldown Seconds × 0.5)
```

**Normalized 0-100 scale** per champion

**Components:**

| Component | Explanation |
|-----------|------------|
| Damage Dealt | Total damage this ability dealt to champions |
| CC Duration | Seconds of crowd control × 200 (represents utility value) |
| Utility Value | Healing, shields, or movement (enemy slows count as negative) |
| Mana Cost | Mana spent per cast × number of casts |
| Cooldown Seconds | Cooldown duration × 0.5 (time-availability penalty) |

### Example: Ahri Charm (E)

- **Damage Dealt:** 8,400 (primary damage)
- **CC Duration:** 1.5 seconds average per land × 35 casts × 0.7 land rate = 36.75 CC seconds
- **Utility Value:** 0 (charm has no other utility)
- **Mana Cost:** 50 mana × 35 casts = 1,750
- **Cooldown:** 12 seconds × 0.5 = 6

**AER = (8,400 + 36.75 × 200 + 0) / (1,750 + 6) = (8,400 + 7,350) / 1,756 = 8.98 → 82 (0-100 scale)**

**Interpretation:** AER 82 (Excellent) — charm was effective; 68% land rate is strong.

### Example: Ahri Orb (Q)

- **Damage Dealt:** 11,200 (primary + return)
- **CC Duration:** 0 (no CC)
- **Utility Value:** 0
- **Mana Cost:** 60 mana × 40 casts = 2,400
- **Cooldown:** 7 seconds × 0.5 = 3.5

**AER = (11,200) / (2,400 + 3.5) = 4.65 → 54 (0-100 scale)**

**Interpretation:** AER 54 (Poor-Average) — orb did damage but missed frequently. 23% of casts missed return damage.

**Actionable Insight:** *"Your Charm (AER 82) is excellent — land rate 68%. But Orb (AER 54) is underperforming — 23% of casts missed. Focus on hitting both return shots for +5 AER."*

## Advanced Resource Management

### 1. Mana Waste Index

**Definition:** `(Mana spent while at 100% mana) / (Total mana spent)`

**Interpretation:**
- High (>30%): Inefficient early-game poking; spending mana unnecessarily at full
- Medium (10-30%): Typical; some waste but mostly intentional poke
- Low (<10%): Perfect mana management; ramping up spend as fights escalate

**Example:** *"Mana Waste Index: 18% — reasonable. Some early laning waste (common for mages), but tightened up mid-game."*

### 2. Cooldown Utilization

**Definition:** `(Ability casts) / (Game Seconds / Avg Cooldown)`

**Interpretation:**
- Above 0.8: Spell rotation mastery; using abilities every cooldown
- 0.4-0.8: Typical playstyle; not spam-casting
- Below 0.4: Conservative; holding abilities for specific moments

**Example:** *"Cooldown Utilization (0.76) — near mastery level. You're cycling abilities efficiently without spam-casting."*

## Visual 3: Build Adaptation Score

**Definition:** Compares your item order to "optimal" vs. enemy team composition

**Calculation:** For each recall decision, compare:
- Your purchase to "oracle optimal" (RL model trained on 10,000 high-elo games)
- Consider: armor/MR needed, healing reduction (anti-heal) necessity, spike timing

**Example Analysis:**
- *"You bought Oblivion Orb at 22:30, but enemy Soraka hit level 11 at 13:00 — too slow (-12% effectiveness). Earlier anti-heal would've crippled her heals for 30+ minutes."*
- *"Buying Void Staff at exactly 24:00 (2 minutes after Soraka got her 2nd MR item) was optimally timed — gained +8% effectiveness vs. standard timing."*

**Overall Build Adaptation Score:** 0-100, comparing your adaptation decisions to oracle model

## Accessibility

- **Color:** Item icons colored by type (damage = red, defense = blue, utility = purple)
- **Text:** All metrics labeled; AER definitions accessible via tooltips

## Boundaries

**Assumes:**
- Item purchase timestamps and ability cast counts are accurate from API
- Mana costs and cooldowns are accurate for patch
- Damage numbers are precise from match timeline

**Constraints:**
- AER must account for ability scaling (AP/AD ratios affect damage output)
- Mythic item comparisons should only compare to "reasonable" alternatives for the matchup
- Build Adaptation Score requires oracle model trained on high-elo games (not all elos)

---

## Sub-Package

See [Ability Efficiency Rating](ability-efficiency-rating/README.md) for detailed AER specifications and calculation edge cases.
