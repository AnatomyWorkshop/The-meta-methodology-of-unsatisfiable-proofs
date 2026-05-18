"""
Spectral Pairing Stability: Does the Fiedler ordering reshuffle predict regime change?

The hypothesis: it's not the DEFECT VALUE that matters, but whether the
spectral pairing ITSELF is stable or volatile across time.

The Fiedler vector ranks nodes by spectral embedding. The duality operator P
pairs node ranked k with node ranked n+1-k. If this pairing is stable
(same nodes stay paired quarter after quarter), the network's deep structure
is unchanged. If the pairing suddenly reshuffles, something structural shifted.

This is genuinely non-local: you can't detect pairing instability from any
single correlation matrix. You need the temporal derivative of the spectral
structure. No existing metric measures this.

Metric: Pairing Turnover = fraction of node pairs that changed between
consecutive windows.

Test: does high pairing turnover predict future volatility/drawdowns
better than defect or VIX?
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
    return prices, spy, vix, list(prices.columns)


def laplacian(A):
    return np.diag(A.sum(axis=1)) - A


def fiedler_pairing(returns_window):
    """Return the Fiedler-based pairing as a dict: node_idx -> partner_idx."""
    corr = returns_window.corr().values
    if np.any(np.isnan(corr)):
        return None
    n = corr.shape[0]
    A = np.maximum(corr - 0.3, 0)
    np.fill_diagonal(A, 0)
    if A.sum() < 1e-10:
        return None
    L = laplacian(A)
    _, evecs = np.linalg.eigh(L)
    fiedler = evecs[:, 1]
    order = np.argsort(fiedler)
    pairing = {}
    for rank, node in enumerate(order):
        partner = order[n - 1 - rank]
        pairing[node] = partner
    return pairing


def pairing_turnover(pairing_prev, pairing_curr):
    """Fraction of nodes whose partner changed."""
    if pairing_prev is None or pairing_curr is None:
        return np.nan
    n = len(pairing_prev)
    changed = sum(1 for node in pairing_prev
                  if node in pairing_curr and pairing_prev[node] != pairing_curr[node])
    return changed / n


def fiedler_rank_correlation(returns_prev, returns_curr):
    """Spearman correlation between Fiedler rankings in two windows.
    Measures how much the spectral ordering itself changed."""
    corr_prev = returns_prev.corr().values
    corr_curr = returns_curr.corr().values
    if np.any(np.isnan(corr_prev)) or np.any(np.isnan(corr_curr)):
        return np.nan

    n = corr_prev.shape[0]

    def get_fiedler_ranks(corr):
        A = np.maximum(corr - 0.3, 0)
        np.fill_diagonal(A, 0)
        if A.sum() < 1e-10:
            return None
        L = laplacian(A)
        _, evecs = np.linalg.eigh(L)
        fiedler = evecs[:, 1]
        return np.argsort(np.argsort(fiedler))  # ranks

    ranks_prev = get_fiedler_ranks(corr_prev)
    ranks_curr = get_fiedler_ranks(corr_curr)

    if ranks_prev is None or ranks_curr is None:
        return np.nan

    # Spearman rank correlation
    from scipy.stats import spearmanr
    rho, _ = spearmanr(ranks_prev, ranks_curr)
    return rho


def compute_defect(returns_window):
    corr = returns_window.corr().values
    if np.any(np.isnan(corr)):
        return np.nan
    A = np.maximum(corr - 0.3, 0)
    np.fill_diagonal(A, 0)
    if A.sum() < 1e-10:
        return np.nan
    L = laplacian(A)
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
    P = (P + P.T) / 2
    comm = L @ P - P @ L
    return np.linalg.norm(comm, 'fro') / (np.linalg.norm(L, 'fro') + 1e-10)


def run():
    prices, spy, vix, tickers = download_data()
    returns = prices.pct_change().dropna()

    print()
    print("=" * 80)
    print("SPECTRAL PAIRING STABILITY: Temporal Derivative of Network Structure")
    print("=" * 80)
    print(f"Period: {returns.index[0].date()} to {returns.index[-1].date()}")
    print(f"Universe: {len(tickers)} stocks")
    print()

    window = 60
    step = 5  # weekly

    records = []
    prev_pairing = None
    prev_window_returns = None

    for i in range(window, len(returns), step):
        w = returns.iloc[i-window:i]
        dt = returns.index[i]

        curr_pairing = fiedler_pairing(w)
        defect = compute_defect(w)

        turnover = pairing_turnover(prev_pairing, curr_pairing)

        # Rank correlation with previous window
        rank_corr = np.nan
        if prev_window_returns is not None:
            rank_corr = fiedler_rank_correlation(prev_window_returns, w)

        # VIX and SPY forward
        vix_val = np.nan
        fwd_20d = np.nan
        fwd_60d = np.nan
        max_dd_60d = np.nan
        realized_vol_60d = np.nan

        if vix is not None:
            idx = vix.index.searchsorted(dt)
            if 0 < idx < len(vix):
                vix_val = vix.iloc[idx]

        if spy is not None:
            spy_idx = spy.index.searchsorted(dt)
            spy_val = spy.iloc[spy_idx] if spy_idx < len(spy) else np.nan
            if spy_idx + 60 < len(spy):
                spy_future_20 = spy.iloc[spy_idx:spy_idx+20]
                spy_future_60 = spy.iloc[spy_idx:spy_idx+60]
                fwd_20d = (spy_future_20.iloc[-1] / spy_val - 1) * 100
                fwd_60d = (spy_future_60.iloc[-1] / spy_val - 1) * 100
                peak = spy_future_60.expanding().max()
                dd = (spy_future_60 - peak) / peak * 100
                max_dd_60d = dd.min()
                # Realized vol
                spy_rets = spy_future_60.pct_change().dropna()
                realized_vol_60d = spy_rets.std() * np.sqrt(252) * 100

        records.append({
            'date': dt, 'defect': defect, 'turnover': turnover,
            'rank_corr': rank_corr, 'vix': vix_val,
            'fwd_20d': fwd_20d, 'fwd_60d': fwd_60d,
            'max_dd_60d': max_dd_60d, 'realized_vol_60d': realized_vol_60d,
        })

        prev_pairing = curr_pairing
        prev_window_returns = w

    df = pd.DataFrame(records)
    valid = df.dropna(subset=['turnover', 'rank_corr', 'fwd_60d', 'realized_vol_60d'])
    print(f"Computed {len(df)} weekly snapshots, {len(valid)} with full data\n")

    # ── BASIC STATISTICS ────────────────────────────────────────────────────
    print("=" * 80)
    print("PAIRING STABILITY STATISTICS")
    print("=" * 80)
    print(f"\n  Turnover (fraction of pairs that changed week-to-week):")
    print(f"    Mean:   {valid['turnover'].mean():.3f}")
    print(f"    Median: {valid['turnover'].median():.3f}")
    print(f"    Std:    {valid['turnover'].std():.3f}")
    print(f"    Range:  {valid['turnover'].min():.3f} - {valid['turnover'].max():.3f}")

    print(f"\n  Rank correlation (Fiedler ordering stability):")
    print(f"    Mean:   {valid['rank_corr'].mean():.3f}")
    print(f"    Median: {valid['rank_corr'].median():.3f}")
    print(f"    Std:    {valid['rank_corr'].std():.3f}")
    print(f"    Range:  {valid['rank_corr'].min():.3f} - {valid['rank_corr'].max():.3f}")

    # ── CORRELATION MATRIX ──────────────────────────────────────────────────
    print()
    print("=" * 80)
    print("CORRELATION MATRIX: What predicts what?")
    print("=" * 80)

    metrics = ['defect', 'turnover', 'rank_corr', 'vix',
               'fwd_20d', 'fwd_60d', 'max_dd_60d', 'realized_vol_60d']
    print(f"\n  {'':>12}", end="")
    for m in metrics:
        print(f" {m[:8]:>9}", end="")
    print()
    print(f"  {'-'*90}")
    for m1 in metrics:
        print(f"  {m1[:12]:<12}", end="")
        for m2 in metrics:
            c = valid[m1].corr(valid[m2])
            print(f" {c:>9.3f}", end="")
        print()

    # ── THE KEY TEST ────────────────────────────────────────────────────────
    print()
    print("=" * 80)
    print("KEY TEST: Does pairing instability predict future outcomes?")
    print("=" * 80)

    # Quintile analysis on turnover
    valid_sorted = valid.copy()
    valid_sorted['turnover_q'] = pd.qcut(valid_sorted['turnover'], 5,
                                          labels=['Q1(stable)', 'Q2', 'Q3', 'Q4', 'Q5(unstable)'],
                                          duplicates='drop')

    print(f"\n  By TURNOVER quintile:")
    print(f"  {'Quintile':<14} {'N':>4} {'Fwd20d':>8} {'Fwd60d':>8} {'MaxDD':>7} {'RealVol':>8} {'VIX':>6} {'Defect':>7}")
    print(f"  {'-'*70}")
    for q, group in valid_sorted.groupby('turnover_q'):
        print(f"  {q:<14} {len(group):>4} {group['fwd_20d'].mean():>+7.2f}% "
              f"{group['fwd_60d'].mean():>+7.2f}% {group['max_dd_60d'].mean():>6.2f}% "
              f"{group['realized_vol_60d'].mean():>7.1f}% {group['vix'].mean():>5.1f} "
              f"{group['defect'].mean():>7.3f}")

    # Quintile analysis on rank_corr (inverted: low corr = unstable)
    valid_sorted['stability_q'] = pd.qcut(valid_sorted['rank_corr'], 5,
                                           labels=['Q1(unstable)', 'Q2', 'Q3', 'Q4', 'Q5(stable)'],
                                           duplicates='drop')

    print(f"\n  By RANK CORRELATION quintile (low = spectral reshuffling):")
    print(f"  {'Quintile':<14} {'N':>4} {'Fwd20d':>8} {'Fwd60d':>8} {'MaxDD':>7} {'RealVol':>8} {'VIX':>6} {'Defect':>7}")
    print(f"  {'-'*70}")
    for q, group in valid_sorted.groupby('stability_q'):
        print(f"  {q:<14} {len(group):>4} {group['fwd_20d'].mean():>+7.2f}% "
              f"{group['fwd_60d'].mean():>+7.2f}% {group['max_dd_60d'].mean():>6.2f}% "
              f"{group['realized_vol_60d'].mean():>7.1f}% {group['vix'].mean():>5.1f} "
              f"{group['defect'].mean():>7.3f}")

    # ── ORTHOGONALITY: Does stability add info beyond VIX and defect? ───────
    print()
    print("=" * 80)
    print("ORTHOGONALITY: Controlling for VIX")
    print("=" * 80)

    # Split by VIX median, then check if turnover still predicts
    vix_med = valid['vix'].median()
    for vix_regime, subset in [("Low VIX (<{:.0f})".format(vix_med),
                                 valid[valid['vix'] < vix_med]),
                                ("High VIX (>={:.0f})".format(vix_med),
                                 valid[valid['vix'] >= vix_med])]:
        if len(subset) < 50:
            continue
        turnover_med = subset['turnover'].median()
        stable = subset[subset['turnover'] < turnover_med]
        unstable = subset[subset['turnover'] >= turnover_med]
        print(f"\n  {vix_regime}:")
        print(f"    Stable pairing:   fwd60d={stable['fwd_60d'].mean():>+.2f}%, "
              f"MaxDD={stable['max_dd_60d'].mean():.2f}%, "
              f"RealVol={stable['realized_vol_60d'].mean():.1f}% (N={len(stable)})")
        print(f"    Unstable pairing: fwd60d={unstable['fwd_60d'].mean():>+.2f}%, "
              f"MaxDD={unstable['max_dd_60d'].mean():.2f}%, "
              f"RealVol={unstable['realized_vol_60d'].mean():.1f}% (N={len(unstable)})")

    # ── EXTREME EVENTS ──────────────────────────────────────────────────────
    print()
    print("=" * 80)
    print("EXTREME INSTABILITY EVENTS: When pairing reshuffles most")
    print("=" * 80)

    extreme = valid.nlargest(20, 'turnover')
    print(f"\n  Top 20 highest-turnover weeks:")
    print(f"  {'Date':<12} {'Turnover':>9} {'RankCorr':>9} {'Defect':>7} {'VIX':>6} {'Fwd60d':>8} {'MaxDD':>7}")
    print(f"  {'-'*65}")
    for _, row in extreme.iterrows():
        print(f"  {str(row['date'].date()):<12} {row['turnover']:>9.3f} "
              f"{row['rank_corr']:>9.3f} {row['defect']:>7.3f} "
              f"{row['vix']:>6.1f} {row['fwd_60d']:>+7.2f}% {row['max_dd_60d']:>6.2f}%")

    # ── VERDICT ─────────────────────────────────────────────────────────────
    print()
    print("=" * 80)
    print("VERDICT")
    print("=" * 80)

    # Key correlations
    c_turnover_vol = valid['turnover'].corr(valid['realized_vol_60d'])
    c_turnover_dd = valid['turnover'].corr(valid['max_dd_60d'])
    c_defect_vol = valid['defect'].corr(valid['realized_vol_60d'])
    c_vix_vol = valid['vix'].corr(valid['realized_vol_60d'])
    c_turnover_vix = valid['turnover'].corr(valid['vix'])

    print(f"""
  Predictive correlations with future 60d realized volatility:
    Turnover:  {c_turnover_vol:.3f}
    Defect:    {c_defect_vol:.3f}
    VIX:       {c_vix_vol:.3f}

  Correlation between turnover and VIX: {c_turnover_vix:.3f}
  (If close to 0: turnover is orthogonal to VIX = genuinely new info)
  (If close to +/-1: redundant with VIX = no edge)

  Predictive correlation with future 60d max drawdown:
    Turnover:  {c_turnover_dd:.3f}
    Defect:    {valid['defect'].corr(valid['max_dd_60d']):.3f}
    VIX:       {valid['vix'].corr(valid['max_dd_60d']):.3f}

  PASS criteria:
    1. Turnover predicts vol/drawdown (|corr| > 0.1)
    2. Turnover is NOT redundant with VIX (|corr with VIX| < 0.3)
    3. Quintile spread is monotonic and economically meaningful
""")


if __name__ == "__main__":
    run()
