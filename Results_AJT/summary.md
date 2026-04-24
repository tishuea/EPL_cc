# EPL 2024-25 — Executive Summary

**380 matches · 20 teams · 26 referees · Season: Aug 2024 – May 2025**

## Standings
Liverpool won the title (84 pts, +45 GD), 10 points clear of Arsenal. Southampton were relegated with just 12 pts — one of the worst EPL seasons on record.

## Home Advantage
Home advantage is statistically real: 40.8% home wins vs 34.7% away (χ²=15.5, p<0.001). Home teams produce significantly more shots (+1.6/game, p<0.001) and receive fewer yellow cards (−0.24/game, p=0.008). The goal differential is directional but not significant in isolation.

## Half-Time → Full-Time
Teams leading at HT win ~69% of the time. A draw at HT is effectively a coin flip — outcomes split nearly equally three ways. Comebacks (trailing at HT, winning at FT) happen only ~12% of the time.

## Form
Liverpool led the form charts for most of the season. Southampton appeared in the worst-3 almost every matchweek. Wolves had the most dramatic turnaround, moving from cold in autumn to hot in spring.

## Referees
Away teams receive 0.24 more yellow cards/game on average (significant overall). Individually, D England (p=0.031) and M Oliver (p=0.019) show significant away-card bias. J Brooks trends toward home-card bias (p=0.056).

## Corners
Top teams (Arsenal, Liverpool, Man City) average 6.6+ corners/game. Corners have a weak but real correlation with result (r=0.12, p=0.02), explaining ~1.4% of outcome variance.

## Betting Prediction (Bet365)
Renormalised Bet365 odds predict match outcome with 53.9% accuracy — vs 33.3% random and 40.8% majority-class. The model never predicts draws (highest implied probability is almost always H or A), leaving 93 draws (24.5% of games) completely unaddressed.

## Figures Generated
- `1b_result_distribution.pdf` — Home/draw/away win counts
- `1b_home_away_comparison.pdf` — Goals, yellow cards, shots: home vs away
- `1c_attack_defence_scatter.pdf` — GF/game vs GA/game by team
- `1c_conversion_rate.pdf` — Shot-on-target conversion % by team
- `1d_referee_cards.pdf` — Yellow card rates by referee
- `2a_ht_ft_matrix.pdf` — HT→FT result transition matrix (count + %)
- `2b_form_lines.pdf` — 5-game rolling form for all 20 teams
- `2c_corners.pdf` — Corners for/against per game by team
- `2c_corner_goal_scatter.pdf` — Corner differential vs goal differential
- `3a_prediction_accuracy.pdf` — Model accuracy comparison
