# The Summoner's Chronicle – Package Index

Welcome to the modular specification for **The Summoner's Chronicle**, a post-game champion-centric analysis graphic for League of Legends.

This directory decomposes the complete specification into independent, hierarchically organized packages that each address a distinct concern.

## Package Overview

### [Overview](overview/README.md)
High-level purpose, philosophy, target audience, and champion selection strategy.

### [Visual Design](visual-design/README.md)
Canvas dimensions, layout zones, and the 7 distinct display sections that comprise the graphic.

- **[Zones](visual-design/zones/README.md)** – Detailed specifications for all 7 zones, from header to comparative insights

### [Statistics & Algorithms](statistics-and-algorithms/README.md)
The computational and statistical frameworks that power insights and analytics.

- **Computer Vision Heatmaps** – Position density tracking via replay analysis
- **Win Probability Model** – Counterfactual impact analysis for player actions
- **Role Positional Normalization** – Role-based performance benchmarking
- **Natural Language Generation** – Procedural event annotation and insights
- **Build Adaptation Scoring** – Item purchase optimization scoring

### [Infrastructure](infrastructure/README.md)
Data sources, privacy guarantees, accessibility features, localization, and polish interactions.

---

## How to Navigate

1. **Start here:** [Overview](overview/README.md) to understand the product vision
2. **Design focus:** [Visual Design](visual-design/README.md) for layout and presentation
3. **Implementation:** [Statistics & Algorithms](statistics-and-algorithms/README.md) for computational methods
4. **Deployment:** [Infrastructure](infrastructure/README.md) for data, privacy, and UX polish

---

## Cross-Package Boundaries

| From | To | Via |
|------|----|----|
| Overview | Visual Design | Visual hierarchy implements the philosophy |
| Visual Design | Statistics & Algorithms | Zones display algorithmic outputs |
| Statistics & Algorithms | Infrastructure | Algorithms require data sources and respect privacy |
| Infrastructure | All Packages | Accessibility and localization apply globally |

---

**Project:** The Summoner's Chronicle  
**Scope:** Post-game champion performance analysis  
**Audience:** Silver to Diamond players + casual viewers  
**Focus:** Narrative-driven, visually compelling champion stories
