# Quadrant A – Gold & XP Efficiency: Barrels & Bursts

## Purpose

Measure how efficiently the champion acquired resources (gold and experience) relative to game time and role expectations.

## Metrics

### 1. Gold per Minute (GPM) vs. Role Average

**Display:** Side-by-side bars

- **Your GPM:** e.g., 428 gpm
- **Role Average:** e.g., 395 gpm (5th percentile for your role this patch)
- **Global Average:** e.g., 380 gpm (cross-role average)

**Interpretation:**
- Above role average: Efficient farming or high kill participation
- Below role average: Underfed, missed CS, or died too much (lost gold on timer)

### 2. Effective Gold Earned

**Definition:** `Total Gold Earned - (Gold Lost on Unfinished Items + Death Timer Gold Loss × 0.3)`

**Reasoning:** 
- Unfinished items represent capital inefficiency
- Death timers reduce your effective earning capacity
- The 0.3 multiplier reflects that losing 60 seconds at 35-min means ~400g lost in pressure value

**Example:**
- Total gold earned: 11,500
- Unfinished item value: -200
- Death timer loss (3 deaths × 60s each at avg game state): -180
- **Effective Gold:** 11,120

### 3. XP Gap Over Time

**Display:** Line chart showing level differential vs. lane opponent

**Annotated Breakpoints:**
- Level 6, 11, 16 (ultimate upgrades)
- Each level tick represents +400g in assumed power

**Interpretation:**
- Gap widens over time: You outleveled your opponent (farming or kill advantage)
- Gap narrows: Opponent caught up (roamed, grouped better)
- Gap reverses: Opponent now ahead (possible gank deaths or missed cs)

**Insight Examples:**
- *"You hit level 6 first (2:14 advantage) — first ultimate + pressure combo was important."*
- *"At 25 min, you were 2 levels behind despite even kills — bot lane grouped mid, you farmed alone."*

## Visual Hierarchy

1. **Gold per Minute bars** – Most important, largest visual
2. **XP Gap line chart** – Secondary detail
3. **Effective Gold callout** – Supporting calculation

## Accessibility

- **Color:** Bars use colorblind-safe green (above average) vs. red (below average)
- **Text:** All numbers labeled clearly; tooltips explain calculations

## Boundaries

**Assumes:**
- Gold earned and death timers are accurate from match timeline
- Role averages are current for the patch and rank
- Level times are precise from API

**Constraints:**
- All metrics must be normalized to "per minute" for game-duration independence
- XP gap must be calculated vs. specific lane opponent (mid vs. mid, not mid vs. bot)
