# Natural Language Generation for Event Annotations & Insights

## Purpose

Generate natural language descriptions of match events, improvement suggestions, and emotional story summaries. Combines templates with learned stylistic variation to produce readable, contextual text.

## Architecture: Template-Based + VAE Variation

### Approach

**Two-Stage Generation:**

1. **Template Generation:** Structured, deterministic event annotation
   - Format: `{timestamp} — {event_type} {qualifier} {outcome} {strategic_comment}`
   - Example template: `"{time} — {kill_type} on {target}. {positioning_quality}. {gold_impact}"`

2. **Stylistic Variation:** Variational Autoencoder (VAE) adds natural cadence and word choice variation
   - Input: Generated template text
   - VAE processing: Learn style distribution from professional commentary
   - Output: Natural-sounding variant of template

### Stage 1: Template Generation

**Template Rules:**

| Event Type | Template | Variables |
|-----------|----------|-----------|
| Kill | `{time} — {kill_type} ({target_champion}). {positioning}. {gold_impact}.` | time, target, positioning quality |
| Death | `{time} — Caught out {location}. {enemy_champions} unaware on map for {fog_duration}s.` | location, enemies present, vision |
| Objective | `{time} — {objective_type} {status} ({team_control}). {objective_importance}.` | objective, team, importance |
| Teamfight | `{time} — {side} initiated {fight_type}. Result: {outcome_description}.` | side, engagement, result |

**Example Instantiations:**

```
Template: "{time} — Solo kill on {target}. {positioning_quality}. {gold_impact}."

Instantiation 1:
"8:14 — Solo kill on Zed. Excellent positioning from fog. 400g bounty earned."

Instantiation 2:
"8:14 — Solo kill on Zed. Zed was overextended, caught by excellent charm. Bounty swing: +400g."
```

### Stage 2: VAE Stylistic Variation

**Training Data:** 100k LCS broadcast transcripts (professionally annotated game moments)

**VAE Architecture:**
- Encoder: Text → latent space (20-dimensional)
- Decoder: Latent space → varied text (different word choices, phrasing)
- Loss: Reconstruction loss + KL divergence (learn style distribution)

**Sampling:** Sample from latent distribution to generate natural variations

**Example Transformations:**

Template: *"19:45 — Aggressive invade punished by Lee Sin."*

VAE variations:
- *"19:45 — Risky jungle invade; unseen Lee Sin punished you."*
- *"19:45 — Over-extended in enemy jungle. Lee Sin capitalized."*
- *"19:45 — Your deep invade was read. Lee Sin was waiting."*

**All variations preserve factual accuracy** (timing, champions, outcome) while varying tone and emphasis.

## Applications

### Zone 3: Timeline Narrative – Event Annotations (Track C)

**Generation Process:**

1. **Identify Events:** Scan match timeline for major moments
   - First Blood, Deaths, Multikills, Objectives, Power Spikes, Teamfights
2. **Generate Templates:** For each event, instantiate appropriate template
3. **Apply VAE:** Transform templates to natural variations
4. **Selection:** Choose most compelling variation for display (highest NLG confidence score)

**Examples:**

*"8:14 — First Blood (solo kill on enemy Zed, 400g bounty collected)"*  
*"17:45 — Lost teamfight at dragon. Your charm missed priority target."*  
*"28:30 — Quadra kill! Turned baron fight from 3v5. Game flipped."*

### Zone 7: Comparative Insights – Improvement Prompts

**Template:** `"Work on: **{skill_area}**. {current_performance}. Next game: {actionable_step}. Target: {goal}. Impact: {benefit}."`

**Example Instantiation:**

*"Work on: **Mid-game vision**. Your vision score drops 40% between 15-25 min. Next game, buy a **Control Ward on every recall after 12 minutes** — aim for **1.8 vision score/min**. This 0.4 point gain = +2% average win rate over 100 games."*

**VAE Variations:**
- *"Weakness: Mid-game vision. Score dips 40% 15-25 min. Remedy: Control ward every recall post-12min. Target 1.8 vision/min (+0.4 gain = +2% WR)."*
- *"Focus area: Vision drops 40% mid-game (15-25 min). Solution: Consistent control ward purchases after 12 min. Achieve 1.8 vision/min for +2% win rate."*

### Zone 7: Parting Shot – Emotional Signature

**Template:** `"{initial_characterization}. {performance_summary}. {outcome_narrative}."`

**Examples:**

*"A patient hunter who struck at the right moments, but left too many kills on the table. Your team's victory was built on your early pressure, not your late-game execution."*

*"The unkillable demon king — 3 deaths in 34 minutes, elite positioning, and a heatmap that shows calculated, not reckless, aggression."*

*"A ghost on the map. Your presence was felt globally through warding and rotations, but your damage says you stayed safe. Calculated strategy worked, but aggression would've been rewarding."*

**Generation Process:**

1. **Profile Analysis:** Extract key stats (deaths, KP, positioning, roaming, etc.)
2. **Archetype Matching:** Assign emotional archetype (Hunter, King, Ghost, Executioner, etc.) based on stats
3. **Template Selection:** Choose template matching archetype
4. **VAE Variation:** Transform template to natural language

## Data Inputs for NLG

**Required Data:**

| Input | Source | Used For |
|-------|--------|----------|
| Event timestamps & types | Match timeline API | Event annotations |
| Champion names, abilities | League data | Templates (what ability was cast) |
| Gold impacts | Match timeline | Consequence descriptions |
| Player performance metrics | Computed statistics | Improvement prompts, archetypes |
| Pro play reference stats | Pro database | Shadow match comparison text |

## Validation & Quality Control

**Factual Accuracy Check:**
- Every generated text must correspond to actual game events
- Automated validation: Parse text, extract facts, check against match data
- Reject generations that contradict timeline

**Readability Check:**
- Flesch-Kincaid Grade Level: 6-8 (readable by Silver+ players)
- Length: Event annotations <30 words, improvement prompts <50 words
- Manual review: 10% of generated text reviewed by humans (first month)

**Tone Consistency:**
- Parting shots should feel earned (celebration for wins, constructive for losses)
- Improvement prompts should be encouraging, not demoralizing
- Emotional language should match performance level

## Limitations & Edge Cases

**Known Limitations:**
- VAE can occasionally generate awkward phrasings (1-2% of samples)
- Archetype matching can be ambiguous (multiple matching archetypes)
- Edge games (2-minute FF, 60+ minute stalling) have limited templates

**Edge Cases:**

| Case | Handling |
|------|----------|
| No major events (5 cs game) | Use generic narrative; focus on small moments |
| Mixed performance (great early, awful late) | Multiple characterizations in parting shot |
| Extremely high KDA (30/0/10) | Use "Unkillable" archetype; avoid overstatement |
| Extremely low KDA (0/10/0) | Use constructive framing; focus on learning |

## Boundaries

**Assumes:**
- VAE model is trained on representative pro commentary
- Match timeline is accurate and complete
- Player performance metrics are calculated correctly

**Provides:**
- Natural, readable event descriptions
- Contextual improvement suggestions
- Emotionally resonant story summaries
