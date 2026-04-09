# Build Adaptation Scoring

## Purpose

Evaluate the quality of item purchase decisions by comparing actual item choices to optimal choices given the game state at each recall.

## Framework: Reinforcement Learning Simulation

**Concept:** Model itemization as a sequential decision problem:
- **State:** Game state at each recall (gold, enemy items, team composition, game phase)
- **Action:** Which item to purchase
- **Reward:** Win probability increase over next 5 minutes (estimated via oracle model)
- **Goal:** Maximize cumulative reward

**Agent:** Deep Q-Network (DQN) trained on 10k high-elo games

## Method

### Training Phase (Offline)

**Data:** 10k high-elo ranked games (Masters+)

**Training Process:**

1. **State Representation:** Extract 30-dimensional vector at each recall:
   - Current gold, total gold earned, game phase
   - Enemy items (armor, MR, healing reduction, etc.)
   - Team composition (gaps in team comp)
   - Own items (current items, synergies)
   - Matchup difficulty (vs. each enemy)

2. **Oracle Model:** Train XGBoost to predict win probability change after item purchase
   - Input: Current state + proposed item
   - Output: ΔWin Prob (0.0 to +0.05, representing -5% to +5% swing)
   - Training target: Actual 5-minute post-purchase win probability change

3. **Q-Network Training:** Deep Q-Network learns action-value function Q(state, action)
   - Learn which item maximizes expected 5-minute win probability increase
   - Discount factor: 0.99 (future purchases matter)

### Evaluation Phase (Per-Game)

**Process:**

1. **Extract Recalls:** Identify all moments player enters base with gold
2. **Compute States:** For each recall, extract 30-dimensional state vector
3. **Optimal Action:** Use trained Q-Network to find optimal item
4. **Evaluate Actual:** Compare player's actual item to optimal
5. **Reward Calculation:**
   - Optimal item → E[Reward] via Q-Network (e.g., +0.03 win prob)
   - Actual item → E[Reward] via oracle model (e.g., +0.021 win prob)
   - Gap: 0.03 - 0.021 = +0.009 (player did almost as well)

### Build Adaptation Score

**Definition:** `(Actual Reward - Average Reward of All Possible Items at that State) / Max Possible Reward`

**Normalization:** 0-100 scale

- **80+:** Excellent item selection; nearly optimal every recall
- **60-80:** Good selections; minor inefficiencies
- **40-60:** Mixed approach; some good, some suboptimal
- **0-40:** Poor adaptation; not responding to enemy items

**Per-Recall Score:** For detailed feedback, each item purchase gets its own 0-100 score

## Applications

### Zone 6: Build & Ability Breakdown – Mythic Comparison

**Display:** Ghost line showing alternative mythic's expected damage

**Calculation:**

1. **Actual Mythic:** Your chosen mythic (e.g., Liandry's at 14:30)
2. **Counterfactual:** Simulate building alternative mythic (Luden's) instead
3. **Oracle Prediction:** Using oracle model, estimate damage curve with Luden's
4. **Comparison:** Liandry's +8% damage by 25min vs. Luden's (validated by game outcome)

**Insight:** *"Building Liandry's over Luden's was the right call — +8% damage advantage that accelerated your powerspikes."*

### Zone 6: Build Breakdown – Callouts & Timings

**Examples:**

- *"You bought Oblivion Orb (healing reduction) 9 minutes after enemy Soraka hit level 11 — too slow (-12% effectiveness). Earlier anti-heal would've crippled her heals for 30+ minutes."*

- *"Buying Void Staff at 24:00 (2 minutes after Soraka got her 2nd MR item) was optimally timed — gained +8% effectiveness vs. standard timing."*

## Advanced Analysis: Itemization Context

### 1. Enemy Adaptation

**Metric:** How well did you respond to enemy builds?

- Enemy built armor: Did you buy penetration on time?
- Enemy built healing: Did you buy anti-heal?
- Enemy built MR: Did you adapt damage type?

**Calculation:** For each enemy item, check if you purchased counter-item within 2 minutes

**Insight Example:**
- *"Enemy Soraka got Redemption at 18:00. You didn't buy anti-heal until 22:30 (4:30 delay). Typical optimal response: purchase within 2 minutes of detection (-2 efficiency points)."*

### 2. Spike Timing

**Metric:** Did you hit power spikes when most valuable?

- Early spikes (6-12 min): Roaming/laning pressure windows
- Mid spikes (12-20 min): Objective contestation windows
- Late spikes (20+ min): Teamfight windows

**Calculation:** For each spike, compare your item completion time vs. "optimal contest window"

**Insight Example:**
- *"Your Liandry's spike came at 14:30 — after baron contest (14:00) and mid-game skirmish (13:00). Gaining spike 30-60s earlier would've changed two fights (+3 efficiency points)."*

### 3. Full-Build Efficiency

**Overall Score:** Weighted combination of all per-recall scores

- Early game (0-14 min): Weight 0.3 (less important, less gold to spend)
- Mid game (14-25 min): Weight 0.5 (most important)
- Late game (25+ min): Weight 0.2 (less flexible, forced items)

**Formula:** `Final Score = 0.3 × Early + 0.5 × Mid + 0.2 × Late`

## Edge Cases & Limitations

### Known Limitations

- **Oracle Model Error:** Oracle accuracy ~80%; some suboptimal items appear optimal
- **Matchup-Specific:** Itemization depends on hidden factors (skill matchups) not captured in state
- **Meta Shifts:** Post-patch, optimal items change; model needs retraining

### Edge Cases

| Case | Handling |
|------|----------|
| Unusual items (tank support with AD item) | Penalize for off-meta, note as exception |
| Low-gold situations (forced buys) | Adjust expectations; fewer optimal items available |
| Perfect game (ahead entire time) | Normalize expectations; different optimal items when winning |
| Comeback game (behind, catching up) | Recognize anti-meta builds as potentially correct |

## Validation

**Accuracy Test:** Compare model's item recommendations vs. actual pro play

- Expected accuracy: ~60-70% (high variability in pro itemization)
- Outliers (unusual but optimal builds) are flagged

**Reward Prediction:** Compare oracle model's predicted damage gain vs. actual in-game damage change

- Expected correlation: >0.80
- Error analysis: Investigate outliers

## Boundaries

**Assumes:**
- Oracle model accurately predicts win probability change from items
- Q-Network correctly learns optimal itemization policy
- Game state representation (30 dimensions) adequately captures context

**Provides:**
- Per-recall item quality scores
- Overall build adaptation score
- Constructive itemization insights
