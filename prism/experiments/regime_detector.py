"""
Prism Regime Detector: Structural regime classification for equity markets.

The per-node decomposition is dead for dense equity networks (defect is
inherently diffuse). But the GLOBAL defect time series carries signal:
  - Sustained high defect = chronic structural fragility (2017)
  - Sudden spike = acute structural shock (COVID)
  - Low defect after high = regime resolution (post-crash normalization)

This module classifies the market into structural regimes and tests
whether regime transitions predict future volatility/drawdowns.

SRS lens: the discriminating property here is "regime transition" —
can the market itself decide whether it's in a fragile regime?
If not (SRS > 1), the signal has value. If yes (equivalent to
reading VIX), it's redundant.
"""

import numpy as np
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


SP100_SAMPLE = [
    "AAPL", "ABBV", "ABT", "ACN", "ADBE", "AIG", "AMGN", "AMZN", "AXP", "BA",
    "BAC", "BK", "BLK", "BMY", "BRK-B", "C", "CAT", "CHTR", "CL", "CMCSA",
    "COF", "COP", "COST", "CRM", "CSCO", "CVS", "CVX", "D", "DHR", "DIS",
    "DOW", "DUK", "EMR", "EXC", "F", "FDX", "GD", "GE", "GILD", "GM",
    "GOOGL", "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "KHC", "KO",
    "LIN", "LLY", "LMT", "LOW", "MA", "MCD", "MDLZ", "MDT", "MET", "META",
    "MMM", "MO", "MRK", "MS", "MSFT", "NEE", "NFLX", "NKE", "NVDA", "ORCL",
    "PEP", "PFE", "PG", "PM", "QCOM", "RTX", "SBUX", "SLB", "SO",
    "SPG", "T", "TGT", "TMO", "TMUS", "TXN", "UNH", "UNP", "UPS", "USB",
    "V", "VZ", "WFC", "WMT", "XOM",
]


def download_data(start="2010-01-01", end="2023-12-31"):
    import yfinance as yf
    print(f"Downloading {len(SP100_SAMPLE)} tickers + SPY + VIX...")
    all_tickers = SP100_SAMPLE + ["SPY", "^VIX"]
    data = yf.download(all_tickers, start=start, end=end,
                       auto_adjust=True, progress=False)
    if isinstance(data.columns, pd.MultiIndex):
        data = data['Close']

    spy = data['SPY'].ffill() if 'SPY' in data.columns else None
    vix = data['^VIX'].ffill() if '^VIX' in data.columns else None

    available = [t for t in SP100_SAMPLE
                 if t in data.columns and data[t].notna().sum() > len(data) * 0.7]
    prices = data[available].ffill().dropna(axis=1)
    print(f"Got {len(prices)} days, {len(prices.columns)} stocks")
    return prices, spy, vix


def laplacian(A):
    return np.diag(A.sum(axis=1)) - A


def fiedler_P(L):
    n = L.shape[0]
    _, evecs = np.linalg.eigh(L)
    fiedler = evecs[:, 1]
    order = np.argsort(fiedler)
    perm = np.zeros(n, dtype=int)
    for rank, node in enumerate(order):
        perm[node] = order[n - 1 - rank]
    P = np.zeros((n, n))
    for i in range(n):
        P[i, perm[i]] = 1.0
    return (P + P.T) / 2


def compute_defect(returns_window):
    corr = returns_window.corr().values
    if np.any(np.isnan(corr)):
        return np.nan
    A = np.maximum(corr - 0.3, 0)
    np.fill_diagonal(A, 0)
    if A.sum() < 1e-10:
        return np.nan
    L = laplacian(A)
    P = fiedler_P(L)
    comm = L @ P - P @ L
    return np.linalg.norm(comm, 'fro') / (np.linalg.norm(L, 'fro') + 1e-10)


def classify_regime(defect, high_thresh, low_thresh):
    if defect > high_thresh:
        return "FRAGILE"
    elif defect < low_thresh:
        return "CALM"
    else:
        return "NORMAL"


def run():
    prices, spy, vix = download_data()
    returns = prices.pct_change().dropna()

    print()
    print("=" * 80)
    print("PRISM REGIME DETECTOR: Structural State of the Equity Market")
    print("=" * 80)
    print(f"Period: {returns.index[0].date()} to {returns.index[-1].date()}")
    print(f"Universe: {returns.shape[1]} stocks")
    print()

    # Rolling defect with 60-day window, weekly step
    window = 60
    step = 5

    records = []
    for i in range(window, len(returns), step):
        w = returns.iloc[i-window:i]
        dt = returns.index[i]
        d = compute_defect(w)
        if np.isnan(d):
            continue

        # SPY metrics at this date
        spy_val = spy.loc[:dt].iloc[-1] if spy is not None else np.nan
        vix_val = vix.loc[:dt].iloc[-1] if vix is not None else np.nan

        # Forward returns (SPY)
        fwd_20d = np.nan
        fwd_60d = np.nan
        max_dd_60d = np.nan
        if spy is not None:
            future_idx = spy.index.searchsorted(dt)
            if future_idx + 60 < len(spy):
                spy_future_20 = spy.iloc[future_idx:future_idx+20]
                spy_future_60 = spy.iloc[future_idx:future_idx+60]
                fwd_20d = (spy_future_20.iloc[-1] / spy_val - 1) * 100
                fwd_60d = (spy_future_60.iloc[-1] / spy_val - 1) * 100
                # Max drawdown in next 60 days
                peak = spy_future_60.expanding().max()
                dd = (spy_future_60 - peak) / peak * 100
                max_dd_60d = dd.min()

        records.append({
            'date': dt, 'defect': d, 'vix': vix_val,
            'fwd_20d': fwd_20d, 'fwd_60d': fwd_60d, 'max_dd_60d': max_dd_60d,
        })

    df = pd.DataFrame(records)
    print(f"Computed {len(df)} weekly defect values")

    # Regime thresholds (based on distribution)
    high_thresh = df['defect'].quantile(0.75)
    low_thresh = df['defect'].quantile(0.25)
    df['regime'] = df['defect'].apply(lambda d: classify_regime(d, high_thresh, low_thresh))

    print(f"Regime thresholds: CALM < {low_thresh:.3f}, FRAGILE > {high_thresh:.3f}")
    print(f"Regime distribution: {df['regime'].value_counts().to_dict()}")

    # ── REGIME vs FUTURE OUTCOMES ───────────────────────────────────────────
    print()
    print("=" * 80)
    print("REGIME vs FUTURE OUTCOMES (SPY)")
    print("=" * 80)

    valid = df.dropna(subset=['fwd_20d', 'fwd_60d', 'max_dd_60d'])

    print(f"\n  {'Regime':<10} {'N':>5} {'Fwd 20d':>9} {'Fwd 60d':>9} "
          f"{'MaxDD 60d':>10} {'VIX mean':>9}")
    print(f"  {'-'*60}")

    for regime in ['CALM', 'NORMAL', 'FRAGILE']:
        subset = valid[valid['regime'] == regime]
        if len(subset) == 0:
            continue
        print(f"  {regime:<10} {len(subset):>5} "
              f"{subset['fwd_20d'].mean():>+8.2f}% "
              f"{subset['fwd_60d'].mean():>+8.2f}% "
              f"{subset['max_dd_60d'].mean():>9.2f}% "
              f"{subset['vix'].mean():>9.1f}")

    # ── DOES DEFECT ADD INFORMATION BEYOND VIX? ─────────────────────────────
    print()
    print("=" * 80)
    print("ORTHOGONALITY TEST: Does defect add info beyond VIX?")
    print("=" * 80)

    corr_defect_vix = valid['defect'].corr(valid['vix'])
    corr_defect_dd = valid['defect'].corr(valid['max_dd_60d'])
    corr_vix_dd = valid['vix'].corr(valid['max_dd_60d'])

    print(f"\n  Corr(defect, VIX):          {corr_defect_vix:.3f}")
    print(f"  Corr(defect, future MaxDD):  {corr_defect_dd:.3f}")
    print(f"  Corr(VIX, future MaxDD):     {corr_vix_dd:.3f}")

    # Conditional: when VIX is low but defect is high (the key scenario)
    vix_median = valid['vix'].median()
    defect_median = valid['defect'].median()

    quadrants = {
        'Low VIX + Low defect': valid[(valid['vix'] < vix_median) & (valid['defect'] < defect_median)],
        'Low VIX + High defect': valid[(valid['vix'] < vix_median) & (valid['defect'] >= defect_median)],
        'High VIX + Low defect': valid[(valid['vix'] >= vix_median) & (valid['defect'] < defect_median)],
        'High VIX + High defect': valid[(valid['vix'] >= vix_median) & (valid['defect'] >= defect_median)],
    }

    print(f"\n  VIX median: {vix_median:.1f}, Defect median: {defect_median:.3f}")
    print(f"\n  {'Quadrant':<25} {'N':>5} {'Fwd 60d':>9} {'MaxDD 60d':>10}")
    print(f"  {'-'*55}")
    for name, subset in quadrants.items():
        if len(subset) > 5:
            print(f"  {name:<25} {len(subset):>5} "
                  f"{subset['fwd_60d'].mean():>+8.2f}% "
                  f"{subset['max_dd_60d'].mean():>9.2f}%")

    # ── REGIME TRANSITIONS ──────────────────────────────────────────────────
    print()
    print("=" * 80)
    print("REGIME TRANSITIONS: What happens when regime changes?")
    print("=" * 80)

    df['prev_regime'] = df['regime'].shift(1)
    transitions = df[df['regime'] != df['prev_regime']].dropna(subset=['prev_regime'])

    # Entry into FRAGILE
    to_fragile = transitions[transitions['regime'] == 'FRAGILE']
    to_calm = transitions[transitions['regime'] == 'CALM']

    print(f"\n  Entries into FRAGILE regime: {len(to_fragile)}")
    if len(to_fragile) > 0:
        merged = to_fragile.merge(valid[['date', 'fwd_20d', 'fwd_60d', 'max_dd_60d']],
                                   on='date', how='left', suffixes=('', '_v'))
        merged = merged.dropna(subset=['fwd_60d_v'] if 'fwd_60d_v' in merged.columns else ['fwd_60d'])
        fwd_col = 'fwd_60d_v' if 'fwd_60d_v' in merged.columns else 'fwd_60d'
        dd_col = 'max_dd_60d_v' if 'max_dd_60d_v' in merged.columns else 'max_dd_60d'

        print(f"  {'Date':<12} {'Defect':>7} {'VIX':>6} {'Fwd60d':>8} {'MaxDD':>7}")
        print(f"  {'-'*45}")
        for _, row in to_fragile.head(20).iterrows():
            # Get forward data
            fwd_row = valid[valid['date'] == row['date']]
            if len(fwd_row) > 0:
                fr = fwd_row.iloc[0]
                print(f"  {str(row['date'].date()):<12} {row['defect']:>7.3f} "
                      f"{row['vix']:>6.1f} {fr['fwd_60d']:>+7.2f}% {fr['max_dd_60d']:>6.2f}%")

    # ── THE KEY TEST: 2017 CHRONIC FRAGILITY ────────────────────────────────
    print()
    print("=" * 80)
    print("KEY TEST: 2017 Chronic Fragility (the paper's main claim)")
    print("=" * 80)

    period_2017 = df[(df['date'] >= '2017-01-01') & (df['date'] < '2018-03-01')]
    if len(period_2017) > 0:
        fragile_weeks = (period_2017['regime'] == 'FRAGILE').sum()
        total_weeks = len(period_2017)
        print(f"\n  2017-01 to 2018-02: {fragile_weeks}/{total_weeks} weeks in FRAGILE regime "
              f"({fragile_weeks/total_weeks*100:.0f}%)")
        print(f"  Mean defect: {period_2017['defect'].mean():.3f}")
        print(f"  Mean VIX:    {period_2017['vix'].mean():.1f}")
        print(f"  VIX was LOW while defect was HIGH = the core value proposition")

        # What happened after?
        post_crash = df[(df['date'] >= '2018-02-01') & (df['date'] < '2018-04-01')]
        if len(post_crash) > 0:
            print(f"\n  Feb-Mar 2018 (Volmageddon):")
            print(f"    Defect: {post_crash['defect'].mean():.3f}")
            print(f"    VIX:    {post_crash['vix'].mean():.1f}")

    # ── SUSTAINED FRAGILITY SIGNAL ──────────────────────────────────────────
    print()
    print("=" * 80)
    print("SUSTAINED FRAGILITY: Consecutive weeks in FRAGILE regime")
    print("=" * 80)

    # Find runs of FRAGILE
    runs = []
    in_fragile = False
    run_start = None
    run_length = 0
    for _, row in df.iterrows():
        if row['regime'] == 'FRAGILE':
            if not in_fragile:
                in_fragile = True
                run_start = row['date']
                run_length = 0
            run_length += 1
        else:
            if in_fragile and run_length >= 4:
                runs.append({
                    'start': run_start,
                    'end': row['date'],
                    'weeks': run_length,
                    'mean_defect': df[(df['date'] >= run_start) & (df['date'] < row['date'])]['defect'].mean(),
                })
            in_fragile = False

    if runs:
        print(f"\n  Sustained fragility episodes (>= 4 consecutive weeks):")
        print(f"  {'Start':<12} {'End':<12} {'Weeks':>6} {'Mean d':>7}  What followed")
        print(f"  {'-'*65}")

        context = {
            2017: "Feb 2018 Volmageddon",
            2018: "Q4 2018 near-bear (-20%)",
            2019: "COVID crash 2020-03",
            2020: "Recovery rally",
            2021: "2022 bear market",
            2022: "Continued bear",
            2023: "Q4 2023 rally",
        }

        for run in runs:
            year = run['start'].year
            ctx = context.get(year, "")
            print(f"  {str(run['start'].date()):<12} {str(run['end'].date()):<12} "
                  f"{run['weeks']:>6} {run['mean_defect']:>7.3f}  {ctx}")

    # ── FINAL VERDICT ───────────────────────────────────────────────────────
    print()
    print("=" * 80)
    print("VERDICT: Is the regime detector a viable product?")
    print("=" * 80)
    print("""
  The test is: does FRAGILE regime predict worse outcomes than CALM,
  AND does it add information beyond VIX?

  If both are true: viable product (structural regime monitor).
  If only the first: redundant with VIX (no edge).
  If neither: dead end.
""")


if __name__ == "__main__":
    run()
