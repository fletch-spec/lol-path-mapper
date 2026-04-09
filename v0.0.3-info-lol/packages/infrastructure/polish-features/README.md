# Polish Features: Micro-Interactions, Sharing & Integration

## Purpose

Polish features elevate the user experience from "functional" to "delightful." These are subtle interactions that make the graphic memorable and shareable.

## Micro-Interactions

### 1. Hover Tooltips

**Trigger:** User hovers over any metric or term

**Display:**
- Small popup near cursor
- Shows calculation formula (e.g., "Kill Participation = (Kills + Assists) / Team Total Kills")
- Includes "pro tip" improvement suggestion
- Disappears on mouse-out or timeout (5 seconds)

**Example:**

```
Hover over "Kill Participation 67%":

┌─────────────────────────────────┐
│ Kill Participation              │
├─────────────────────────────────┤
│ Formula: (Kills + Assists) /    │
│          Team Total Kills       │
│                                 │
│ Your KP: 67%                    │
│ Role Avg: 52%                   │
│                                 │
│ 💡 Pro Tip: High KP means you   │
│    participate in 2/3 of team   │
│    kills. Keep roaming to high  │
│    conflict areas.              │
└─────────────────────────────────┘
```

**Keyboard Access:** Tab to element + Enter reveals tooltip

**Animation:** Fade-in over 150ms (smooth but not slow)

### 2. Click-Through Insights

**Trigger:** Click on any major stat, zone, or narrative text

**Action:** Highlight or zoom-in on related context

**Example 1: Click "Performance Score 84"**
- Zoom to Five-Ring dial
- Highlight lowest metric (Map Pressure 41)
- Show callout: "Your Map Pressure is lowest metric. Consider roaming more mid-game."

**Example 2: Click timeline event "8:14 — First Blood"**
- Highlight momentum curve at 8:14
- Show gold differential swing (+400g)
- Suggest: "This early kill gave you momentum and jungle pressure."

**Example 3: Click percentile bar "Vision Score 42nd percentile"**
- Highlight vision-related metrics across zones
- Show progression: "You improved vision from match start to end"
- Suggest focus area: "Vision score drops 40% mid-game"

### 3. Dynamic Titles

**System:** Parting shot title changes based on performance archetype

**Examples:**

```
Performance Profile → Emotional Title

Elite (81+) with 0 deaths → "The Unkillable Demon King"
Elite (81+) with 1-2 deaths → "The Unstoppable Force"
Good (61-80) with high KP → "The Teamfight Anchor"
Good (61-80) with high roaming → "The Versatile Roamer"
Average (41-60) with high vision → "The Silent Sentinel"
Average (41-60) with early game lead → "The Quick Striker"
Below Avg (21-40) with comeback → "The Scrappy Underdog"
Struggling (0-20) but tied → "The Undervalued Asset"
```

**Calculation:** Based on top 2-3 performance characteristics

**Tone:** Positive even for low scores (celebratory, not demoralizing)

## Shareable Content

### 1. Highlight Strip

**Trigger:** "Share" button in Zone 7 (Comparative Insights)

**Output:** 1200×630px summary card optimized for Twitter/Discord

**Content:**
- Champion portrait + name
- Top 3 stats (e.g., "Performance: 84", "Damage: 29%", "KP: 67%")
- Emotional title ("The Unkillable Demon King")
- Match result (VICTORY/DEFEAT)
- Summoner name

**Example:**

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│  [Champion Splash Art]        VICTORY              │
│                                                     │
│  AHRI • THE NINE-TAILED FOX  |  VorpalFox         │
│                              |                     │
│  Performance Score: 84 | Damage Share: 29%         │
│  Kill Participation: 67%                           │
│                                                     │
│  The Unkillable Demon King                         │
│                                                     │
│  Ranked Solo/Duo • Patch 15.1 • 34:21              │
│                                                     │
│  summoner-chronicle.riot.com                       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Functionality:**
- Click "Copy to Clipboard" for easy Twitter posting
- Click "Download" to save as PNG
- Click "Share to Discord" for direct Discord message

### 2. Full Graphic Export

**Trigger:** "Export as PDF" button

**Output:** Complete graphic (all 7 zones) in printable PDF format

**Features:**
- High-resolution (300 DPI) for printing
- Page breaks between zones
- QR code linking back to interactive version (if in-client)
- Metadata (summoner name, match ID, date)

**Use Cases:**
- Print as poster (24×30 inch at home)
- Share as PDF with friends or team
- Archive as digital trophy

### 3. Copy-Paste Text Snippets

**Trigger:** Hover over any insight text, then right-click "Copy"

**Content:** Just the text (formatted for Reddit/Discord markdown)

**Example:**

```
Copy: "Your death at 19:22 dropped win probability by 18% — the largest negative swing of the match."

Pasted in Discord/Reddit:
> Your death at 19:22 dropped win probability by 18% — the largest negative swing of the match.
```

## Replay Integration (Client-Only)

### 1. Click-to-Replay Synchronization

**Requirement:** Viewed in League client (not web browser)

**Trigger:** Click on any timeline event or stat callout

**Action:** Client jumps replay to that moment

**Example:**

```
Click on timeline event "8:14 — First Blood (solo kill on Zed)"
↓
Replay jumps to 8:14
↓
Champion (Ahri) camera centered, Zed visible
↓
Replay plays forward slowly (0.5x speed)
↓
User can pause, rewind, speed up to analyze the play
```

**UI Integration:**
- Event markers glow when hoverable
- Mouse cursor changes to "hand" icon
- Tooltip: "Click to jump to replay"

### 2. Heatmap Replay Overlay

**Requirement:** Client mode + replay available

**Feature:** Playing replay while heatmap visible overlays your positional data

**Visual:**
- Semi-transparent red overlay showing your position history during current scene
- As replay plays forward, heatmap updates in real-time
- Shows "decision points" (where you right-clicked, key moments)

**Use:** Watch replay while seeing positioning context

## Dynamic Refinement

### 1. "That Was Close" Callout

**Trigger:** If game was close (gold differential <1000g at 25 min)

**Display:** Special section in Zone 7

```
┌──────────────────────────────────┐
│ 🔥 That Was Close!               │
├──────────────────────────────────┤
│ Gold differential narrowed from  │
│ +2500g (15 min) to +800g (25 min).│
│                                  │
│ One missed teamfight and you lose│
│ this game. Your pacing was elite.│
└──────────────────────────────────┘
```

### 2. Conditional Celebrations

**If win + high stats:** Celebratory tone & animations

```
Zone 1 result banner: "VICTORY" text has falling confetti animation
Parting Shot: Enthusiastic language ("domination", "perfection")
Colors: Brighter, more saturated
```

**If loss but strong performance:** Encouraging tone

```
Parting Shot: "Your 29% damage share was the team's hope. 
One rotation decision away from victory."
Colors: Neutral, respectful
```

### 3. First-Match Celebration

**Trigger:** First time user generates a graphic

**Display:** Special "Congratulations!" screen after generation

```
┌────────────────────────────────────┐
│  🎉 Your First Summoner's          │
│  Chronicle is Ready!               │
├────────────────────────────────────┤
│ You've unlocked post-game insights │
│ for your games. Continue playing   │
│ to build your performance library. │
│                                    │
│ [View Graphic] [Share] [Tutorial]  │
└────────────────────────────────────┘
```

## Performance Optimizations (For Smooth Experience)

### 1. Lazy Loading

**Concept:** Load zones as user scrolls, not all at once

**Benefit:** Initial graphic appears in <2 seconds (Zone 1 only), zones load as user scrolls

**Visual Feedback:** Subtle loading spinner for each zone as it loads

### 2. Caching & Preloading

**Strategy:**
- Cache computed metrics locally (browser storage)
- Preload assets (images, styles) in background
- If user revisits same match, serve from cache instantly

### 3. Progressive Enhancement

**Fallback Rendering:**
- If replay unavailable: Skip heatmap, show message "Replay required for positioning analysis"
- If cloud data unavailable: Show cached percentiles with "estimated" label
- If NLG offline: Show template-based text (less poetic but functional)

## Error Handling & Feedback

### 1. Graceful Degradation

**If Something Fails:**

```
Zone 5 (Heatmap) unavailable:
┌──────────────────────────────────┐
│ 📍 Positioning Data Unavailable   │
├──────────────────────────────────┤
│ Replay file not found or expired. │
│ Other zones are still available.  │
│                                  │
│ [Try Again] [Learn More]          │
└──────────────────────────────────┘
```

User sees other 6 zones; Heatmap gracefully omitted.

### 2. Success Confirmation

**After actions:**

```
Copied to Clipboard:
┌──────────────────────────────────┐
│ ✓ Copied! Ready to share          │
│ (Dismisses after 2 seconds)       │
└──────────────────────────────────┘

Exported as PDF:
┌──────────────────────────────────┐
│ ✓ Downloaded: Summoner-15221.pdf  │
│ (Appears in user's Downloads)     │
└──────────────────────────────────┘
```

## Boundaries

**Assumes from Visual Design:**
- All content is ready to be shared (no incomplete zones)
- Zones are self-contained and can be viewed individually

**Provides to User:**
- Delightful, shareable experience
- Smooth performance on all devices
- Graceful handling of errors
