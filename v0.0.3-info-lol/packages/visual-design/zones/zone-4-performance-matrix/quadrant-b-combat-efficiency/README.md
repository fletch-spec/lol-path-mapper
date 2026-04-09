# Quadrant B – Combat Efficiency Ratios: Fighting Power

## Purpose

Analyze how effectively the champion converted resources (gold, abilities, durability) into combat impact.

## Metrics

### 1. Damage per Gold Spent

**Definition:** `Total Damage to Champions / Total Gold Earned`

**Interpretation:**
- High (>6): Gold-efficient fighter or burst champion; every gold does meaningful work
- Medium (4-6): Typical scaling champion; damage scales as intended
- Low (<4): Item-reliant scaler or low itemization impact (support, tank)

**Example:**
- Damage dealt: 71,400
- Gold earned: 11,500
- **Ratio:** 6.2 damage per gold

**Insight:** *"Your Damage per Gold (6.2) is excellent — you're getting maximum value from your purchases."*

### 2. Kill Conversion Rate

**Definition:** `(Kills + Assists) / (Team Fights Participated)`

**Interpretation:**
- Above 0.8: Clean-up master or high involvement in successful fights
- 0.4-0.8: Moderate participation; some fights were losses
- Below 0.4: Damage without finish; you're poke-heavy without kills/assists

**Example:**
- Kills: 12
- Assists: 9
- Fights participated: 32
- **Ratio:** (12 + 9) / 32 = 0.66

**Insight:** *"You're converting 66% of fights into kills/assists — solid but not exceptional. Look for opportunities to secure more kills after poking."*

### 3. Effective Tankiness

**Definition:** `(Damage Taken + Damage Mitigated) / Deaths` ÷ 1000 for "tank points per death"

**Interpretation:**
- High (>80): You absorbed massive resources before dying or didn't die much
- Medium (30-80): Typical for damage dealers
- Low (<30): Either very few deaths or minimal mitigation (squishy champion)

**Why This Matters:** A tank dying while soaking 150k damage is better than a carry dying while soaking 20k damage.

**Example:**
- Damage taken: 23,400
- Damage mitigated: 15,600
- Deaths: 3
- **Ratio:** (23,400 + 15,600) / 3 / 1000 = 13.0 tank points per death

**Insight:** *"For a mage, absorbing 39k durability-equivalent per death is strong — good positioning in fights."*

### 4. Crowd Control Score per Minute

**Definition:** Standard LoL API metric (Crowd Control Score), normalized against champion average

**Interpretation:**
- Ahri baseline: 0.35 cc/min (charm-dependent, hard to land)
- Leona baseline: 2.1 cc/min (multiple CC tools)
- Context: Your score is compared to your champion's expected baseline, not global

**Example:**
- Your CC/min: 0.31
- Ahri average: 0.35
- **Comparison:** "0.31 vs. 0.35 — slightly below average. Your charm land rate was 68%; with 5% better accuracy, expect +0.03 cc/min."

## Visual Representation

**Display:** 4 key numbers, each with:
- Your value
- Role/champion baseline
- Percentile ranking (vs. same champion, same rank, last 30 days)
- Interpretation color (green for good, red for poor relative to baseline)

## Accessibility

- **Color:** Green (above baseline) vs. red (below baseline), plus text labels
- **Calculation:** Each metric has a tooltip showing the formula

## Boundaries

**Assumes:**
- Damage dealt/taken and CC score are accurate from match timeline
- Champion baselines are current for the patch
- Deaths are accurately counted

**Constraints:**
- All metrics must be per-champion comparable (not cross-champion rankings)
- Mitigation should only count shields/damage reduction, not healing
