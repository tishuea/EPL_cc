# EPL 2024-25 — Agent 2 Findings
**Role:** Review of Agent 1's analysis and improvement/completion.  
**Data:** EPL_24_25.csv · 380 matches · 20 teams · 26 referees  
**Season dates:** 16 Aug 2024 – 25 May 2025  
**Figures:** saved to `/figures_2/`

---

## Scope of This Document

This document covers:
1. An explicit review of Agent 1's work — what was done correctly, what was incomplete or erroneous.
2. The **completed missing analysis** (Section 3b, Bookmaker Accuracy).
3. **Corrections** to Agent 1's statistical methodology.
4. **Additional analyses** that add value beyond the original brief.

---

## Review of Agent 1's Work

### What Agent 1 did well
- Standings table, home advantage, team profiles, referee analysis, HT/FT matrix, form analysis, corners, and Bet365 prediction (3a) were all structurally sound.
- Statistical tests (chi-square, paired t-tests) were used appropriately for most analyses.
- The findings document was clearly written and the key stories (Liverpool title, Southampton relegation, Bet365 never predicting draws) were correctly identified.
- Agent 1 correctly noted the multiple-testing concern in the referee analysis, even though it was not addressed computationally.

### Issues Identified and Addressed

| # | Issue | Severity | Resolution |
|---|---|---|---|
| 1 | **Section 3b entirely missing** (Bookmaker accuracy, Bet365 vs WH P&L) | High | Implemented below |
| 2 | **Corner correlation method**: Agent 1 used `pointbiserialr` (for binary variables) on a 3-level ordinal match result. Spearman is the appropriate test, and **it reverses the conclusion** (p=0.082, not significant). | High | Corrected below |
| 3 | **Referee multiple testing**: 18 simultaneous t-tests were run with no correction; Agent 1 flagged this in text but did not apply any correction. After Bonferroni and BH-FDR, **neither D England nor M Oliver remain significant**. | Medium | Corrected below |
| 4 | **Path references** in analysis.py used deprecated `/Claude_EPL/` paths; results.pkl would not have saved. | Low | N/A (code runs correctly from `/EPL_cc/`) |

---

## 3b. Bookmaker Accuracy — Bet365 vs William Hill *(MISSING FROM AGENT 1)*

**Method:** Bet365 odds are available for all 380 games; William Hill (WH) odds are available for 289/380 (76%). For a fair head-to-head comparison, all metrics below are computed on the **289 shared games only**.

Implied probabilities computed as 1/decimal_odds, renormalised to sum to 100% (removing the bookmaker overround). The outcome with the highest renormalised probability is predicted. P&L is calculated as: +£(decimal_odds − 1) if correct, −£1 if incorrect, assuming a flat £1 stake per game on the predicted outcome.

| Metric | Bet365 | William Hill |
|---|---|---|
| Bookmaker overround | 5.46% | 5.22% |
| Prediction accuracy | 51.9% | **52.2%** |
| Random baseline | 33.3% | — |
| Majority-class baseline | 39.4% | — |
| Total P&L (289 games, £1/game) | −£28.82 | **−£23.90** |
| ROI per game | −9.97% | **−8.27%** |
| Draws predicted | 0 | 0 |

### Per-class accuracy (shared games)

| Actual Result | Bet365 | William Hill | n |
|---|---|---|---|
| Home Win (H) | 80.7% | 80.7% | 114 |
| Draw (D) | **0.0%** | **0.0%** | 72 |
| Away Win (A) | 56.3% | 57.3% | 103 |

### Key Findings

1. **William Hill is modestly better on both accuracy and P&L** on the shared sample, despite a slightly lower overround. The difference is small and likely within sampling noise (no formal significance test performed — see limitations).
2. **Both bookmakers lose money for the bettor**: approximately −9% to −8% ROI per game, consistent with a ~5% bookmaker margin baked in.
3. **Neither bookmaker ever predicts a draw** (highest implied probability is never assigned to the draw outcome). This is the same structural failure identified in Section 3a: draws remain systematically unpredictable from raw argmax on implied probabilities.
4. **William Hill should be preferred** if you must bet using this naive strategy — it loses approximately £4.92 less over 289 games (£23.90 vs £28.82).

**Limitations:** The 91 games where WH odds are missing are not a random sample — they may be earlier-season games when WH data collection started late. Any systematic difference in those games' outcomes could bias the comparison. A more rigorous comparison would require examining *why* those games are missing.

**Figure:** `3b_bookmaker_comparison.pdf`

---

## Corrected 2c. Corner Correlation

Agent 1 reported: *"Corners are a statistically significant but weak predictor of match outcome (r=0.117, p=0.023)"*, using `scipy.stats.pointbiserialr`.

**Problem:** `pointbiserialr` is designed for a **binary** variable. The match result encoded as H=+1, D=0, A=−1 is a **3-level ordinal** variable. Pearson and pointbiserialr give numerically identical results here because both assume the outcome is continuous with equal spacing between levels. For a 3-level ordinal outcome, **Spearman rank correlation** is the appropriate non-parametric test.

| Method | r | p |
|---|---|---|
| Pearson / pointbiserialr (Agent 1) | 0.117 | 0.023 ✓ |
| **Spearman (correct)** | **0.089** | **0.082 ✗** |

**The Spearman result (p=0.082) is not significant at α=0.05.**

Additional confirmation: a chi-square test of whether winning the corner battle (HC > AC) vs losing it predicts the FTR shows χ²=2.13, p=0.345 — clearly non-significant.

**Revised conclusion:** There is no statistically significant relationship between corner differential and match outcome when the appropriate test is used. Agent 1's claim that "corners explain ~1.4% of outcome variance" and are a "real but weak predictor" is not supported. The corner differential vs goal differential Pearson correlation (r=0.121, p=0.018) remains significant, but this measures a different thing — corner dominance is associated with goal dominance, but not independently with the match result after accounting for the ordinal scale.

**Figures:** (existing Agent 1 figures remain valid as visualization; the interpretive label should be updated)

---

## Corrected 1d. Referee Analysis — Multiple Testing

Agent 1 ran 18 paired t-tests (one per referee with ≥10 games) and reported D England (p=0.031) and M Oliver (p=0.019) as statistically significant. Agent 1 correctly noted: *"with 18 tests, 1–2 false positives expected at α=0.05"* but did not apply any correction.

Results after correction:

| Referee | n | AY−HY | p (raw) | p (Bonferroni) | p (BH-FDR) | Significant? |
|---|---|---|---|---|---|---|
| D England | 19 | +0.789 | 0.031 | 0.566 | 0.283 | **No** |
| M Oliver | 25 | +0.720 | 0.019 | 0.340 | 0.283 | **No** |
| All others | — | — | >0.05 | — | — | No |

**After applying Bonferroni or Benjamini-Hochberg FDR correction, zero individual referees show statistically significant card bias.** The two referees Agent 1 named as significant (D England, M Oliver) do not survive multiple-testing correction.

**What does remain significant:** The *overall* league-wide effect (all 380 games) is robust: away teams receive +0.239 more yellow cards per game on average (paired t-test: t=2.68, p=0.0077). This is a genuine systemic effect across all referees, but cannot be traced to any single referee when testing at the individual level.

**Interpretation:** The overall away-card bias is likely a genuine home-advantage effect (referees are more lenient with home teams), but it is distributed across all referees rather than concentrated in a few. The specific naming of individual referees as biased is not statistically warranted.

**Figure:** `1d_referee_improved.pdf`

---

## Additional A. Home Advantage by Team

Agent 1 established overall home advantage but did not examine whether it varies by team.

| Rank | Team | Home PPG | Away PPG | HA Diff |
|---|---|---|---|---|
| 1 | Aston Villa | 2.11 | 1.37 | +0.74 |
| 2 | Chelsea | 2.16 | 1.47 | +0.68 |
| 3 | Man City | 2.21 | 1.53 | +0.68 |
| 4 | Newcastle | 2.00 | 1.47 | +0.53 |
| 5 | Liverpool | 2.42 | 2.00 | +0.42 |
| … | | | | |
| 17 | Crystal Palace | 1.32 | 1.47 | −0.16 |
| 18 | West Ham | 1.05 | 1.21 | −0.16 |
| 19 | Fulham | 1.37 | 1.47 | −0.11 |
| 20 | **Ipswich** | **0.37** | **0.79** | **−0.42** |

**Key findings:**
- **Ipswich had a strongly negative home effect**: they averaged 0.79 PPG away but only 0.37 at home — their worst results came at Portman Road. This is anomalous and worth investigating further (e.g., was the stadium atmosphere a negative factor for a newly promoted side?).
- **5 teams had zero or negative home advantage** (Ipswich, Crystal Palace, West Ham, Fulham, Nott'm Forest). For these teams the "home advantage" narrative does not apply.
- **Aston Villa had the largest home advantage** despite finishing 6th — they were a much better team in front of their home crowd.
- Even the champion Liverpool had a meaningful home/away split (+0.42 PPG), suggesting home advantage persists at the top of the table.

**Limitation:** With only 19 home games per team, individual estimates are noisy. The team-level home advantage differences should be interpreted cautiously; none have been formally tested for significance.

**Figure:** `ha_by_team.pdf`

---

## Additional B. Goals Distribution — Poisson Test

Football scoring is classically modelled with Poisson-distributed goals (independent goals, constant rate). This is the foundation for many betting models. We test the fit formally using a chi-square goodness-of-fit test (with df = bins − 2 to account for the estimated λ).

| | Mean (λ) | χ² | df | p-value | Conclusion |
|---|---|---|---|---|---|
| Home goals | 1.513 | 7.62 | 6 | 0.268 | Cannot reject Poisson |
| Away goals | 1.421 | 10.19 | 6 | 0.117 | Cannot reject Poisson |

**The Poisson distribution is an acceptable model for EPL goal scoring in 2024-25.** Neither home nor away goals significantly deviate from a Poisson distribution, consistent with the standard assumption in football analytics (Dixon-Coles and related models). This validates the use of Poisson-based models for future probability modelling.

**Note:** This test uses all 380 games independently. In practice, goals are not truly i.i.d. (team quality varies, and home/away goals within a game are slightly negatively correlated — teams defending a lead score fewer, concede more). The Dixon-Coles correction for low-scoring games (0-0, 1-0, 0-1, 1-1) could be tested as a follow-on.

**Figure:** `goals_poisson.pdf`

---

## Improved 2b. Form Visualization

Agent 1's form plot drew all 20 team lines at equal weight, making it difficult to follow individual teams. The improved version greys out background teams and highlights key teams with thicker, coloured lines.

Teams highlighted: Liverpool (champion), Southampton (relegated), Arsenal (2nd), Nott'm Forest (7th, surprise qualifier), Man City (3rd).

The best/worst form matchweek table (reproduced in analysis output) is consistent with Agent 1's findings:
- Liverpool dominated the top-3 from MW 5 through MW 26 before sharing the lead.
- Southampton appeared in the worst-3 for nearly every matchweek.
- Nott'm Forest was in the top-3 in MW 11, 12, 16, 17, 20 — consistent with their surprising 7th-place finish.

**Figure:** `2b_form_improved.pdf`

---

## Summary of Agent 2 Contributions

| Section | Contribution |
|---|---|
| **3b (new)** | Bookmaker comparison implemented: WH edges out B365 on accuracy (52.2% vs 51.9%) and P&L (−£23.90 vs −£28.82 over 289 games). Both lose money. William Hill preferred for this strategy. |
| **2c (correction)** | Spearman correlation (r=0.089, p=0.082) replaces Agent 1's Pearson/pointbiserialr result (p=0.023). **Corners do not significantly predict match outcomes.** |
| **1d (correction)** | After Bonferroni and BH-FDR correction: **zero individual referees are significantly biased** (D England and M Oliver do not survive). The league-wide effect remains (p=0.008). |
| **Home by team (new)** | Ipswich had *negative* home advantage (−0.42 PPG). 5 teams showed no home benefit. |
| **Poisson test (new)** | Goals fit a Poisson distribution (home p=0.27, away p=0.12), validating standard modelling assumptions. |
| **Improved form plot** | Key teams highlighted; grey background for clarity. |

---

## Remaining Uncertainties and Future Work

1. **Draws remain unpredictable**: Neither Bet365 nor WH ever predicts a draw using naive argmax. A model trained to identify draw-likely games (low expected goals, even match-ups) could add substantial value. The 24.5% draw rate represents significant unexplained variance.

2. **WH missing data**: 91 games (24%) have no WH odds. Understanding whether these are systematically different games would strengthen the 3b comparison.

3. **Poisson independence assumption**: Home and away goals within a game are correlated (Dixon-Coles adjustment). Testing this formally, and fitting a bivariate Poisson or Dixon-Coles model, is a natural next step.

4. **Referee analysis**: Individual referee bias is not detectable with typical season sample sizes (10-30 games per ref). Multi-season analysis would provide the statistical power needed to identify genuinely biased officials.

5. **Ipswich home disadvantage**: With only 19 home games, this is a noisy estimate. Whether this reflects a structural factor (promoted-side crowd pressure, travel fatigue patterns) or is sampling noise should be examined with multiple seasons.
