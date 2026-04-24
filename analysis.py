"""
EPL 2024-25 Season Full Exploratory Analysis
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

FIGURES = '/Users/averytishue/Claude_EPL/figures'
DATA = '/Users/averytishue/Claude_EPL/EPL_24_25.csv'

# ── Load ──────────────────────────────────────────────────────────────────────
df = pd.read_csv(DATA)
print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")

# ── 1. EDA: missing values, summary stats ─────────────────────────────────────
print("\n=== MISSING VALUES ===")
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(1)
missing_summary = pd.DataFrame({'missing': missing, 'pct': missing_pct})
missing_summary = missing_summary[missing_summary['missing'] > 0].sort_values('pct', ascending=False)
print(missing_summary.to_string())

core_cols = ['Div','Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HTHG','HTAG','HTR',
             'Referee','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR']

print("\n=== CORE COLUMN DTYPES ===")
print(df[core_cols].dtypes)

print("\n=== SUMMARY STATS (core numeric) ===")
num_core = ['FTHG','FTAG','HTHG','HTAG','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR']
print(df[num_core].describe().round(2).to_string())

# Check date range
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
df = df.sort_values('Date').reset_index(drop=True)
print(f"\nDate range: {df['Date'].min().date()} → {df['Date'].max().date()}")
print(f"Total matches: {len(df)}")
print(f"Unique teams: {sorted(set(df['HomeTeam']) | set(df['AwayTeam']))}")
print(f"Unique referees: {df['Referee'].nunique()}")

# FTR distribution
print("\n=== FULL TIME RESULT DISTRIBUTION ===")
print(df['FTR'].value_counts())
print(df['FTR'].value_counts(normalize=True).round(3))

# Goals
print("\n=== GOALS PER GAME ===")
df['total_goals'] = df['FTHG'] + df['FTAG']
print(f"Avg total goals/game: {df['total_goals'].mean():.3f}")
print(f"Avg home goals/game:  {df['FTHG'].mean():.3f}")
print(f"Avg away goals/game:  {df['FTAG'].mean():.3f}")

# ── 1a. STANDINGS TABLE ───────────────────────────────────────────────────────
print("\n\n=== 1a. STANDINGS TABLE ===")
teams = sorted(set(df['HomeTeam']) | set(df['AwayTeam']))
records = []
for team in teams:
    home = df[df['HomeTeam'] == team]
    away = df[df['AwayTeam'] == team]

    hp = home['FTR'].map({'H': 3, 'D': 1, 'A': 0}).sum()
    ap = away['FTR'].map({'H': 0, 'D': 1, 'A': 3}).sum()
    pts = hp + ap

    hw = (home['FTR'] == 'H').sum()
    hd = (home['FTR'] == 'D').sum()
    hl = (home['FTR'] == 'A').sum()
    aw = (away['FTR'] == 'A').sum()
    ad = (away['FTR'] == 'D').sum()
    al = (away['FTR'] == 'H').sum()

    gf = home['FTHG'].sum() + away['FTAG'].sum()
    ga = home['FTAG'].sum() + away['FTHG'].sum()
    gd = gf - ga

    played = len(home) + len(away)
    records.append({
        'Team': team, 'P': played,
        'W': hw + aw, 'D': hd + ad, 'L': hl + al,
        'GF': gf, 'GA': ga, 'GD': gd, 'Pts': pts
    })

standings = pd.DataFrame(records)
standings = standings.sort_values(['Pts', 'GD', 'Team'], ascending=[False, False, True]).reset_index(drop=True)
standings.index += 1
print(standings.to_string())

# ── 1b. HOME ADVANTAGE ────────────────────────────────────────────────────────
print("\n\n=== 1b. HOME ADVANTAGE ===")
ftr_counts = df['FTR'].value_counts()
n = len(df)
print(f"Home wins: {ftr_counts.get('H',0)} ({ftr_counts.get('H',0)/n*100:.1f}%)")
print(f"Draws:     {ftr_counts.get('D',0)} ({ftr_counts.get('D',0)/n*100:.1f}%)")
print(f"Away wins: {ftr_counts.get('A',0)} ({ftr_counts.get('A',0)/n*100:.1f}%)")

# Chi-squared test vs equal probability
obs = [ftr_counts.get('H',0), ftr_counts.get('D',0), ftr_counts.get('A',0)]
chi2, p_val = stats.chisquare(obs)
print(f"\nChi-squared test vs equal distribution: χ²={chi2:.2f}, p={p_val:.4f}")

# Goals
print(f"\nAvg home goals: {df['FTHG'].mean():.3f}")
print(f"Avg away goals: {df['FTAG'].mean():.3f}")
t_stat, p_goals = stats.ttest_rel(df['FTHG'], df['FTAG'])
print(f"Paired t-test home vs away goals: t={t_stat:.3f}, p={p_goals:.4f}")

# Cards
df['total_HY'] = df['HY']
df['total_AY'] = df['AY']
print(f"\nAvg home yellows: {df['HY'].mean():.3f}")
print(f"Avg away yellows: {df['AY'].mean():.3f}")
t_y, p_y = stats.ttest_rel(df['HY'], df['AY'])
print(f"Paired t-test yellow cards: t={t_y:.3f}, p={p_y:.4f}")

print(f"\nAvg home reds: {df['HR'].mean():.3f}")
print(f"Avg away reds: {df['AR'].mean():.3f}")
t_r, p_r = stats.ttest_rel(df['HR'], df['AR'])
print(f"Paired t-test red cards: t={t_r:.3f}, p={p_r:.4f}")

# Shots
print(f"\nAvg home shots: {df['HS'].mean():.3f}")
print(f"Avg away shots: {df['AS'].mean():.3f}")
t_s, p_s = stats.ttest_rel(df['HS'], df['AS'])
print(f"Paired t-test shots: t={t_s:.3f}, p={p_s:.4f}")

# Fig: result distribution bar
fig, ax = plt.subplots(figsize=(6, 4))
labels = ['Home Win', 'Draw', 'Away Win']
vals = [ftr_counts.get('H', 0), ftr_counts.get('D', 0), ftr_counts.get('A', 0)]
colors = ['#2196F3', '#9E9E9E', '#F44336']
bars = ax.bar(labels, vals, color=colors, edgecolor='black', linewidth=0.5)
for bar, v in zip(bars, vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, str(v), ha='center', fontsize=11)
ax.set_ylabel('Number of Matches')
ax.set_title('EPL 2024-25: Match Result Distribution')
ax.set_ylim(0, max(vals) * 1.15)
plt.tight_layout()
plt.savefig(f'{FIGURES}/1b_result_distribution.pdf')
plt.close()
print(f"Saved 1b_result_distribution.pdf")

# Fig: avg goals and cards home vs away
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
metrics = [
    ('Goals', df['FTHG'].mean(), df['FTAG'].mean()),
    ('Yellow Cards', df['HY'].mean(), df['AY'].mean()),
    ('Shots', df['HS'].mean(), df['AS'].mean()),
]
for ax, (label, h_val, a_val) in zip(axes, metrics):
    ax.bar(['Home', 'Away'], [h_val, a_val], color=['#2196F3', '#F44336'], edgecolor='black', linewidth=0.5)
    ax.set_title(f'Avg {label} per Game')
    ax.set_ylabel(label)
plt.suptitle('Home vs Away Comparison – EPL 2024-25', fontsize=13)
plt.tight_layout()
plt.savefig(f'{FIGURES}/1b_home_away_comparison.pdf')
plt.close()
print("Saved 1b_home_away_comparison.pdf")

# ── 1c. TEAM PROFILES ────────────────────────────────────────────────────────
print("\n\n=== 1c. TEAM PROFILES ===")
team_stats = []
for team in teams:
    home = df[df['HomeTeam'] == team]
    away = df[df['AwayTeam'] == team]
    played = len(home) + len(away)
    if played == 0:
        continue
    gf = home['FTHG'].sum() + away['FTAG'].sum()
    ga = home['FTAG'].sum() + away['FTHG'].sum()
    shots_f = home['HS'].sum() + away['AS'].sum()
    shots_a = home['AS'].sum() + away['HS'].sum()
    sot_f   = home['HST'].sum() + away['AST'].sum()
    goals_f = gf
    conversion = goals_f / sot_f * 100 if sot_f > 0 else 0

    team_stats.append({
        'Team': team, 'P': played,
        'GF_pg': gf / played, 'GA_pg': ga / played,
        'Shots_F_pg': shots_f / played, 'Shots_A_pg': shots_a / played,
        'SOT_F_pg': sot_f / played,
        'Conversion_pct': conversion,
    })

ts = pd.DataFrame(team_stats)
print(ts[['Team','GF_pg','GA_pg','Shots_F_pg','Shots_A_pg','Conversion_pct']].sort_values('GF_pg', ascending=False).round(3).to_string())

# Attack vs Defence scatter
fig, ax = plt.subplots(figsize=(10, 8))
ax.scatter(ts['GA_pg'], ts['GF_pg'], s=60, alpha=0.7, color='steelblue', edgecolors='navy', linewidths=0.5)
for _, row in ts.iterrows():
    ax.annotate(row['Team'], (row['GA_pg'], row['GF_pg']), fontsize=7, ha='center', va='bottom', xytext=(0, 4), textcoords='offset points')
ax.axhline(ts['GF_pg'].mean(), color='gray', linestyle='--', linewidth=0.8, label='Avg GF/game')
ax.axvline(ts['GA_pg'].mean(), color='gray', linestyle=':', linewidth=0.8, label='Avg GA/game')
ax.set_xlabel('Goals Conceded per Game (lower = better defence)')
ax.set_ylabel('Goals Scored per Game (higher = better attack)')
ax.set_title('EPL 2024-25: Attack vs Defence Profile')
ax.legend(fontsize=8)
plt.tight_layout()
plt.savefig(f'{FIGURES}/1c_attack_defence_scatter.pdf')
plt.close()
print("Saved 1c_attack_defence_scatter.pdf")

# Conversion rate bar
fig, ax = plt.subplots(figsize=(12, 5))
ts_sorted = ts.sort_values('Conversion_pct', ascending=False)
ax.bar(ts_sorted['Team'], ts_sorted['Conversion_pct'], color='steelblue', edgecolor='navy', linewidth=0.5)
ax.set_ylabel('Shots on Target → Goal Conversion %')
ax.set_title('EPL 2024-25: Shot Conversion Rate (Goals / Shots on Target)')
plt.xticks(rotation=45, ha='right', fontsize=8)
plt.tight_layout()
plt.savefig(f'{FIGURES}/1c_conversion_rate.pdf')
plt.close()
print("Saved 1c_conversion_rate.pdf")

# ── 1d. REFEREES ─────────────────────────────────────────────────────────────
print("\n\n=== 1d. REFEREES ===")
ref_stats = []
for ref, grp in df.groupby('Referee'):
    n_games = len(grp)
    if n_games < 10:
        continue
    avg_hy = grp['HY'].mean()
    avg_ay = grp['AY'].mean()
    avg_hr = grp['HR'].mean()
    avg_ar = grp['AR'].mean()
    avg_total_y = (grp['HY'] + grp['AY']).mean()
    # Card bias: positive = more yellow to away team
    card_bias = (grp['AY'] - grp['HY']).mean()
    ref_stats.append({
        'Referee': ref, 'Games': n_games,
        'Avg_HY': avg_hy, 'Avg_AY': avg_ay,
        'Avg_HR': avg_hr, 'Avg_AR': avg_ar,
        'Total_Y_pg': avg_total_y,
        'Card_Bias_AY_minus_HY': card_bias,
    })

ref_df = pd.DataFrame(ref_stats).sort_values('Total_Y_pg', ascending=False)
print(ref_df.round(3).to_string())

# Statistical test: for each qualifying ref, t-test on HY vs AY
print("\n--- Card Bias t-tests (paired HY vs AY per game) ---")
for ref, grp in df.groupby('Referee'):
    if len(grp) < 10:
        continue
    t, p = stats.ttest_rel(grp['AY'], grp['HY'])
    sig = '***' if p < 0.01 else ('**' if p < 0.05 else ('*' if p < 0.1 else ''))
    print(f"  {ref:<25} n={len(grp):3d}  AY-HY={grp['AY'].mean()-grp['HY'].mean():+.3f}  t={t:.2f}  p={p:.3f} {sig}")

# Overall test across all games
t_all, p_all = stats.ttest_rel(df['AY'], df['HY'])
print(f"\nAll games: AY-HY={df['AY'].mean()-df['HY'].mean():+.3f}, t={t_all:.2f}, p={p_all:.4f}")

# Fig: referee card rates
fig, ax = plt.subplots(figsize=(12, 5))
x = np.arange(len(ref_df))
w = 0.35
ax.bar(x - w/2, ref_df['Avg_HY'], w, label='Avg Home Yellows', color='#2196F3', edgecolor='navy', linewidth=0.5)
ax.bar(x + w/2, ref_df['Avg_AY'], w, label='Avg Away Yellows', color='#F44336', edgecolor='darkred', linewidth=0.5)
ax.set_xticks(x)
ax.set_xticklabels(ref_df['Referee'], rotation=45, ha='right', fontsize=8)
ax.set_ylabel('Avg Yellow Cards per Game')
ax.set_title('EPL 2024-25: Referee Yellow Card Rates (≥10 games)')
ax.legend()
plt.tight_layout()
plt.savefig(f'{FIGURES}/1d_referee_cards.pdf')
plt.close()
print("Saved 1d_referee_cards.pdf")

# ── 2a. HT → FT MATRIX ───────────────────────────────────────────────────────
print("\n\n=== 2a. HALF TIME → FULL TIME RESULT MATRIX ===")
ht_ft = pd.crosstab(df['HTR'], df['FTR'])
ht_ft = ht_ft.reindex(index=['H','D','A'], columns=['H','D','A'])
print("Rows=HTR, Cols=FTR")
print(ht_ft)

# As percentages of row total
ht_ft_pct = ht_ft.div(ht_ft.sum(axis=1), axis=0) * 100
print("\nRow percentages (given HT result, FT result %):")
print(ht_ft_pct.round(1))

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
import matplotlib.colors as mcolors

for ax, (data, title) in zip(axes, [(ht_ft, 'Count'), (ht_ft_pct.round(1), '% of HT result')]):
    im = ax.imshow(data.values, cmap='YlOrRd', aspect='auto')
    ax.set_xticks([0,1,2]); ax.set_xticklabels(['FT: H', 'FT: D', 'FT: A'])
    ax.set_yticks([0,1,2]); ax.set_yticklabels(['HT: H', 'HT: D', 'HT: A'])
    ax.set_title(f'HT→FT Result Matrix ({title})')
    for i in range(3):
        for j in range(3):
            ax.text(j, i, f"{data.values[i,j]:.1f}" if 'pct' in title.lower() or '%' in title else str(data.values[i,j]),
                    ha='center', va='center', fontsize=12, fontweight='bold',
                    color='white' if data.values[i,j] > data.values.max()*0.6 else 'black')
    plt.colorbar(im, ax=ax)
plt.tight_layout()
plt.savefig(f'{FIGURES}/2a_ht_ft_matrix.pdf')
plt.close()
print("Saved 2a_ht_ft_matrix.pdf")

# ── 2b. FORM ANALYSIS ─────────────────────────────────────────────────────────
print("\n\n=== 2b. FORM ANALYSIS ===")

# Assign match week: sort by date, then group into match weeks
# EPL typically plays ~10 games per week; we'll compute week number
# as the ordinal week of the season (matchday)
# Simplest: rank by date among each team's games → assign matchweek

# Build long-form team results
rows = []
for _, row in df.iterrows():
    rows.append({'date': row['Date'], 'team': row['HomeTeam'],
                 'pts': 3 if row['FTR']=='H' else (1 if row['FTR']=='D' else 0)})
    rows.append({'date': row['Date'], 'team': row['AwayTeam'],
                 'pts': 3 if row['FTR']=='A' else (1 if row['FTR']=='D' else 0)})

long = pd.DataFrame(rows).sort_values('date')

# Compute 5-game rolling average for each team
long['game_num'] = long.groupby('team').cumcount() + 1
long_sorted = long.sort_values(['team', 'date'])
long_sorted['form5'] = long_sorted.groupby('team')['pts'].transform(
    lambda x: x.rolling(5, min_periods=5).mean()
)

# Assign season matchweek using weekly date bins
unique_dates = sorted(df['Date'].unique())
# Create matchweek by grouping fixtures by calendar week
date_to_mw = {}
mw = 0
prev_week = None
for d in unique_dates:
    week_id = (pd.Timestamp(d).isocalendar().year, pd.Timestamp(d).isocalendar().week)
    if week_id != prev_week:
        mw += 1
        prev_week = week_id
    date_to_mw[d] = mw

long_sorted['mw'] = long_sorted['date'].map(date_to_mw)

# For each matchweek, compute form for each team (take their latest form up to that mw)
# We'll track form at each matchweek end
form_grid = {}
for team in teams:
    tdf = long_sorted[long_sorted['team'] == team].copy()
    # form5 is already rolling; we want the value at each matchweek they played
    for _, row in tdf.iterrows():
        mw_val = row['mw']
        f = row['form5']
        if not np.isnan(f):
            form_grid.setdefault(mw_val, {})[team] = f

# Summarize best/worst form per matchweek
print("Matchweek | Best 3 teams (form avg pts/5g) | Worst 3 teams")
all_mws = sorted(form_grid.keys())
for mw_val in all_mws:
    fd = form_grid[mw_val]
    if len(fd) < 6:
        continue
    sorted_teams = sorted(fd.items(), key=lambda x: x[1], reverse=True)
    best3 = [(t, round(v,2)) for t,v in sorted_teams[:3]]
    worst3 = [(t, round(v,2)) for t,v in sorted_teams[-3:]]
    print(f"  MW {mw_val:2d} | {best3} | {worst3}")

# Plot form lines for all teams
fig, ax = plt.subplots(figsize=(14, 7))
for team in teams:
    team_form = []
    for mw_val in all_mws:
        v = form_grid.get(mw_val, {}).get(team, np.nan)
        team_form.append(v)
    ax.plot(all_mws, team_form, alpha=0.5, linewidth=1.2, label=team)

ax.set_xlabel('Match Week')
ax.set_ylabel('Form (avg pts/last 5 games)')
ax.set_title('EPL 2024-25: Team Form (5-game rolling avg pts)')
ax.axhline(1.0, color='gray', linestyle='--', linewidth=0.8, label='Draw-equivalent')
ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=6, ncol=1)
plt.tight_layout()
plt.savefig(f'{FIGURES}/2b_form_lines.pdf', bbox_inches='tight')
plt.close()
print("Saved 2b_form_lines.pdf")

# ── 2c. CORNERS ──────────────────────────────────────────────────────────────
print("\n\n=== 2c. CORNERS ===")
corner_stats = []
for team in teams:
    home = df[df['HomeTeam'] == team]
    away = df[df['AwayTeam'] == team]
    played = len(home) + len(away)
    cf = home['HC'].sum() + away['AC'].sum()
    ca = home['AC'].sum() + away['HC'].sum()
    corner_stats.append({'Team': team, 'P': played,
                         'Corners_For_pg': cf/played, 'Corners_Against_pg': ca/played})

corner_df = pd.DataFrame(corner_stats).sort_values('Corners_For_pg', ascending=False)
print(corner_df.round(2).to_string())

# Do corners correlate with result?
df['corner_diff'] = df['HC'] - df['AC']
df['result_num'] = df['FTR'].map({'H': 1, 'D': 0, 'A': -1})
corr, p_corr = stats.pointbiserialr(df['result_num'], df['corner_diff'])
print(f"\nCorrelation (corner_diff vs result_num): r={corr:.3f}, p={p_corr:.4f}")

# Corners for vs against by team
fig, ax = plt.subplots(figsize=(12, 5))
x = np.arange(len(corner_df))
w = 0.35
ax.bar(x - w/2, corner_df['Corners_For_pg'], w, label='Corners For/game', color='steelblue', edgecolor='navy', linewidth=0.5)
ax.bar(x + w/2, corner_df['Corners_Against_pg'], w, label='Corners Against/game', color='tomato', edgecolor='darkred', linewidth=0.5)
ax.set_xticks(x)
ax.set_xticklabels(corner_df['Team'], rotation=45, ha='right', fontsize=8)
ax.set_ylabel('Corners per Game')
ax.set_title('EPL 2024-25: Corners For/Against per Game')
ax.legend()
plt.tight_layout()
plt.savefig(f'{FIGURES}/2c_corners.pdf')
plt.close()
print("Saved 2c_corners.pdf")

# Scatter: corner diff vs goal diff per game
fig, ax = plt.subplots(figsize=(7, 5))
goal_diff = df['FTHG'] - df['FTAG']
ax.scatter(df['corner_diff'], goal_diff, alpha=0.3, s=20, color='steelblue')
m, b = np.polyfit(df['corner_diff'].dropna(), goal_diff[df['corner_diff'].notna()], 1)
x_line = np.linspace(df['corner_diff'].min(), df['corner_diff'].max(), 100)
ax.plot(x_line, m*x_line + b, 'r-', linewidth=1.5, label=f'r={corr:.3f}')
ax.set_xlabel('Corner Differential (Home − Away)')
ax.set_ylabel('Goal Differential (Home − Away)')
ax.set_title('Corners vs Goals – EPL 2024-25')
ax.legend()
ax.axhline(0, color='gray', linewidth=0.5)
ax.axvline(0, color='gray', linewidth=0.5)
plt.tight_layout()
plt.savefig(f'{FIGURES}/2c_corner_goal_scatter.pdf')
plt.close()
print("Saved 2c_corner_goal_scatter.pdf")

# ── 3a. BETTING ODDS PREDICTION ───────────────────────────────────────────────
print("\n\n=== 3a. BET365 PREDICTION MODEL ===")
bet_df = df[['FTR', 'B365H', 'B365D', 'B365A']].dropna()
print(f"Games with Bet365 odds: {len(bet_df)}")

# Convert to implied probabilities
bet_df = bet_df.copy()
bet_df['imp_H'] = 1 / bet_df['B365H']
bet_df['imp_D'] = 1 / bet_df['B365D']
bet_df['imp_A'] = 1 / bet_df['B365A']
bet_df['margin'] = bet_df['imp_H'] + bet_df['imp_D'] + bet_df['imp_A']

# Renormalize
bet_df['prob_H'] = bet_df['imp_H'] / bet_df['margin']
bet_df['prob_D'] = bet_df['imp_D'] / bet_df['margin']
bet_df['prob_A'] = bet_df['imp_A'] / bet_df['margin']

print(f"Avg bookmaker margin: {(bet_df['margin']-1).mean()*100:.2f}%")

# Predict: outcome with highest normalized probability
bet_df['pred'] = bet_df[['prob_H','prob_D','prob_A']].idxmax(axis=1).str[-1]
bet_df['correct'] = bet_df['pred'] == bet_df['FTR']
accuracy_bet = bet_df['correct'].mean()

# Random baseline (equal 1/3)
accuracy_random = 1/3
# Majority-class baseline
majority = df['FTR'].value_counts().idxmax()
accuracy_majority = (df['FTR'] == majority).mean()

print(f"\nBet365 model accuracy:     {accuracy_bet*100:.1f}%")
print(f"Random baseline (1/3):     {accuracy_random*100:.1f}%")
print(f"Majority class ('{majority}'):   {accuracy_majority*100:.1f}%")

# Per-class accuracy
for outcome in ['H', 'D', 'A']:
    sub = bet_df[bet_df['FTR'] == outcome]
    acc_o = (sub['pred'] == sub['FTR']).mean()
    print(f"  Accuracy when true={outcome}: {acc_o*100:.1f}% (n={len(sub)})")

# Confusion matrix
from collections import Counter
labels_order = ['H', 'D', 'A']
print("\nConfusion matrix (rows=actual, cols=predicted):")
print(f"{'':>10} {'Pred H':>8} {'Pred D':>8} {'Pred A':>8}")
for actual in labels_order:
    row = []
    for pred in labels_order:
        row.append(((bet_df['FTR'] == actual) & (bet_df['pred'] == pred)).sum())
    print(f"  Act {actual}: {row[0]:>8} {row[1]:>8} {row[2]:>8}")

# Fig: accuracy comparison
fig, ax = plt.subplots(figsize=(6, 4))
models = ['Bet365\n(renorm)', 'Random\n(1/3 each)', f'Majority\nclass ({majority})']
accs = [accuracy_bet*100, accuracy_random*100, accuracy_majority*100]
colors = ['#4CAF50', '#9E9E9E', '#FF9800']
bars = ax.bar(models, accs, color=colors, edgecolor='black', linewidth=0.5)
for bar, v in zip(bars, accs):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{v:.1f}%', ha='center', fontsize=11)
ax.set_ylim(0, 100)
ax.set_ylabel('Prediction Accuracy (%)')
ax.set_title('EPL 2024-25: Match Prediction Accuracy')
plt.tight_layout()
plt.savefig(f'{FIGURES}/3a_prediction_accuracy.pdf')
plt.close()
print("Saved 3a_prediction_accuracy.pdf")

print("\n\n=== ANALYSIS COMPLETE ===")
print(f"Figures saved to: {FIGURES}/")

# Collect key results for summary
summary = {
    'n_matches': len(df),
    'date_range': f"{df['Date'].min().date()} – {df['Date'].max().date()}",
    'home_win_pct': ftr_counts.get('H',0)/n*100,
    'draw_pct': ftr_counts.get('D',0)/n*100,
    'away_win_pct': ftr_counts.get('A',0)/n*100,
    'avg_goals_per_game': df['total_goals'].mean(),
    'avg_home_goals': df['FTHG'].mean(),
    'avg_away_goals': df['FTAG'].mean(),
    'p_result_dist': p_val,
    'p_goals_ttest': p_goals,
    'p_yellow_ttest': p_y,
    'standings': standings,
    'team_stats': ts,
    'ref_df': ref_df,
    'ht_ft': ht_ft,
    'ht_ft_pct': ht_ft_pct,
    'corner_corr': corr,
    'p_corner_corr': p_corr,
    'accuracy_bet': accuracy_bet,
    'bet_margin': (bet_df['margin']-1).mean()*100,
}
print("\nAll results computed.")
import pickle
with open('/Users/averytishue/Claude_EPL/results.pkl', 'wb') as f:
    pickle.dump(summary, f)
print("Results pickled to results.pkl")
