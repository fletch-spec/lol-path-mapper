# Accessibility: Universal Design & Compliance

## Standards

**Target:** WCAG 2.1 Level AA (minimum standard for public-facing products)

**Testing:** Automatic + manual testing; third-party audit quarterly

## Colorblind Support

### Colorblind Modes

**Standard Mode (Trichromacy):**
- Red-Green-Blue full spectrum
- Used by ~92% of population

**Deuteranopia Mode (Green-Blind):**
- Red, yellow, blue visible
- Affects ~1% of males

**Protanopia Mode (Red-Blind):**
- Yellow, blue, blue-cyan visible
- Affects ~1% of males

**Tritanopia Mode (Blue-Blind):**
- Red, green, yellow visible
- Affects ~0.001% (extremely rare; included for completeness)

**Implementation:**
- All color-coded graphics (momentum curve, heatmaps, bars) use color-blind-safe palettes
- Each color pair is distinguishable by both hue and brightness
- User can toggle colorblind mode in settings (auto-detect available)

**Examples:**

| Element | Standard | Deuteranopia | Protanopia | Tritanopia |
|---------|----------|--------------|-----------|-----------|
| Momentum Winning | Gold | Blue | Blue | Yellow |
| Momentum Losing | Red | Orange | Blue-Cyan | Red |
| Heatmap High | Red | Green | Red-Green | Blue |
| Heatmap Low | Blue | Blue | Cyan | Orange |

### Testing Protocol

1. **Automated:** Convert all graphics to colorblind modes; verify distinguishability
2. **Manual:** Colorblind testers review graphics (quarterly)
3. **User Feedback:** Forum for colorblind users to report issues

## Screen Reader Support

**Screenreader Technology:** NVDA, JAWS, VoiceOver compatible

### Semantic HTML + ARIA

**Every interactive element has:**
- Clear label (text or ARIA label attribute)
- Role (button, heading, list item, etc.)
- State (if applicable: expanded, selected, disabled)

**Example:**

```html
<button aria-label="Toggle colorblind mode" 
        aria-pressed="false">
  Colorblind Mode
</button>

<div role="heading" aria-level="2">
  Zone 2: Champion Portrait & Core Stats
</div>

<table role="table" aria-label="Performance Matrix">
  <tr>
    <th>Metric</th>
    <th>Value</th>
  </tr>
  ...
</table>
```

### Data Visualization Accessibility

**For Charts & Graphs:**

1. **Text Alternative:** Below each chart, provide data table with same information
2. **ARIA Descriptions:** Chart has `aria-describedby` pointing to text description
3. **Interactive Elements:** Hover tooltips are announced by screen reader
4. **Keyboard Access:** User can navigate chart using arrow keys, hear values

**Example:**

```html
<svg id="momentumChart" role="img" aria-labelledby="chartTitle chartDesc">
  <title id="chartTitle">Momentum Curve Over Match Duration</title>
  <desc id="chartDesc">
    Gold differential starts at 0. First kill at 8:14 increases to +300g.
    Death at 19:22 drops to -200g. Recovers to +1500g by 28:30...
  </desc>
  <!-- Chart SVG content -->
</svg>
```

### Text-to-Speech Ready

**Content Preparation:**
- All text is structured (headings, paragraphs, lists)
- Abbreviations expanded (e.g., "KP" → "Kill Participation")
- Numbers spelled out for clarity (e.g., "67%" → "sixty-seven percent")
- Jargon has tooltips with expansions

**ARIA Live Regions:**
- Calculations that update are marked `aria-live="polite"`
- Screen reader announces changes without forcing user back to top

## Keyboard Navigation

### Full Keyboard Access

**Every interactive element is reachable via keyboard:**

| Interaction | Keyboard | Screen Reader Announcement |
|------------|----------|---------------------------|
| Toggle setting | Tab + Enter | "Toggle colorblind mode, not pressed" |
| Navigate zones | Tab / Shift+Tab | "Zone 1 Header" |
| View tooltip | Tab + Enter / Space | Tooltip content read aloud |
| Click button | Tab + Enter / Space | Button action performed |
| Navigate table | Arrow keys | Current cell announced |
| Exit menu | Escape | Menu closed announcement |

### Tab Order

**Logical tab order:** Left-to-right, top-to-bottom within zones

**Skip Links:** Top of graphic has "Skip to [Zone]" links for power users

**Focus Indicator:** Clear visual focus ring (2px outline, high-contrast color)

## Motor Accessibility

### Click Targets

**Minimum size:** 44×44 pixels (WCAG standard)

**Spacing:** Buttons have 8px minimum spacing to prevent accidental clicks

**Alternative Inputs:**
- Mouse: Point and click
- Keyboard: Tab + Enter
- Touch: Single tap (no double-click required)
- Voice Control: Voice commands for major actions (if OS supports)

### Simplified Mode

**For users with limited motor control:**
- Reduce number of interactive elements
- Larger touch targets (56×56px)
- Fewer hover-required interactions (keyboard alternative available)

## Cognitive Accessibility

### Plain Language

**Writing Standards:**
- Flesch-Kincaid Grade Level: 6-8 (readable by age 12+)
- Sentences <20 words (shorter = easier to understand)
- Jargon avoided or explained
- Acronyms expanded on first mention

**Examples (Bad → Good):**

❌ "Your KP (67%) is in the top 12% of Ahri players this patch — but your MPI (41) suggests late-game scaling suboptimality."

✅ "Your kill participation (67%) is in the top 12% for Ahri. But your map pressure (41) shows you stayed in lane too long after 20 minutes."

### Consistent Navigation

- Same buttons, same place in each zone
- Predictable interactions
- No surprising popups or auto-playing media

### Cognitive Load Management

**Information Progressively Disclosed:**
1. **Zone 1 (Simple):** Win/loss, champion, player name
2. **Zone 2 (Moderate):** 5 metrics
3. **Zone 3-6 (Complex):** Detailed analysis
4. **Zone 7 (Simple):** Summary and improvement tips

**Tooltips:** Detailed explanations hidden behind hover (not forced on load)

## Visual Accessibility

### Font & Typography

**Font Choice:** Sans-serif (Arial, Helvetica, or system font)
- Easier to read than serif
- Clear distinction between similar letters (l/I/1, O/0)

**Font Size:**
- Base: 14px (readable at arm's distance)
- Headings: 18-24px
- Important metrics: 16px

**Line Height:** 1.5× (increased spacing for readability)

**Color Contrast:**
- Text on background: 4.5:1 minimum (normal text)
- Large text: 3:1 minimum
- Icons: 3:1 contrast ratio
- Testing: WCAG Contrast Checker

### Motion & Animation

**Reduce Motion:**
- Check user's OS preference (`prefers-reduced-motion`)
- Disable animations for users with vestibular disorders
- No auto-playing videos or GIFs

**Safe Animations:**
- Color transitions: <200ms (fast enough to feel instant)
- Fade-ins: <300ms
- Avoid: Flashing, strobing, or high-frequency changes

## Audio Accessibility

**If Any Audio Elements:**
- Captions for all spoken content
- Transcripts for explanatory audio
- No background music during critical information

## Testing & Validation

### Automated Testing

**Tools:** axe DevTools, WAVE, Lighthouse

**Frequency:** Every build (continuous integration)

**Metrics:**
- Zero critical violations
- <5 warnings (accessibility issues that don't block use)

### Manual Testing

**Quarterly Audit:**
1. Keyboard-only navigation (no mouse)
2. Screen reader testing (NVDA + JAWS)
3. Colorblind mode review
4. Mobile accessibility (touch targets, zoom)

**User Testing:** Recruit 2-3 users with disabilities; gather feedback

## Accessibility Statement

**In-App Statement (Settings > Accessibility):**

"The Summoner's Chronicle is designed to be accessible to all players.

**Supported:**
- Colorblind modes (4 types)
- Screen readers (NVDA, JAWS, VoiceOver)
- Keyboard-only navigation
- High-contrast mode

**Report Issues:**
If you encounter accessibility barriers, please contact us at accessibility@summoner-chronicle.riot.com. We take accessibility seriously and will work to resolve issues promptly."

## Boundaries

**Assumes from All Packages:**
- All text content is well-written and uses plain language
- All visuals have text alternatives (labels, descriptions)
- No critical information is conveyed through color alone

**Provides to All Packages:**
- WCAG AA-compliant implementation
- Support for all major assistive technologies
- User controls for accessibility preferences
