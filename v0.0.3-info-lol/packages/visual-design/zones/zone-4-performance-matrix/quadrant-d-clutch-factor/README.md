# Quadrant D – The Clutch Factor: Game-Changing Moments

## Purpose

Highlight the champion's ability to deliver impact in high-pressure, game-deciding scenarios: low-health teamfights, comeback windows, and shutdowns.

## Metrics

### 1. Low-Health Efficiency

**Definition:** Damage dealt while below 30% HP (as percentage of total damage)

**Interpretation:**
- High (>15%): Risk-taker, aggressive fighter; continues dealing damage even when vulnerable
- Medium (5-15%): Balanced approach; some low-health fights but not reckless
- Low (<5%): Conservative; disengages when low on health (safe playstyle)

**Example:**
- Total damage: 71,400
- Damage dealt while <30% HP: 11,800
- **Ratio:** 11,800 / 71,400 = 16.5%

**Interpretation:** *"16.5% of your damage came from low-health scenarios — you're a risk-taker who fights even when vulnerable. Works well for burst champs; risky for squishies."*

### 2. Comeback Contribution

**Definition:** Gold earned after your team was down 4000+ gold

**Reasoning:** Teams down 4k+ gold are losing; gold earned in these moments directly impacts comeback potential

**Example:**
- Team was down 4k+ gold for 8 minutes (16:00 to 24:00)
- During that window, you earned: 2,100 gold
- **Comeback contribution:** 2,100 gold

**Insight:** *"While your team was behind, you earned 2.1k gold — strong personal economy during adversity. This is why you won despite falling behind."*

### 3. Shutdown Precision

**Definition:** Percentage of enemy shutdowns (500g+ bounties) that you personally collected

**Interpretation:**
- High (>60%): You're the primary threat; enemies focus you first
- Medium (20-60%): You share shutdown securing with teammates
- Low (<20%): Teammates or roaming champions get shutdowns you should've taken

**Example:**
- Enemy shutdowns available in game: 6 (6 × 500g enemies eliminated)
- Shutdowns you collected: 4
- **Precision:** 4 / 6 = 66.7%

**Insight:** *"You collected 66% of available shutdowns — excellent threat priority. Enemies feared you most and bounties reflected that."*

### 4. Late-Game Activity Index

**Definition:** (Kills + Assists + Damage Share) in final 8 minutes of game

**Interpretation:**
- High: You remained impactful even as game ended
- Low: Sidelined or eliminated before finale; teammates closed out

**Example:**
- Last 8 minutes (26:30 to 34:21):
  - Kills + Assists: 5
  - Damage share (your damage as % of team): 26%
- **Index:** High activity

**Insight:** *"You stayed relevant until game end (5 k/a, 26% damage share in final 8 min) — clutch performer."*

## Visual Representation

**Display:** 
- 4 numerical metrics, each with color-coded context (green = strong, red = weak)
- Supporting interpretation text
- Optional sparkline showing low-health damage over time

## Accessibility

- **Color:** Green/red with text labels for clarity
- **Calculation:** Tooltips explain each metric

## Boundaries

**Assumes:**
- Game timestamps and gold values are accurate
- Low-health determination is precise (<30% HP, not approximation)
- Shutdown detection is accurate from API

**Constraints:**
- "Low-health efficiency" should only count actual damage dealt, not abilities cast (which miss)
- "Comeback contribution" needs clear definition of "down 4k+" — must be time-windowed
- Shutdown precision only applies if game had 2+ shutdowns (avoid division by zero)
