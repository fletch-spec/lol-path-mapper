# Role-Positional Normalization

## Purpose

Normalize performance metrics by champion role and positional archetype, ensuring that a 10/0/5 ADC is not directly compared to a 10/0/5 Support. Role-based expectations differ fundamentally.

## Challenge

**Raw Comparison Problem:**

| Stat | Support | ADC | Raw Interpretation |
|------|---------|-----|-------------------|
| Kills | 3 | 12 | ADC is better |
| Damage | 12k | 71k | ADC is better |
| CS | 85 | 278 | ADC is better |

But a 12k damage support is elite, while 71k damage ADC is average.

**Solution:** Normalize metrics against role-specific expectations.

## Method: PCA-Based Role Clustering

### Step 1: Feature Engineering

Extract 20 champion statistics per game:

| Category | Features |
|----------|----------|
| Economy | Gold/min, CS/min, Gold efficiency |
| Combat | Damage/gold, Kill participation, Damage share |
| Survival | Deaths/game, KDA, Damage taken/mitigated |
| Map | Vision score/min, Roaming frequency, Objective damage |
| Utility | CC/min, Shields provided, Healing provided |

### Step 2: Principal Component Analysis (PCA)

1. **Input:** 10k games × 20 features
2. **Processing:** Center and scale each feature
3. **PCA Computation:** Extract first 3 principal components (PC1, PC2, PC3)
4. **Variance Explained:** PC1 = 45%, PC2 = 25%, PC3 = 15% (cumulative 85%)

**Interpretation:**
- PC1: "Economy axis" (farm-focused vs. team-focused)
- PC2: "Damage axis" (burst vs. sustained)
- PC3: "Utility axis" (shields/healing vs. damage)

### Step 3: Clustering

1. **Algorithm:** K-Means with k=6 clusters
2. **Initialization:** Seeds based on known role archetypes (Mid, ADC, Support, Jungle, Top, Support-Tank)
3. **Convergence:** Iterate until cluster centroids stabilize
4. **Result:** 6 role archetypes, each with distinct feature profiles

**Archetypes:**

| Archetype | Profile | Example Champions |
|-----------|---------|-------------------|
| Carry | High damage, high economy | ADC, Mid |
| Brawler | Moderate damage, high tankiness | Top bruisers |
| Tank | Low damage, high tankiness, utility | Support tank, Top tank |
| Support | Low economy, high utility | Enchanter, Warden |
| Jungler | Mobile, high roaming, moderate damage | Elise, Lee Sin |
| Control | Moderate damage, high CC/utility | Control mage |

### Step 4: Assignment

For each player:
1. Compute their 20-feature vector
2. Calculate distance to each archetype centroid
3. Assign to nearest archetype
4. Exception: If player deviates from their assigned archetype, flag as "off-meta" build

**Example:** 
- Player: Ahri mid (typical carry archetype)
- Features: High damage (40 damage/gold), High economy (395 gpm), High roaming (0.18 roams/min)
- Closest archetype: "Carry" → Normal expectations apply

## Dynamic Benchmarking

### Weekly Updates (Post-Patch)

1. **Collect:** New games from patch release
2. **Recompute:** PCA and K-Means on updated dataset
3. **Compare:** How did archetype profiles change?
4. **Example:** Durability patch 2024 → Tank archetype profiles shift (expected tankiness +15%)

### Patch-Specific Expectations

**Before patch:** Tank expected to survive X damage, mitigate Y%  
**After patch:** Tank expected to survive 1.15X damage, mitigate 1.10Y%

Benchmarks adjust weekly to keep percentile rankings meaningful.

## Applications

### Zone 2: Champion Portrait – Five-Ring Performance Dial

**Normalization:** All 5 metrics are compared against role-specific benchmarks

**Example:**
- **Kill Participation (KP):** 
  - Carry baseline: 55%
  - Support baseline: 65%
  - Your KP: 67%
  - Your score: (67 - 65) / std_dev = +0.5 SD above support average → Percentile 69

- **Gold Efficiency:**
  - Carry baseline: 1.0 (meeting expectations)
  - Support baseline: 0.4 (lower economy expected)
  - Your efficiency: 0.42 (support) → Percentile 52

### Zone 4: Advanced Performance Matrix

**Quadrant A (Gold & XP Efficiency):** Compared to role average  
**Quadrant B (Combat Efficiency):** Compared to role average  
**Quadrant C (Objective Control):** Compared to role average (supports roam less)  
**Quadrant D (Clutch Factor):** Compared to archetype-specific expectations

### Zone 7: Comparative Insights – Percentile Rankings

**All percentiles are role-specific:**
- Damage Share: vs. other mids (not vs. supports)
- Vision Score: vs. other supports (not vs. carries)
- Deaths per Game: vs. other junglers (not vs. carries)

## Edge Cases & Special Handling

### Off-Meta Builds
- **Example:** AP Malphite in ADC role
- **Handling:** Detect deviation; apply multiple archetypes weighted by similarity
- **Interpretation:** "Your itemization suggests a Control archetype, but you're in an ADC role. Expectations are hybrid."

### New Champions (First Patch)
- **Challenge:** No games in training data for PCA
- **Solution:** Use most similar existing champion's archetype as default
- **Update:** After 10k+ games collected, recompute PCA with new champion

### Duo/Flex Queue Anomalies
- **Challenge:** Support player might have farmed excessively (unusual for role)
- **Solution:** Flag as "role deviation" and note in insights
- **Interpretation:** *"You farmed 145 CS as support (unusual; typical = 50 CS). Economy metrics are higher than typical support baseline."*

## Validation

**Test:** Generate role assignments for 1000 random games, compare to known Riot API role data

- Expected accuracy: >92% (some ambiguous edge cases)
- False positive rate: <5% (misassigning roles)

**Benchmark Accuracy:** Compare percentile rankings to Riot's official stats

- Expected correlation: >0.95 (same championship, different scale)
- Outliers flagged and investigated

## Boundaries

**Assumes:**
- 20 features adequately capture role differences
- PCA with 6 clusters is appropriate granularity
- Patch updates happen weekly

**Provides:**
- Role-specific performance baselines
- Archetype assignments for each player
- Updated percentile rankings weekly
