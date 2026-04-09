# Zone 1 – Header: Match Context & Champion Identity

## Purpose

Establish immediate context for the graphic by displaying the match outcome, the champion analyzed, and the player identity. The header is the narrative entry point.

## Layout Elements

### Match Result Banner
- **Full-width gradient:** Blue for win, red for loss
- **Typography:** "VICTORY" or "DEFEAT" in large, bold display type
- **Particle Effects:** 
  - Win: Falling laurels background
  - Loss: Shattered runes background
- **Subtle Animation:** Minimal motion to remain professional

### Game ID & Timestamp
- **Position:** Small text, bottom-left of banner
- **Format:** `#NA1-4872291032 • 2025-01-15 • 23:42 UTC`
- **Purpose:** Unique identifier for match archival and replay lookup

### Role & Lane Assignment
- **Display:** Icon + text (e.g., 🗡️ Mid Lane / 🛡️ Top / 🌟 Support)
- **Determination:** Algorithm-based via 2-minute positional data (not player-reported)
- **Rationale:** Position data is more reliable than player-selected roles

### Champion Name & Title
- **Typography:** Large, prominent display
- **Format:** `CHAMPION_NAME • THE_CHAMPION_TITLE`
- **Example:** *"AHRI • THE NINE-TAILED FOX"*
- **Source:** League's official champion roster data

### Player Summoner Name
- **Position:** Below champion name
- **Typography:** Subtle but readable
- **Purpose:** Personalizes the graphic to the player

### Patch & Game Mode
- **Format:** `Patch XX.X • Ranked Solo/Duo • MM:SS match duration`
- **Example:** `Patch 15.1 • Ranked Solo/Duo • 34:21 match duration`
- **Contextual Value:** Patch version affects balance; game mode affects expectations

## Strategic Insight Callout (Corner Ribbon)

A dynamic insight banner highlighting one key fact about this match's context:

- *"This match lasted 2:14 longer than your average [Champion] game — late-game scaling mattered."*
- *"Playing against [Enemy Champion] in [Role]? Your 8-game win rate here is 62% — better than your average."*
- *"Patch 15.1 buffed [Champion]. You gained 340 HP/lvl. Tankiness increased."*

These callouts are procedurally generated based on match data and historical player stats.

## Visual Hierarchy

1. **Result Banner (gradient + text)** – Dominates visual attention
2. **Champion Name & Title** – Second-level prominence
3. **Player Summoner Name** – Third level
4. **Role, Patch, Duration** – Supporting details
5. **Game ID & Timestamp** – Archival data (small)

## Accessibility

- **Color:** Gradient (blue/red) is distinguished by color *and* text ("VICTORY"/"DEFEAT")
- **Text-to-Speech:** All text labels have ARIA descriptions
- **Colorblind Mode:** Tritanopia/Protanopia safe gradients; text remains readable

## Boundaries

**Assumes:**
- Match data (ID, timestamp, role position, patch) is provided by data infrastructure
- Champion roster and titles are current with live game

**Constraints:**
- Must fit within 200px height
- Result banner must be immediately recognizable (blue ≠ red, VICTORY ≠ DEFEAT)
- Particle effects should not obscure or distract from text readability
