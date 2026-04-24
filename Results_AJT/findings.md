# EPL 2024-25 Season — Exploratory Analysis Findings

**Data:** EPL_24_25.csv · 380 matches · 20 teams · 26 referees  
**Season dates:** 16 Aug 2024 – 25 May 2025  
**Figures:** saved as PDFs in `/figures/`

---

## 0. Data Quality

| Issue | Detail |
|---|---|
| Bet&Win (BW) odds | 141 / 380 games missing (37%) |
| William Hill (WH) odds | 91 / 380 games missing (24%) |
| 1XBet odds | 9 / 380 games missing (2%) |
| Betfair Exchange | 3 / 380 games missing (<1%) |
| All core match stats | **Complete — no missing values** |

Core columns (goals, cards, shots, corners, fouls, referee) are fully populated. Missing data is isolated to certain bookmakers and does not affect any analysis below.

---

## 1a. Final Standings Table

| Pos | Team | P | W | D | L | GF | GA | GD | Pts |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Liverpool | 38 | 25 | 9 | 4 | 86 | 41 | +45 | **84** |
| 2 | Arsenal | 38 | 20 | 14 | 4 | 69 | 34 | +35 | **74** |
| 3 | Man City | 38 | 21 | 8 | 9 | 72 | 44 | +28 | **71** |
| 4 | Chelsea | 38 | 20 | 9 | 9 | 64 | 43 | +21 | **69** |
| 5 | Newcastle | 38 | 20 | 6 | 12 | 68 | 47 | +21 | **66** |
| 6 | Aston Villa | 38 | 19 | 9 | 10 | 58 | 51 | +7 | **66** |
| 7 | Nott'm Forest | 38 | 19 | 8 | 11 | 58 | 46 | +12 | **65** |
| 8 | Brighton | 38 | 16 | 13 | 9 | 66 | 59 | +7 | **61** |
| 9 | Bournemouth | 38 | 15 | 11 | 12 | 58 | 46 | +12 | **56** |
| 10 | Brentford | 38 | 16 | 8 | 14 | 66 | 57 | +9 | **56** |
| 11 | Fulham | 38 | 15 | 9 | 14 | 54 | 54 | 0 | **54** |
| 12 | Crystal Palace | 38 | 13 | 14 | 11 | 51 | 51 | 0 | **53** |
| 13 | Everton | 38 | 11 | 15 | 12 | 42 | 44 | -2 | **48** |
| 14 | West Ham | 38 | 11 | 10 | 17 | 46 | 62 | -16 | **43** |
| 15 | Man United | 38 | 11 | 9 | 18 | 44 | 54 | -10 | **42** |
| 16 | Wolves | 38 | 12 | 6 | 20 | 54 | 69 | -15 | **42** |
| 17 | Tottenham | 38 | 11 | 5 | 22 | 64 | 65 | -1 | **38** |
| 18 | Leicester | 38 | 6 | 7 | 25 | 33 | 80 | -47 | **25** |
| 19 | Ipswich | 38 | 4 | 10 | 24 | 36 | 82 | -46 | **22** |
| 20 | Southampton | 38 | 2 | 6 | 30 | 26 | 86 | -60 | **12** |

**Note:** Newcastle and Aston Villa both finished on 66 pts; Newcastle rank higher on goal differential (+21 vs +7).

**Key stories:**
- Liverpool won the title comfortably, 10 pts clear of Arsenal.
- Southampton (12 pts) had one of the worst EPL seasons on record.
- Tottenham scored 64 goals yet finished 17th — historically leaky mid-table performance.

---

## 1b. Home Advantage

| Metric | Value |
|---|---|
| Home wins | 155 / 380 (40.8%) |
| Draws | 93 / 380 (24.5%) |
| Away wins | 132 / 380 (34.7%) |
| χ² vs equal distribution | χ²=15.51, **p=0.0004** ✓ |

**Home wins significantly outnumber away wins.** The distribution is statistically different from equal (p < 0.001).

### Goals
- Avg home goals/game: **1.51** vs away: **1.42** (paired t-test p=0.337 — not significant)
- Total goals/game: **2.93**

Despite more wins, home teams don't score significantly more goals — the advantage may come from fewer draws being lost rather than outscoring opponents.

### Shots
- Home: **13.75** shots/game vs Away: **12.17** (t-test **p=0.0009** ✓)
- Home teams generate significantly more shots, suggesting territorial/attacking advantage.

### Cards
- Home yellows: **1.91** vs Away: **2.14** (t-test **p=0.008** ✓)
- Away teams receive significantly more yellow cards.
- Red cards are identical (0.068/game each, p=1.000).

**Conclusion:** Home advantage is real — teams win more often, generate more shots, and receive fewer yellow cards at home. The goal differential is directionally consistent but not statistically significant on its own.

**Figures:** `1b_result_distribution.pdf`, `1b_home_away_comparison.pdf`

---

## 1c. Team Profiles

### Top Attackers (goals/game)
| Team | GF/game | Shots/game | Conversion % |
|---|---|---|---|
| Liverpool | 2.26 | 17.1 | 37.2% |
| Man City | 1.90 | 16.0 | 33.2% |
| Arsenal | 1.82 | 14.4 | 36.7% |
| Newcastle | 1.79 | 13.8 | 39.1% |

### Best Defences (goals conceded/game)
| Team | GA/game |
|---|---|
| Arsenal | 0.89 |
| Liverpool | 1.08 |
| Man City | 1.16 |
| Chelsea | 1.13 |

### Worst Defences
| Team | GA/game |
|---|---|
| Southampton | 2.26 |
| Ipswich | 2.16 |
| Leicester | 2.11 |

### Notable Observations
- **Newcastle** had the highest shot conversion rate (39.1%) despite being 5th — very clinical.
- **Southampton** had the worst attack (0.68 GF/game) AND worst defence (2.26 GA/game).
- **Tottenham** scored 1.68 goals/game but conceded at the same rate — a "glass cannon" side.
- **Brentford** had surprisingly low shots for/game (11.6) but scored efficiently (35.9%).

**Figures:** `1c_attack_defence_scatter.pdf`, `1c_conversion_rate.pdf`

---

## 1d. Referee Analysis

Referees with 10+ games included (18 qualify, out of 26 total).

### Total Cards per Game (highest to lowest)
| Referee | Games | Total Y/game | HY/game | AY/game | AY−HY bias |
|---|---|---|---|---|---|
| J Brooks | 17 | 5.06 | 2.82 | 2.24 | **−0.59** (favours home) |
| S Hooper | 23 | 4.70 | 2.39 | 2.30 | −0.09 |
| S Barrott | 23 | 4.61 | 2.09 | 2.52 | +0.44 |
| M Oliver | 25 | 4.32 | 1.80 | 2.52 | +0.72 |
| A Madley | 20 | 4.30 | 1.85 | 2.45 | +0.60 |
| … | | | | | |
| A Taylor | 30 | 2.93 | 1.33 | 1.60 | +0.27 |
| M Salisbury | 15 | 2.87 | 1.47 | 1.40 | −0.07 |

### Statistically Significant Card Bias
| Referee | n | AY−HY | p-value | |
|---|---|---|---|---|
| **D England** | 19 | +0.789 | 0.031 | ** away-biased |
| **M Oliver** | 25 | +0.720 | 0.019 | ** away-biased |
| J Brooks | 17 | −0.588 | 0.056 | * home-biased (marginal) |

- **Overall** (all 380 games): away teams receive +0.24 more yellows/game on average (p=0.008).
- Only **D England** and **M Oliver** show individually significant away-card bias at α=0.05.
- **J Brooks** trends toward home-team card bias (more cards for home teams) but is marginal.
- Note: with 18 tests, 1–2 false positives expected at α=0.05 — results should be interpreted cautiously.

**Figure:** `1d_referee_cards.pdf`

---

## 2a. Half-Time → Full-Time Result Matrix

|  | FT: Home Win | FT: Draw | FT: Away Win |
|---|---|---|---|
| **HT: Home Win** | 97 (68.3%) | 30 (21.1%) | 15 (10.6%) |
| **HT: Draw** | 44 (32.6%) | 45 (33.3%) | 46 (34.1%) |
| **HT: Away Win** | 14 (13.6%) | 18 (17.5%) | 71 (68.9%) |

**Key findings:**
- **HT leaders are very likely to win:** ~69% of half-time leaders win the match.
- **Draws at HT are almost perfectly balanced** for FT outcomes (~1/3 each direction) — the second half is essentially a coin flip from an even HT.
- **Comebacks are rare:** only ~11–14% of trailing teams at HT go on to win.
- The matrix is nearly symmetric (HT Home and HT Away have near-identical conversion rates ~69%).

**Figure:** `2a_ht_ft_matrix.pdf`

---

## 2b. Form Analysis (5-game rolling average pts/game)

Key trends per matchweek:

| Period | Hot Teams | Cold Teams |
|---|---|---|
| MW 5–12 | Liverpool (dominant), Man City, Arsenal | Wolves, Southampton |
| MW 13–17 | Chelsea, Nott'm Forest, Newcastle | Man City (dip), Leicester, Southampton |
| MW 20–26 | Arsenal, Liverpool, Bournemouth | Tottenham, Wolves, Ipswich |
| MW 27–31 | Crystal Palace, Aston Villa, Wolves (surprise) | Brighton, Southampton, Leicester |
| MW 32–36 | Man City (resurgent), Brentford, Brighton | Tottenham, Ipswich, Southampton |

**Notable patterns:**
- **Liverpool** dominated form charts for the majority of the season (MW 5–26), consistent with their title win.
- **Wolves** appeared in both hot (MW 30–33) AND cold lists (MW 5–13) — a dramatic mid-season turnaround.
- **Southampton** appeared in the worst-3 for nearly every matchweek — consistently poor all season.
- **Man City** showed two distinct dips (MW 13–15, MW 17) before rallying late.

**Figure:** `2b_form_lines.pdf`

---

## 2c. Corners

### Corners For/Against per Game
| Team | For | Against |
|---|---|---|
| Man City | 6.66 | 3.26 |
| Liverpool | 6.66 | 3.71 |
| Arsenal | 6.61 | 3.11 |
| Tottenham | 6.39 | 5.42 |
| Chelsea | 6.21 | 3.71 |
| … | | |
| Leicester | 3.71 | 6.08 |
| Ipswich | 3.82 | 6.63 |
| Wolves | 3.92 | 5.74 |

**Top 3 teams (Arsenal, Liverpool, Man City) dominate corners both for and against** — they control territory and limit opponent attacks. Southampton, Ipswich, and Leicester concede the most corners.

### Do corners predict results?

- Pearson correlation between corner differential (HC − AC) and result (Home=+1, Draw=0, Away=−1): **r = 0.117, p = 0.023**
- Corners are a **statistically significant but weak predictor** of match outcome. A team winning the corner battle is slightly more likely to win, but corners explain only ~1.4% of variance in result (r²=0.014).

**Figures:** `2c_corners.pdf`, `2c_corner_goal_scatter.pdf`

---

## 3a. Match Prediction — Bet365 Implied Probabilities

**Method:** Convert Bet365 pre-match odds (B365H/D/A) to implied probabilities (1/odds), renormalise to sum to 100% to remove the bookmaker margin, then predict the outcome with the highest probability.

| Model | Accuracy |
|---|---|
| **Bet365 renormalised** | **53.9%** |
| Random (equal 1/3) | 33.3% |
| Majority class (always predict H) | 40.8% |

**Average bookmaker margin:** 5.53%

### Per-Class Performance
| Actual Result | Predicted Correctly | n |
|---|---|---|
| Home Win (H) | 83.9% | 155 |
| Draw (D) | 0.0% | 93 |
| Away Win (A) | 56.8% | 132 |

**Critical finding:** The model **never predicts a draw.** Bet365 rarely prices draws as the highest-probability outcome, so renormalized probabilities always favour H or A. As a result:
- Draws are predicted 0% correctly.
- This explains why accuracy (53.9%) is well above random but falls short of a theoretical ceiling.

### Confusion Matrix
|  | Pred H | Pred D | Pred A |
|---|---|---|---|
| **Act H** | 130 | 0 | 25 |
| **Act D** | 59 | 0 | 34 |
| **Act A** | 57 | 0 | 75 |

**Bet365 is significantly better than random** (+20.6pp over random, +13.1pp over majority-class baseline), but the complete failure to predict draws is a structural limitation when using argmax on implied probabilities.

**Figure:** `3a_prediction_accuracy.pdf`

---

## Summary of Key Findings

1. **Liverpool dominated** — won the title with 84 pts, 10 clear of Arsenal.
2. **Home advantage exists** — significantly more home wins (41%) vs away (35%), more shots at home, fewer yellow cards.
3. **HT result is highly predictive** — 69% of teams leading at HT go on to win.
4. **Draws are hard to predict** — no model (including Bet365) reliably identifies draws.
5. **Bet365 outperforms random by ~21pp** but misses all draws; accuracy = 53.9%.
6. **Corners weakly predict outcomes** (r=0.12, p=0.02) — top teams (Arsenal/Liverpool/City) dominate corners.
7. **D England and M Oliver** show statistically significant away-card bias.
8. **Southampton** was historically poor — worst in nearly every metric all season.
