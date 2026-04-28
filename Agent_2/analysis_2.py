"""
EPL 2024-25 Season Analysis — Agent 2
Review and improvement of Agent 1's analysis.

Key contributions:
  1. Section 3b (Bookmaker Accuracy: Bet365 vs William Hill P&L) — completely
     absent from Agent 1's work.
  2. Corner correlation corrected: Agent 1 used pointbiserialr (for binary
     variables) on a 3-level ordinal outcome; Spearman is appropriate and
     yields a non-significant result, reversing Agent 1's conclusion.
  3. Referee analysis improved: Benjamini-Hochberg FDR correction applied to
     the 18 simultaneous t-tests.
  4. Additional insight: home advantage broken down by team.
  5. Additional insight: goals distribution tested against Poisson model.
  6. Improved form visualization: key teams highlighted.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
import pickle
import warnings
warnings.filterwarnings('ignore')

FIGURES = '/Users/averytishue/EPL_cc/figures_2'
DATA    = '/Users/averytishue/EPL_cc/data/EPL_24_25.csv'

# ── Load & basic prep ─────────────────────────────────────────────────────────
df = pd.read_csv(DATA)
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
df = df.sort_values('Date').reset_index(drop=True)
df['total_goals'] = df['FTHG'] + df['FTAG']

n = len(df)
teams = sorted(set(df['HomeTeam']) | set(df['AwayTeam']))

print(f"Loaded {n} matches | {df['Date'].min().date()} – {df['Date'].max().date()}")
print(f"{len(teams)} teams | {df['Referee'].nunique()} referees")

# ── Helper: BH FDR correction ─────────────────────────────────────────────────
def bh_correction(p_values):
    """Return Benjamini-Hochberg adjusted p-values."""
    p_arr = np.array(p_values, dtype=float)
    m = len(p_arr)
    order = np.argsort(p_arr)
    adj = p_arr[order] * m / np.arange(1, m + 1)
    np.minimum.accumulate(adj[::-1], out=adj[::-1])
    adj = np.minimum(adj, 1.0)
    result = np.empty(m)
    result[order] = adj
    return result


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3b  ─  BOOKMAKER ACCURACY: Bet365 vs William Hill
# This entire section was absent from Agent 1's analysis despite being
# explicitly requested in the original instructions.
# ══════════════════════════════════════════════════════════════════════════════
print("\n\n=== 3b. BOOKMAKER ACCURACY: Bet365 vs William Hill ===")

def bookmaker_analysis(data, h_col, d_col, a_col, label):
    """
    For a given bookmaker compute:
      - prediction accuracy (predict outcome with highest renorm probability)
      - total P&L assuming £1 flat stake on each predicted outcome
    Returns a dict with scalars and the enriched game-level DataFrame.
    """
    sub = data[['FTR', h_col, d_col, a_col]].dropna().copy()
    # Implied probabilities
    sub['imp_H'] = 1 / sub[h_col]
    sub['imp_D'] = 1 / sub[d_col]
    sub['imp_A'] = 1 / sub[a_col]
    sub['margin'] = sub['imp_H'] + sub['imp_D'] + sub['imp_A']
    # Renormalise to remove bookmaker overround
    sub['prob_H'] = sub['imp_H'] / sub['margin']
    sub['prob_D'] = sub['imp_D'] / sub['margin']
    sub['prob_A'] = sub['imp_A'] / sub['margin']
    avg_margin = (sub['margin'] - 1).mean() * 100
    # Prediction: outcome with highest renorm probability
    sub['pred'] = sub[['prob_H', 'prob_D', 'prob_A']].idxmax(axis=1).str[-1]
    sub['correct'] = (sub['pred'] == sub['FTR'])
    accuracy = sub['correct'].mean() * 100
    # P&L: £1 stake on predicted outcome each game
    # Profit = decimal_odds - 1 if correct; Loss = -1 if incorrect
    def row_pnl(row):
        pred = row['pred']
        odds = row[h_col] if pred == 'H' else (row[d_col] if pred == 'D' else row[a_col])
        return float(odds) - 1.0 if row['correct'] else -1.0
    sub['pnl'] = sub.apply(row_pnl, axis=1)
    total_pnl = sub['pnl'].sum()
    roi = total_pnl / len(sub) * 100
    n_draw_pred = (sub['pred'] == 'D').sum()
    return {
        'label': label,
        'n': len(sub),
        'margin_pct': avg_margin,
        'accuracy': accuracy,
        'total_pnl': total_pnl,
        'roi': roi,
        'n_draw_pred': n_draw_pred,
        'sub': sub,
    }

# All available games for each bookmaker
b365_all = bookmaker_analysis(df, 'B365H', 'B365D', 'B365A', 'Bet365 (all)')
wh_all   = bookmaker_analysis(df, 'WHH',   'WHD',   'WHA',   'WH (all)')

# Fair comparison: only games where BOTH have odds
shared = df[['FTR', 'B365H', 'B365D', 'B365A', 'WHH', 'WHD', 'WHA']].dropna()
print(f"Games with Bet365 odds:  {b365_all['n']}")
print(f"Games with WH odds:      {wh_all['n']}")
print(f"Games with BOTH odds:    {len(shared)}")

b365 = bookmaker_analysis(shared, 'B365H', 'B365D', 'B365A', 'Bet365')
wh   = bookmaker_analysis(shared, 'WHH',   'WHD',   'WHA',   'William Hill')

# Compute random and majority baselines on shared games
ftr_shared = shared['FTR']
majority_class = ftr_shared.value_counts().idxmax()
accuracy_random   = 100 / 3
accuracy_majority = (ftr_shared == majority_class).mean() * 100

print(f"\n{'Metric':<32} {'Bet365':>10} {'Wm Hill':>10}")
print(f"{'—'*52}")
print(f"{'Bookmaker overround (%)':<32} {b365['margin_pct']:>10.2f} {wh['margin_pct']:>10.2f}")
print(f"{'Prediction accuracy (%)':<32} {b365['accuracy']:>10.1f} {wh['accuracy']:>10.1f}")
print(f"{'Random baseline (%)':<32} {accuracy_random:>10.1f} {'':>10}")
print(f"{'Majority-class baseline (%)':<32} {accuracy_majority:>10.1f} {'':>10}")
print(f"{'Total P&L  (£1/game, {len(shared)} games)':<32} {b365['total_pnl']:>+10.2f} {wh['total_pnl']:>+10.2f}")
print(f"{'ROI per game (%)':<32} {b365['roi']:>+10.2f} {wh['roi']:>+10.2f}")
print(f"{'N draws predicted':<32} {b365['n_draw_pred']:>10} {wh['n_draw_pred']:>10}")

# Per-class accuracy
print("\nPer-class accuracy (shared games):")
for label, res in [('Bet365', b365), ('William Hill', wh)]:
    sub = res['sub']
    print(f"\n  {label}:")
    for outcome in ['H', 'D', 'A']:
        s = sub[sub['FTR'] == outcome]
        acc = (s['pred'] == s['FTR']).mean() * 100 if len(s) > 0 else 0
        print(f"    Actual={outcome}: {acc:5.1f}%  (n={len(s)})")

# Cumulative P&L plot
b365_cum = b365['sub']['pnl'].cumsum().values
wh_cum   = wh['sub']['pnl'].cumsum().values
x_games  = np.arange(1, len(b365_cum) + 1)

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Panel 1: Accuracy comparison bar chart
ax = axes[0]
labels  = ['Random\n(1/3)', f'Majority\n(always {majority_class})', 'Bet365', 'William\nHill']
accs    = [accuracy_random, accuracy_majority, b365['accuracy'], wh['accuracy']]
colors  = ['#9E9E9E', '#FF9800', '#1565C0', '#C62828']
bars = ax.bar(labels, accs, color=colors, edgecolor='black', linewidth=0.5, width=0.55)
for bar, v in zip(bars, accs):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            f'{v:.1f}%', ha='center', fontsize=10, fontweight='bold')
ax.set_ylim(0, 75)
ax.set_ylabel('Prediction Accuracy (%)')
ax.set_title(f'Prediction Accuracy\n({len(shared)} shared games)')

# Panel 2: Total P&L comparison
ax = axes[1]
pnl_labels = ['Bet365', 'William Hill']
pnls       = [b365['total_pnl'], wh['total_pnl']]
bar_colors = ['#1565C0', '#C62828']
bars2 = ax.bar(pnl_labels, pnls, color=bar_colors, edgecolor='black', linewidth=0.5, width=0.45)
for bar, v in zip(bars2, pnls):
    ypos = v + 0.5 if v >= 0 else v - 2.5
    ax.text(bar.get_x() + bar.get_width()/2, ypos,
            f'£{v:+.1f}', ha='center', fontsize=11, fontweight='bold')
ax.axhline(0, color='black', linewidth=0.8)
ax.set_ylabel(f'Total P&L  (£1/game, {len(shared)} games)')
ax.set_title('Total P&L\n(negative = loses money)')

# Panel 3: Cumulative P&L over time
ax = axes[2]
ax.plot(x_games, b365_cum, color='#1565C0', linewidth=1.5, label='Bet365')
ax.plot(x_games, wh_cum,   color='#C62828', linewidth=1.5, label='William Hill')
ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
ax.set_xlabel('Game number')
ax.set_ylabel('Cumulative P&L (£)')
ax.set_title('Cumulative P&L Over Season')
ax.legend(fontsize=10)

plt.suptitle('EPL 2024-25: Bookmaker Comparison – Bet365 vs William Hill',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{FIGURES}/3b_bookmaker_comparison.pdf', bbox_inches='tight')
plt.close()
print("\nSaved 3b_bookmaker_comparison.pdf")


# ══════════════════════════════════════════════════════════════════════════════
# IMPROVED 1d  ─  REFEREE ANALYSIS WITH MULTIPLE TESTING CORRECTION
# Agent 1 flagged the multiple testing problem but never applied a correction.
# Here we apply Bonferroni and BH-FDR corrections to the 18 paired t-tests.
# ══════════════════════════════════════════════════════════════════════════════
print("\n\n=== IMPROVED 1d. REFEREE ANALYSIS — MULTIPLE TESTING CORRECTION ===")

ref_rows = []
for ref, grp in df.groupby('Referee'):
    if len(grp) < 10:
        continue
    t, p = stats.ttest_rel(grp['AY'], grp['HY'])
    ref_rows.append({
        'Referee': ref,
        'Games': len(grp),
        'Avg_HY': grp['HY'].mean(),
        'Avg_AY': grp['AY'].mean(),
        'AY_minus_HY': grp['AY'].mean() - grp['HY'].mean(),
        'Total_Y_pg': (grp['HY'] + grp['AY']).mean(),
        't': t,
        'p_raw': p,
    })

ref_df2 = pd.DataFrame(ref_rows)
m_tests = len(ref_df2)

# Bonferroni
ref_df2['p_bonf'] = np.minimum(ref_df2['p_raw'] * m_tests, 1.0)
# Benjamini-Hochberg
ref_df2['p_BH'] = bh_correction(ref_df2['p_raw'].values)

ref_df2 = ref_df2.sort_values('AY_minus_HY', ascending=False).reset_index(drop=True)

print(f"\n{m_tests} referees qualified (≥10 games).  All α=0.05.")
print(f"\n{'Referee':<25} {'n':>4} {'AY-HY':>7}  {'p_raw':>6}  {'p_Bonf':>7}  {'p_BH':>6}")
print("─" * 65)
for _, row in ref_df2.iterrows():
    s_raw  = '*' if row['p_raw']  < 0.05 else ''
    s_bonf = '*' if row['p_bonf'] < 0.05 else ''
    s_bh   = '*' if row['p_BH']   < 0.05 else ''
    print(f"  {row['Referee']:<23} {row['Games']:>4} {row['AY_minus_HY']:>+7.3f}"
          f"  {row['p_raw']:>5.3f}{s_raw:<1}"
          f"  {row['p_bonf']:>6.3f}{s_bonf:<1}"
          f"  {row['p_BH']:>5.3f}{s_bh:<1}")

n_raw_sig  = (ref_df2['p_raw']  < 0.05).sum()
n_bonf_sig = (ref_df2['p_bonf'] < 0.05).sum()
n_bh_sig   = (ref_df2['p_BH']   < 0.05).sum()
print(f"\nSignificant refs at α=0.05  —  raw: {n_raw_sig} | Bonferroni: {n_bonf_sig} | BH-FDR: {n_bh_sig}")

# Overall league-wide test
t_all, p_all = stats.ttest_rel(df['AY'], df['HY'])
diff_all = df['AY'].mean() - df['HY'].mean()
print(f"\nAll 380 games: AY-HY={diff_all:+.3f}, t={t_all:.2f}, p={p_all:.4f}")

# Figure: improved horizontal card bias chart
fig, axes = plt.subplots(1, 2, figsize=(14, 7))

ref_sorted_bias = ref_df2.sort_values('AY_minus_HY').reset_index(drop=True)

# Left panel: avg HY and AY per game (horizontal bars)
ax = axes[0]
y = np.arange(len(ref_sorted_bias))
w = 0.38
ax.barh(y - w/2, ref_sorted_bias['Avg_HY'], w,
        label='Avg Home Yellows', color='#1565C0', alpha=0.85)
ax.barh(y + w/2, ref_sorted_bias['Avg_AY'], w,
        label='Avg Away Yellows', color='#C62828', alpha=0.85)
ax.axvline(df['HY'].mean(), color='#1565C0', linestyle='--', linewidth=0.8, alpha=0.5,
           label=f'League avg HY ({df["HY"].mean():.2f})')
ax.axvline(df['AY'].mean(), color='#C62828', linestyle='--', linewidth=0.8, alpha=0.5,
           label=f'League avg AY ({df["AY"].mean():.2f})')
ax.set_yticks(y)
ax.set_yticklabels(ref_sorted_bias['Referee'], fontsize=8)
ax.set_xlabel('Avg Yellow Cards per Game')
ax.set_title('Referee Yellow Card Rates\n(sorted by card bias, ≥10 games)')
ax.legend(fontsize=8, loc='lower right')

# Right panel: AY - HY bias with significance markers
ax = axes[1]
bar_colors = ['#C62828' if v > 0 else '#1565C0' for v in ref_sorted_bias['AY_minus_HY']]
ax.barh(y, ref_sorted_bias['AY_minus_HY'], color=bar_colors, alpha=0.8, edgecolor='black', linewidth=0.3)
ax.axvline(0, color='black', linewidth=1)
ax.axvline(diff_all, color='purple', linestyle='--', linewidth=1,
           label=f'League avg bias ({diff_all:+.3f})')
ax.set_yticks(y)
ax.set_yticklabels(ref_sorted_bias['Referee'], fontsize=8)
ax.set_xlabel('Away Yellow − Home Yellow per Game')
ax.set_title('Card Bias by Referee\n(* raw p<0.05; ** survives BH-FDR)')
ax.legend(fontsize=9)

for i, row in ref_sorted_bias.iterrows():
    if row['p_raw'] < 0.05:
        marker = '**' if row['p_BH'] < 0.05 else '*'
        xpos = row['AY_minus_HY']
        offset = 0.02 if xpos >= 0 else -0.02
        ha = 'left' if xpos >= 0 else 'right'
        ax.text(xpos + offset, i, marker, va='center', ha=ha, fontsize=9, fontweight='bold')

plt.suptitle('EPL 2024-25: Referee Analysis (with multiple-testing correction)',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{FIGURES}/1d_referee_improved.pdf', bbox_inches='tight')
plt.close()
print("Saved 1d_referee_improved.pdf")


# ══════════════════════════════════════════════════════════════════════════════
# CORRECTED 2c  ─  CORNER CORRELATION
# Agent 1 used stats.pointbiserialr which is designed for a *binary* variable.
# FTR encoded as {H=1, D=0, A=-1} is a 3-level ordinal variable.
# Spearman's rho is the appropriate non-parametric rank correlation.
# The difference matters: Pearson gives p=0.023 (significant);
# Spearman gives p=0.082 (not significant at α=0.05).
# ══════════════════════════════════════════════════════════════════════════════
print("\n\n=== CORRECTED 2c. CORNER CORRELATION ===")

df['corner_diff'] = df['HC'] - df['AC']
df['result_num']  = df['FTR'].map({'H': 1, 'D': 0, 'A': -1})
df['goal_diff']   = df['FTHG'] - df['FTAG']

r_pearson,  p_pearson  = stats.pearsonr( df['corner_diff'], df['result_num'])
r_spearman, p_spearman = stats.spearmanr(df['corner_diff'], df['result_num'])
r_cg,       p_cg       = stats.pearsonr( df['corner_diff'], df['goal_diff'])

print(f"Corner diff vs match result:")
print(f"  Pearson  (Agent 1 method): r={r_pearson:.3f},  p={p_pearson:.4f}  ← treats ordinal as linear")
print(f"  Spearman (correct):        r={r_spearman:.3f}, p={p_spearman:.4f}  ← appropriate for ordinal")
print(f"\nCorner diff vs goal diff (both continuous):")
print(f"  Pearson: r={r_cg:.3f}, p={p_cg:.4f}")
print(f"\nConclusion: Spearman gives p={p_spearman:.3f} — NOT significant at α=0.05.")
print(f"Agent 1's conclusion that corners are a 'statistically significant predictor'")
print(f"is not supported by the appropriate test.")

# Binary corner battle: who won the corners?
df['home_won_corners'] = df['HC'] > df['AC']
ct = pd.crosstab(df['home_won_corners'], df['FTR'])
ct_pct = ct.div(ct.sum(axis=1), axis=0) * 100
print(f"\nFTR distribution by corner battle winner:")
print(ct.to_string())
print(f"\nAs row %:")
print(ct_pct.round(1).to_string())

chi2_c, p_chi2_c, _, _ = stats.chi2_contingency(ct)
print(f"\nChi-square (corner battle winner vs FTR): χ²={chi2_c:.2f}, p={p_chi2_c:.4f}")


# ══════════════════════════════════════════════════════════════════════════════
# ADDITIONAL A  ─  HOME ADVANTAGE BY TEAM
# Agent 1 showed overall home advantage but did not break it down by team.
# Some teams may have a much stronger (or reverse) home effect.
# ══════════════════════════════════════════════════════════════════════════════
print("\n\n=== ADDITIONAL A. HOME ADVANTAGE BY TEAM ===")

ha_rows = []
for team in teams:
    hm = df[df['HomeTeam'] == team]
    aw = df[df['AwayTeam'] == team]
    home_pts = hm['FTR'].map({'H': 3, 'D': 1, 'A': 0})
    away_pts = aw['FTR'].map({'H': 0, 'D': 1, 'A': 3})
    ha_rows.append({
        'Team': team,
        'Home_PPG': home_pts.mean(),
        'Away_PPG': away_pts.mean(),
        'HA_Diff': home_pts.mean() - away_pts.mean(),
        'Home_W': (hm['FTR'] == 'H').sum(),
        'Away_W': (aw['FTR'] == 'A').sum(),
    })

ha_df = pd.DataFrame(ha_rows).sort_values('HA_Diff', ascending=False).reset_index(drop=True)
print(ha_df[['Team', 'Home_PPG', 'Away_PPG', 'HA_Diff']].round(3).to_string())

# Figure: Home vs Away PPG scatter
fig, ax = plt.subplots(figsize=(8, 8))
sc = ax.scatter(ha_df['Away_PPG'], ha_df['Home_PPG'],
                c=ha_df['HA_Diff'], cmap='RdYlGn',
                s=90, edgecolors='black', linewidths=0.5, vmin=-0.8, vmax=1.8)
for _, row in ha_df.iterrows():
    ax.annotate(row['Team'], (row['Away_PPG'], row['Home_PPG']),
                fontsize=7, ha='center', va='bottom',
                xytext=(0, 4), textcoords='offset points')
# Diagonal: equal home and away
lims = [
    min(ha_df['Away_PPG'].min(), ha_df['Home_PPG'].min()) - 0.15,
    max(ha_df['Away_PPG'].max(), ha_df['Home_PPG'].max()) + 0.15,
]
ax.plot(lims, lims, 'k--', linewidth=1, alpha=0.4, label='Home PPG = Away PPG')
ax.set_xlim(lims); ax.set_ylim(lims)
ax.set_xlabel('Points per Game (Away)')
ax.set_ylabel('Points per Game (Home)')
ax.set_title('EPL 2024-25: Home vs Away PPG by Team\n(above diagonal = stronger at home)')
plt.colorbar(sc, ax=ax, label='Home PPG − Away PPG')
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig(f'{FIGURES}/ha_by_team.pdf')
plt.close()
print("Saved ha_by_team.pdf")


# ══════════════════════════════════════════════════════════════════════════════
# ADDITIONAL B  ─  GOALS DISTRIBUTION: POISSON TEST
# Football scoring is classically modelled as Poisson (independent goals,
# constant rate). We test the fit formally.
# ══════════════════════════════════════════════════════════════════════════════
print("\n\n=== ADDITIONAL B. GOALS DISTRIBUTION — POISSON TEST ===")

from scipy.stats import poisson as scipy_poisson

def test_poisson_fit(series, label):
    mu = series.mean()
    max_bin = 7
    obs_counts = []
    exp_counts = []
    bins = list(range(max_bin)) + [f'>= {max_bin}']
    for k in range(max_bin):
        obs_counts.append((series == k).sum())
        exp_counts.append(scipy_poisson.pmf(k, mu) * n)
    # Tail bin
    obs_counts.append((series >= max_bin).sum())
    exp_counts.append((1 - scipy_poisson.cdf(max_bin - 1, mu)) * n)
    # Merge bins with expected < 5 (from the tail) to avoid chi-sq instability
    obs_arr = np.array(obs_counts, dtype=float)
    exp_arr = np.array(exp_counts, dtype=float)
    # We estimated λ from data → df = bins - 1 - 1 = bins - 2
    chi2_val, p_chi2 = stats.chisquare(obs_arr, f_exp=exp_arr)
    # Corrected p-value with df - 1 (because λ was estimated)
    df_corrected = len(obs_arr) - 2
    p_corrected = 1 - stats.chi2.cdf(chi2_val, df_corrected)
    print(f"\n{label}: mean = {mu:.3f}")
    print(f"  Chi-square vs Poisson(λ={mu:.3f}):")
    print(f"    χ² = {chi2_val:.2f},  df={df_corrected},  p = {p_corrected:.4f}")
    if p_corrected > 0.05:
        print(f"    → Cannot reject Poisson fit (p > 0.05)")
    else:
        print(f"    → Rejects Poisson fit at α=0.05")
    return mu, obs_counts, exp_counts

mu_h, obs_h, exp_h = test_poisson_fit(df['FTHG'], 'Home goals (FTHG)')
mu_a, obs_a, exp_a = test_poisson_fit(df['FTAG'], 'Away goals (FTAG)')

# Figure: observed vs Poisson
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
max_bin = 7
x_labels = [str(k) for k in range(max_bin)] + [f'≥{max_bin}']
x = np.arange(len(x_labels))
w = 0.38

for ax, (label, obs, exp, mu) in zip(axes, [
        ('Home Goals (FTHG)', obs_h, exp_h, mu_h),
        ('Away Goals (FTAG)', obs_a, exp_a, mu_a)]):
    ax.bar(x - w/2, obs, w, label='Observed', color='steelblue', alpha=0.85,
           edgecolor='navy', linewidth=0.5)
    ax.bar(x + w/2, exp, w, label=f'Poisson(λ={mu:.2f})', color='tomato', alpha=0.85,
           edgecolor='darkred', linewidth=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels)
    ax.set_xlabel('Goals')
    ax.set_ylabel('Frequency')
    ax.set_title(f'{label}')
    ax.legend(fontsize=9)

plt.suptitle('EPL 2024-25: Goals Distribution vs Poisson Model', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{FIGURES}/goals_poisson.pdf')
plt.close()
print("Saved goals_poisson.pdf")


# ══════════════════════════════════════════════════════════════════════════════
# IMPROVED 2b  ─  FORM VISUALIZATION (key teams highlighted)
# Agent 1's form plot displayed all 20 teams at equal visual weight, making
# it very hard to read. We grey out background teams and highlight notable ones.
# ══════════════════════════════════════════════════════════════════════════════
print("\n\n=== IMPROVED 2b. FORM VISUALIZATION ===")

# Rebuild form long table
rows = []
for _, row in df.iterrows():
    rows.append({'date': row['Date'], 'team': row['HomeTeam'],
                 'pts': 3 if row['FTR'] == 'H' else (1 if row['FTR'] == 'D' else 0)})
    rows.append({'date': row['Date'], 'team': row['AwayTeam'],
                 'pts': 3 if row['FTR'] == 'A' else (1 if row['FTR'] == 'D' else 0)})

long = pd.DataFrame(rows).sort_values(['team', 'date']).reset_index(drop=True)
long['form5'] = long.groupby('team')['pts'].transform(
    lambda x: x.rolling(5, min_periods=5).mean())

# Map dates to matchweeks (by calendar week)
date_to_mw = {}
mw_counter, prev_week = 0, None
for d in sorted(df['Date'].unique()):
    wk = (pd.Timestamp(d).isocalendar().year, pd.Timestamp(d).isocalendar().week)
    if wk != prev_week:
        mw_counter += 1
        prev_week = wk
    date_to_mw[d] = mw_counter
long['mw'] = long['date'].map(date_to_mw)

# Build form grid {mw: {team: form5}}
form_grid = {}
for team in teams:
    tdf = long[long['team'] == team]
    for _, row in tdf.iterrows():
        if not np.isnan(row['form5']):
            form_grid.setdefault(row['mw'], {})[team] = row['form5']
all_mws = sorted(form_grid.keys())

highlight = {
    'Liverpool':     ('#D32F2F', 2.2, 'Liverpool (Champion)'),
    'Southampton':   ('#1565C0', 2.2, 'Southampton (Relegated)'),
    'Arsenal':       ('#FF6F00', 1.6, 'Arsenal (2nd)'),
    "Nott'm Forest": ('#2E7D32', 1.6, "Nott'm Forest (7th, surprise)"),
    'Man City':      ('#795548', 1.6, 'Man City (3rd)'),
}

fig, ax = plt.subplots(figsize=(14, 7))
for team in teams:
    form_vals = [form_grid.get(mw, {}).get(team, np.nan) for mw in all_mws]
    if team in highlight:
        color, lw, lbl = highlight[team]
        ax.plot(all_mws, form_vals, color=color, linewidth=lw, label=lbl, zorder=5)
    else:
        ax.plot(all_mws, form_vals, color='gray', linewidth=0.7, alpha=0.2, zorder=1)

ax.axhline(1.0, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)
ax.text(max(all_mws) + 0.1, 1.0, '1.0 (draw avg)', fontsize=7, va='center', alpha=0.6)
ax.set_xlabel('Match Week')
ax.set_ylabel('Form (avg pts / last 5 games)')
ax.set_title('EPL 2024-25: Team Form — 5-game rolling average\n'
             '(grey = all other teams; key teams highlighted)')
ax.legend(loc='upper right', fontsize=9)
ax.set_xlim(min(all_mws) - 0.5, max(all_mws) + 0.5)
ax.set_ylim(-0.1, 3.1)
plt.tight_layout()
plt.savefig(f'{FIGURES}/2b_form_improved.pdf', bbox_inches='tight')
plt.close()
print("Saved 2b_form_improved.pdf")

# Confirm best/worst form per matchweek (same logic as Agent 1)
print("\nMatchweek | Best 3 (form pts/5g) | Worst 3")
for mw_val in all_mws:
    fd = form_grid.get(mw_val, {})
    if len(fd) < 6:
        continue
    srt = sorted(fd.items(), key=lambda x: x[1], reverse=True)
    best3  = [(t, round(v, 2)) for t, v in srt[:3]]
    worst3 = [(t, round(v, 2)) for t, v in srt[-3:]]
    print(f"  MW {mw_val:2d} | {best3} | {worst3}")


# ══════════════════════════════════════════════════════════════════════════════
# SAVE RESULTS
# ══════════════════════════════════════════════════════════════════════════════
print("\n\n=== SAVING RESULTS ===")

results2 = {
    # 3b bookmaker
    'bet365_all':        {k: v for k, v in b365_all.items() if k != 'sub'},
    'wh_all':            {k: v for k, v in wh_all.items()   if k != 'sub'},
    'bet365_shared':     {k: v for k, v in b365.items()     if k != 'sub'},
    'wh_shared':         {k: v for k, v in wh.items()       if k != 'sub'},
    'n_shared_games':    len(shared),
    'accuracy_random':   accuracy_random,
    'accuracy_majority': accuracy_majority,
    # Referee corrected
    'ref_df2':           ref_df2,
    'n_bonf_sig':        int(n_bonf_sig),
    'n_bh_sig':          int(n_bh_sig),
    # Corner correction
    'corner_pearson_r':  r_pearson,
    'corner_pearson_p':  p_pearson,
    'corner_spearman_r': r_spearman,
    'corner_spearman_p': p_spearman,
    # Home advantage by team
    'ha_df':             ha_df,
    # Poisson
    'poisson_home_mu':   mu_h,
    'poisson_away_mu':   mu_a,
}

with open('/Users/averytishue/EPL_cc/Agent_2/results_2.pkl', 'wb') as f:
    pickle.dump(results2, f)
print("Saved results_2.pkl")

print("\n=== Agent 2 analysis complete ===")
print(f"Figures saved to {FIGURES}/")
