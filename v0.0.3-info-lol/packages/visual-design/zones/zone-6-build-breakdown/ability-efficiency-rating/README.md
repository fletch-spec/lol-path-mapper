# Ability Efficiency Rating (AER): Detailed Specifications

## Purpose

Provide a single, normalized metric for each ability (Q, W, E, R) that captures how effectively that ability was used in the match.

## Formula

```
AER = (Damage Dealt + CC Duration × 200 + Utility Value) / 
      (Mana Cost × Times Cast + Cooldown Seconds × 0.5)

Scale: 0-100 (normalized per champion baseline)
```

## Components Explained

### Numerator (Impact)

#### Damage Dealt
- **Definition:** Total damage this ability dealt to champions (not minions)
- **Scaling:** Normalized by champion's average ability damage at this level/items

#### Crowd Control Duration × 200
- **Definition:** Total seconds of CC applied × 200 multiplier (utility value proxy)
- **Why 200?:** One second of CC is roughly equivalent to 200 damage in terms of fight impact
- **Examples:**
  - Charm 0.75s: 0.75 × 200 = 150 utility value
  - Stun 1.5s: 1.5 × 200 = 300 utility value
  - Slow 50% for 2s: Partial credit, ~100 utility value

#### Utility Value
- **Definition:** Additional value from non-damage, non-CC effects
  - Healing provided: count as utility
  - Shields provided: count as utility
  - Movement speed buffs: count as utility
  - Debuffs on enemies: count as negative utility (damage reduction, tenacity)
- **Calculation:** Scaled proportionally; 1 point of healing = 1 damage equivalent

### Denominator (Resource Cost)

#### Mana Cost × Times Cast
- **Definition:** Total mana spent on this ability
- **Meaning:** Higher mana cost penalizes inefficient casting
- **Example:** 50 mana ability cast 35 times = 1,750 mana cost

#### Cooldown Seconds × 0.5
- **Definition:** Cooldown duration multiplied by 0.5 (availability penalty)
- **Meaning:** Longer cooldown abilities are expected to do more per cast (ult > Q)
- **Why 0.5 multiplier?:** Cooldown is a soft constraint, not hard like mana; 0.5 weight reflects this

## Per-Champion Scaling

**Baseline AER:** Each champion has a baseline AER for each ability, calculated from 10,000 average-player games

**Normalization:** Individual game AER is compared to baseline, then scaled 0-100

- AER = 50: Average for your champion
- AER = 80: Top 15% of players with this ability
- AER = 30: Bottom 20% of players with this ability

**Updates:** Baselines are recalculated weekly (post-patch) to account for balance changes

## Edge Cases & Special Handling

### Passive Abilities
- **Not included** in AER (no active cast)
- **Exception:** If passive is auto-triggered (e.g., Ashe's passive crit), credit utility value to nearest active ability

### Empowered Casts
- **Example:** Renekton's Fury stun vs. normal E
- **Handling:** Track separately; empowered casts are counted as distinct "casts" with different damage/CC

### Off-Target Casts
- **Definition:** Ability cast but missed (e.g., skill shot that missed)
- **Handling:** 0 damage, 0 CC, 0 utility; mana cost still counts (penalizes missing)
- **Insight:** High miss rate = low AER for that ability

### Overkill Damage
- **Definition:** Damage dealt after target is dead
- **Handling:** Does not count toward damage (realistic damage calculation)

## Display in Zone 6

**Visual:** Four bars (Q, W, E, R) each showing:
- **AER value (0-100)** in large text
- **Percentile ranking** (vs. same champion, same rank, last 30 days)
- **Land/hit rate** (if applicable for skill shots)
- **Interpretation label:** Excellent / Good / Average / Poor

**Example:**
```
Q (Orb):        AER 54 [34th percentile] — Hit Rate 77%
W (Flame):      AER 71 [62nd percentile] — 23 hits
E (Charm):      AER 82 [78th percentile] — Land Rate 68%
R (Spirit Rush): AER 68 [59th percentile] — 6 casts
```

## Actionable Insights Examples

### High AER, High Land Rate
*"Your Charm (AER 82, 68% land rate) is elite. You're landing charms consistently and they're doing damage/CC. This is your win condition ability — lean on it."*

### Low AER, Low Land Rate
*"Your Orb (AER 54, 77% hit rate) is underperforming. Even with decent accuracy, you're missing 23% of returns or dealing minimal damage. Practice the Q→return combo; aim for 85%+ accuracy."*

### High Damage, Low Land Rate
*"Your Q damage is high (11.2k total), but 77% hit rate means 2,600 damage was overkill. Lower hit rate isn't the issue; it's return-shot frequency. Hold Q longer for guaranteed returns."*

### Passive Ability
*"Ahri gains passive movement speed during combat. This generated ~3k 'utility value' equivalent through positioning advantage — correctly reflected in team fight outcomes."*

## Limitations & Disclaimers

- **AER does not account for cooldown remaining:** A 0-cooldown ability cast is more valuable than a 12-second cooldown ability cast
- **AER does not account for game state:** Casting ulti as engage vs. disengage has different value
- **AER is champion-specific:** Comparing AER across champions is meaningless (different scaling, costs, cooldowns)
- **AER assumes standard builds:** If you built non-standard items (AD vs AP Ahri), scaling may be off

## Boundaries

**Assumes:**
- Damage, CC duration, mana cost, and cooldown data are accurate from API
- Champion baselines are updated weekly and accurate
- Ability hit/miss detection is reliable (skill shots tracked)

**Constraints:**
- AER formula must be consistent across all champions (same numerator/denominator structure)
- Utility values must be bounded (-100 to +100) to prevent extreme scores
- Percentile rankings require comparison pool of at least 100 games (ranked games)
