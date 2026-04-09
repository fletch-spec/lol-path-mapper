# Localization: Multi-Language & Regional Support

## Languages Supported

**14 languages** with full localization:

1. **English (US/UK)** — Default
2. **Spanish (Spain/Latin America)** — Separate translations for regional differences
3. **French** — France, Belgium, Canada
4. **German** — Germany, Austria, Switzerland
5. **Italian** — Italy
6. **Portuguese** — Portugal, Brazil (separate translations)
7. **Russian** — Russia, CIS regions
8. **Japanese** — Japan
9. **Korean** — South Korea
10. **Simplified Chinese** — China, Singapore
11. **Traditional Chinese** — Taiwan, Hong Kong
12. **Vietnamese** — Vietnam
13. **Turkish** — Turkey, Cyprus
14. **Thai** — Thailand

## Localization Strategy

### 1. Text Translation

**Scope:**
- All UI labels (buttons, headings, metric names)
- Descriptive text (explanations, tooltips, improvement prompts)
- Event narratives (auto-generated game moment descriptions)
- Parting shot (poetic summary)

**Translation Process:**

1. **Source:** English text marked as translatable in codebase
2. **Professional Translators:** Hired per language (native speakers, gaming expertise)
3. **Context:** Translators receive:
   - Full spec with context
   - Champion names + titles (to understand matchups)
   - Example screenshots (visual context)
   - Glossary (standardized League terminology)
4. **Review:** In-region community members review for cultural fit
5. **Testing:** Linguists verify accuracy, tone, length

**Quality Gates:**
- Terminology consistency (same English term → same translation every time)
- Cultural sensitivity (no offensive or region-specific phrases)
- Length compliance (translations fit UI without overflow)
- Context accuracy (technical terms are precise)

### 2. Number Formatting

**Regional Standards:**

| Region | Examples |
|--------|----------|
| US/UK | 1,234.56 (comma separator, period decimal) |
| EU (France, Germany, etc.) | 1.234,56 (period separator, comma decimal) |
| China | 1,234.56 (comma separator, period decimal) |
| Brazil | 1.234,56 (period separator, comma decimal) |
| India | 12,34,567.89 (lakh system) |
| Thailand | 1,234.56 (same as US) |

**Implementation:**
- Detect user region (from Summoner IP, account settings)
- Format all numbers accordingly (gold, damage, stats)
- Example: "428 gpm" (US) vs. "428 gpm" (EU shows as "428 gpm" but with locale formatting)

### 3. Time & Date Formatting

**Timestamp Examples:**

| Region | Format | Example |
|--------|--------|---------|
| US | MM/DD/YYYY HH:MM AM/PM | 01/15/2025 11:42 PM |
| EU | DD/MM/YYYY HH:MM | 15/01/2025 23:42 |
| ISO Standard | YYYY-MM-DD HH:MM UTC | 2025-01-15 23:42 UTC |
| Japan | YYYY年MM月DD日 HH:MM | 2025年01月15日 23:42 |
| China | YYYY年M月D日 HH:MM | 2025年1月15日 23:42 |

**Match Duration:** Shows as "MM:SS" globally (same everywhere)

**Timezone Handling:**
- Display local timezone offset: "23:42 UTC+1" (EU example)
- Allow user to toggle UTC vs. local time

### 4. Champion Names & Abilities

**Policy:** Champion names and titles **NOT translated** (global consistency)

✅ **Correct:**
- "AHRI • THE NINE-TAILED FOX" (all regions)
- "Her charm is called Charm" (description translated)

❌ **Incorrect:**
- Spanish: "AHRI • LA ZORRA DE NUEVE COLAS" (inconsistent with client)

**Ability Names:** League client shows abilities in original English; we follow same convention

### 5. Cultural Localization

#### Dragon/Baron References

**English:** "Dragon", "Elder Dragon", "Baron Nashor"

**Regional Nuance:**
- Spanish: "Dragón" (consistent with Spanish LoL client)
- Chinese: "巨龙" (giant dragon, matches client)
- Korean: "용" (dragon, matches client)

#### Combat Phraseology

**English Narrative:** "Aggressive jungle invade punished by unseen Lee Sin"

**Spanish:** "Invasión agresiva del jungla, castigada por un Lee Sin invisible" (matches Spanish narrative style)

**Japanese:** "アグレッシブなジャングル侵略が見えないリーシンに罰せられた" (flows naturally in Japanese)

#### Metaphorical Summaries (Parting Shot)

**English Examples:**
- "The Unkillable Demon King" (cultural reference to competitive dominance)
- "A ghost on the map" (Western idiom)

**Regional Adaptations:**
- Japanese: "不滅の鬼王" (demon king = cultural equivalent)
- Korean: "지도상의 유령" (ghost metaphor = culturally resonant)
- Spanish: "El Rey Demonio Inmortal" (maintains metaphor)

**Process:**
- Each region's translator adapts metaphors to culturally resonant equivalents
- Maintains emotional impact, not literal word-for-word

### 6. Metric Terminology

**League of Legends uses different terms across regions:**

| Metric | English | Spanish | French | German |
|--------|---------|---------|--------|--------|
| CS (Creep Score) | Minions killed | CS | CS | CS |
| KDA | Kills/Deaths/Assists | KDA | K/M/A | K/T/U |
| Teamfight | Team Fight | Pelea en equipo | Combat d'équipe | Teamfight |
| Gank | Jungle gank | Ataque coordinado | Gank | Gank |
| Roaming | Roaming | Roaming | Roaming | Roaming |

**Standard:** Use region's official League terminology (from in-game client)

### 7. Patch Notes & Context

**Example:** "Patch 15.1 • Ranked Solo/Duo • 34:21 match duration"

**Localized:** Patch format stays same globally, but queue name localizes

- English: "Ranked Solo/Duo"
- Spanish: "Clasificatoria Solo/Dúo"
- French: "Classement Solo/Duo"
- Japanese: "ソロ/デュオランク"

## Regional Customization (Beyond Translation)

### Eastern Asian Regions (China, Korea, Japan)

**Consideration:** "Lucky numbers" and color symbolism

- Avoid number 4 in Chinese context (sounds like death)
- Red = lucky; avoid inauspicious color combinations
- Parting shot language adjusted for respect/humility norms

### Example: Color Palette for Heatmaps

**Western (Standard):**
- Red = hot/intense (culturally positive in competitive context)

**Eastern Customization:**
- Offer alternate palette: Blue → Purple → Yellow → Gold (lucky colors in East Asia)

### Middle East & North Africa

**Consideration:** Right-to-left (RTL) languages not yet supported; may add in future

**Current:** Flagged as future enhancement, not included in initial 14-language rollout

## Testing & QA

### Linguistic Testing

**Per Language (Quarterly):**
1. **Native Speaker Review:** Check for naturalness, cultural fit
2. **Context Accuracy:** Verify technical terms are correct for region
3. **UI Fit:** Ensure translated text doesn't overflow buttons/boxes
4. **Number/Date Formatting:** Spot-check examples

### Regional Testing

**Quarterly Regional Testing:**
- Select 1 region per quarter for deep-dive testing
- Test with native speakers in actual region
- Gather feedback on cultural appropriateness

### Automated Checks

**Build-Time Validation:**
- Missing translations: Flag any untranslated text
- Length overflow: Warn if translations exceed UI bounds (by 10%+)
- Terminology consistency: Verify same English term always translates the same way
- Encoding: Verify all character sets display correctly

## Translation Management

### Tool: Crowdin or Similar

**Workflow:**
1. Developer marks English text as translatable
2. Automated sync to translation platform
3. Professional translators submit translations
4. Automated sync back to codebase
5. Build system verifies 100% coverage before release

### Update Frequency

**Translations Updated:**
- After major features (new zones, new metrics)
- Post-patch (if balance changes affect terminology)
- Quarterly community review

**Patch Translations:**
- Simple metrics & numbers: <2 hours (automated)
- Narrative changes (NLG updates): <1 day (professional translators)
- UI text: <4 hours (existing strings updated)

## Boundaries

**Assumes from All Packages:**
- All text is in English source code
- Numbers follow standard format (decimal numbers)
- No hardcoded language-specific logic

**Provides to All Packages:**
- Multi-language support for all user-facing text
- Region-appropriate number/date/time formatting
- Culturally sensitive terminology and phrasing
