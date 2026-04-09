# Win Probability Impact Model

## Purpose

Calculate win probability at key game moments and attribute changes in probability to individual player actions, enabling statements like "your death at 19:22 decreased win probability by 18%."

## Framework

**Type:** Gradient-boosted tree ensemble (XGBoost)  
**Training Data:** 10M+ solo queue games  
**Update Frequency:** Weekly (post-patch)

### Features (Input to Model)

The model takes game state at any moment and predicts win probability:

| Feature | Description |
|---------|------------|
| Gold Differential | Your team gold - enemy team gold |
| XP Differential | Your team XP - enemy team XP |
| Tower Differential | Your team turrets remaining - enemy |
| Dragon/Baron Count | Your team objectives secured |
| Champion Composition Synergy | Pre-calculated synergy score (tank/damage/cc balance) |
| Death Timer Remaining | Queue time for next spawn (impacts 4v5 windows) |
| Gold per Minute trajectory | Predicted future gold based on current pace |
| Patch Balance State | Meta weighting (some champs stronger this patch) |

**Example:** At 20 minutes, your team: +1000g, +100 xp, +1 tower, 1 dragon, 0 baron → Win Probability: 58%

## Calculation Methods

### 1. Monte Carlo Simulation (Real-Time Estimate)

**When:** Used for "sentiment arc" in Timeline Narrative (Zone 3)

**Method:**
1. Sample 10,000 possible future game sequences from current game state
2. Each sequence: simulate next 3-5 minutes using learned play patterns
3. Terminal condition: One team reaches win condition (5-0 teamfight, elder, base destruction)
4. Count outcomes: Win probability = (# winning sequences) / 10,000

**Advantages:** Intuitive, handles game uncertainty well  
**Disadvantages:** Slow (~30 seconds per calculation), approximate

### 2. Gradient-Boosted Model (Inference)

**When:** Used for static probabilities displayed in graphics

**Method:**
1. XGBoost model: 500 trees, max depth 8
2. Input: Game state features (listed above)
3. Output: Win probability (0-100%)

**Advantages:** Fast (<10ms per prediction), accurate  
**Disadvantages:** Black-box (less interpretable than Monte Carlo)

## Individual Action Attribution (Counterfactual Inference)

**Question:** How did this action change win probability?

**Method:** Counterfactual simulation

1. **Baseline:** Calculate win probability at moment of action (actual game state)
2. **Counterfactual:** Remove the action's effects and recalculate
   - Example: Death at 19:22 — simulate what if this player didn't die (all other events unchanged)
   - Remove: This player's death, lost CS, lost tempo, respawn delay
3. **Delta:** Difference between baseline and counterfactual = impact

**Example:**

```
Actual win prob at 19:22: 52%
Counterfactual (no death): 70%
Impact: -18% (death lost game momentum)
```

## Applications

### Zone 3: Timeline Narrative – Sentiment Arc

**Display:** Thin color-coded band showing win probability impact over time

**Calculation:** For each major event (kill, death, objective), compute counterfactual impact

**Visual:**
- Green spike: +5% win prob (your play increased chances)
- Red dip: -5% win prob (your play decreased chances)
- Yellow: ±2% neutral swings

### Zone 7: Comparative Insights – Shadow Match

**Calculation:** "What's Faker's win prob in the same situation?"

1. Find pro play game with same champion vs. enemy champion
2. Match game state at 15 min (within ±500g, ±1 kill)
3. Retrieve Faker's actual win prob from that game at 25 min
4. Compare: "Faker had 78% win prob here; you had 58%"
5. Analyze gap: "Faker roamed more; roaming +8% for you"

## Model Training

**Training Pipeline:**

1. **Data Collection:** Download 10M ranked solo queue games from API
2. **Feature Engineering:** Compute features at 1-minute intervals for each game
3. **Labeling:** Outcome = win or loss (binary)
4. **Splitting:** 80% train, 10% validation, 10% test
5. **Training:** XGBoost with log-loss objective
6. **Validation:** Test set accuracy >75% required
7. **Deployment:** Model pushed to cloud inference service

**Retraining:** Weekly, post-major patches (balance changes impact feature importance)

## Validation

**Accuracy Check:**
- Test set: Random sample of 100k games never seen during training
- Prediction vs. actual: Measure calibration (predicted 60% actually wins 60% of time)

**Sanity Checks:**
- Large gold lead (>5k) → >80% win prob ✓
- Early game deficits (<10 min) → recoverable (>40% win prob) ✓
- 4v5 fights → significant decrease (~-15%) ✓

## Limitations & Edge Cases

**Limitations:**
- Model is aggregate (average player): your play could be better/worse
- All games assumed solo queue (not pro play dynamics)
- Doesn't model mental boosts (teammates tilted, confident play)

**Edge Cases:**
- Early game (<10 min): Model has less confidence (wide prediction intervals)
- Lategame (35+ min): Fewer games in training data, less accurate
- New champions (first patch): Baselines estimated, not calculated from data

## Boundaries

**Assumes:**
- Match data (gold, kills, towers, dragons) is accurate from API
- Outcome (win/loss) is definitively known
- Game state is sufficiently captured by input features

**Provides:**
- Instant win probability estimates
- Counterfactual impact attribution
- Comparison to pro-level decision making
