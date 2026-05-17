"""
Prism Historical Backtest: 2011-2020

Core question: does duality defect lead stress events, or just coincide?

Five events:
  1. 2011-08-05: S&P US credit downgrade
  2. 2013-06-19: Taper Tantrum (Bernanke speech)
  3. 2015-08-24: China 811 devaluation / Black Monday
  4. 2018-12-24: Fed rate hike panic (Christmas Eve trough)
  5. 2020-02-24: COVID market collapse onset

For each event, compute metrics at T-60, T-30, T-10, T (event day)
using rolling windows of 30, 60, 90 trading days.

Also: full time-series of defect 2010-2021 to see the complete picture.

Metrics:
  - Prism duality defect δ
  - Mean pairwise correlation
  - Realized volatility (std of returns)
  - Newman-Girvan modularity
"""

import numpy as np
import sys, os
from datetime import date, timedelta
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

STOCKS = {
    "Financials": ["JPM", "BAC", "GS", "WFC", "C"],
    "Technology": ["AAPL", "MSFT", "INTC", "IBM", "ORCL"],
    "Energy":     ["XOM", "CVX", "COP", "SLB", "HAL"],
    "Healthcare": ["JNJ", "PFE", "MRK", "ABT", "MDT"],
    "Consumer":   ["PG", "KO", "WMT", "MCD", "PEP"],
    "Industrial": ["GE", "MMM", "CAT", "HON", "BA"],
}

TICKERS = []
for tickers in STOCKS.values():
    TICKERS.extend(tickers)

STRESS_EVENTS = [
    ("2011 US Downgrade",  "2011-08-05"),
    ("2013 Taper Tantrum", "2013-06-19"),
    ("2015 China Shock",   "2015-08-24"),
    ("2018 Fed Panic",     "2018-12-24"),
    ("2020 COVID Onset",   "2020-02-24"),
]

LOOKBACK_OFFSETS = [-90, -60, -30, -10, 0]
WINDOWS = [30, 60, 90]


def download_all(tickers, start, end):
    import yfinance as yf
    print(f"  Downloading {len(tickers)} tickers ({start} to {end})...")
    data = yf.download(tickers, start=start, end=end,
                       auto_adjust=True, progress=False)
    if hasattr(data.columns, 'levels'):
        data = data['Close']
    available = [t for t in tickers if t in data.columns]
    data = data[available].ffill().dropna(axis=1)
    print(f"  Got {len(data)} trading days, {len(data.columns)} tickers")
    return data, list(data.columns)


def corr_to_adjacency(corr, threshold=0.2):
    A = np.maximum(corr - threshold, 0)
    np.fill_diagonal(A, 0)
    return A


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
    P = (P + P.T) / 2
    return P


def duality_defect(L, P):
    comm = L @ P - P @ L
    return np.linalg.norm(comm, 'fro') / (np.linalg.norm(L, 'fro') + 1e-10)


def mean_offdiag(M):
    n = M.shape[0]
    return (M.sum() - np.trace(M)) / (n * (n - 1))


def modularity_fiedler(A):
    n = A.shape[0]
    m = A.sum() / 2
    if m < 1e-10:
        return 0.0
    L = laplacian(A)
    _, evecs = np.linalg.eigh(L)
    labels = (evecs[:, 1] >= 0).astype(int)
    k = A.sum(axis=1)
    Q = sum(A[i,j] - k[i]*k[j]/(2*m)
            for i in range(n) for j in range(n)
            if labels[i] == labels[j])
    return Q / (2 * m)


def compute_metrics(returns_window):
    corr = returns_window.corr().values
    A = corr_to_adjacency(corr)
    L = laplacian(A)
    P = fiedler_P(L)
    return {
        'defect':    duality_defect(L, P),
        'mean_corr': mean_offdiag(corr),
        'vol':       returns_window.std(axis=0).mean(),
        'modularity': modularity_fiedler(A),
    }


def event_idx(returns_df, event_date_str):
    import pandas as pd
    t = pd.Timestamp(event_date_str)
    idx = returns_df.index.searchsorted(t)
    return min(idx, len(returns_df) - 1)


def run_backtest():
    data, avail = download_all(TICKERS, "2009-06-01", "2021-06-30")
    returns = data.pct_change().dropna()

    print()
    print("=" * 78)
    print("Prism Historical Backtest: 2011-2020 Stress Events")
    print("=" * 78)
    print(f"Tickers: {len(avail)}, Trading days: {len(returns)}")

    # ── Per-event tables ──────────────────────────────────────────────────────
    summary_rows = []

    for event_name, event_date in STRESS_EVENTS:
        print(f"\n{'─'*78}")
        print(f"Event: {event_name} ({event_date})")

        eidx = event_idx(returns, event_date)

        for window in WINDOWS:
            print(f"\n  Window = {window} trading days:")
            print(f"  {'Metric':<18} {'T-90':>7} {'T-60':>7} {'T-30':>7} "
                  f"{'T-10':>7} {'T':>7}  {'T-60→T':>8}")
            print(f"  {'─'*66}")

            row_metrics = {}
            for offset in LOOKBACK_OFFSETS:
                end = eidx + offset
                start = end - window
                if start < 0 or end > len(returns):
                    row_metrics[offset] = None
                    continue
                row_metrics[offset] = compute_metrics(returns.iloc[start:end])

            for key, label in [
                ('defect',    'Duality defect δ'),
                ('mean_corr', 'Mean correlation'),
                ('vol',       'Realized vol'),
                ('modularity','Modularity'),
            ]:
                vals = [row_metrics.get(o, {}) or {} for o in LOOKBACK_OFFSETS]
                vs = [v.get(key, float('nan')) for v in vals]

                t60_val = row_metrics.get(-60, {}) or {}
                t0_val  = row_metrics.get(0,   {}) or {}
                v60 = t60_val.get(key, float('nan'))
                v0  = t0_val.get(key, float('nan'))
                delta = v0 - v60 if not (np.isnan(v60) or np.isnan(v0)) else float('nan')

                cells = "".join(f" {v:>7.3f}" if not np.isnan(v) else f" {'n/a':>7}"
                                for v in vs)
                delta_str = f"{delta:>+8.3f}" if not np.isnan(delta) else f"{'n/a':>8}"
                print(f"  {label:<18}{cells}  {delta_str}")

            if window == 60:
                m60 = row_metrics.get(-60) or {}
                m0  = row_metrics.get(0)   or {}
                summary_rows.append({
                    'event': event_name,
                    'd_t60': m60.get('defect', np.nan),
                    'd_t0':  m0.get('defect', np.nan),
                    'c_t60': m60.get('mean_corr', np.nan),
                    'c_t0':  m0.get('mean_corr', np.nan),
                    'v_t60': m60.get('vol', np.nan),
                    'v_t0':  m0.get('vol', np.nan),
                })

    # ── Full time-series: rolling 60d defect 2010-2021 ───────────────────────
    print(f"\n\n{'='*78}")
    print("Rolling 60-day Duality Defect: 2010-2021 (every 21 trading days)")
    print(f"{'='*78}")
    print(f"  {'Date':<12} {'Defect':>8} {'Mean corr':>10} {'Vol':>8}  Notes")
    print(f"  {'─'*60}")

    import pandas as pd
    event_dates = {pd.Timestamp(d): n for n, d in STRESS_EVENTS}

    step = 21
    window = 60
    for i in range(window, len(returns), step):
        window_ret = returns.iloc[i-window:i]
        m = compute_metrics(window_ret)
        dt = returns.index[i]

        note = ""
        for ed, en in event_dates.items():
            diff = abs((dt - ed).days)
            if diff < 20:
                note = f"<< {en}"
                break

        print(f"  {str(dt.date()):<12} {m['defect']:>8.3f} {m['mean_corr']:>10.3f} "
              f"{m['vol']:>8.4f}  {note}")

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n\n{'='*78}")
    print("Summary: Defect and Correlation change T-60 → T (60d window)")
    print(f"{'='*78}")
    print(f"  {'Event':<25} {'δ(T-60)':>8} {'δ(T)':>8} {'Δδ':>7}  "
          f"{'ρ(T-60)':>8} {'ρ(T)':>8} {'Δρ':>7}  {'vol Δ':>7}")
    print(f"  {'─'*76}")

    for r in summary_rows:
        dd = r['d_t0'] - r['d_t60']
        dc = r['c_t0'] - r['c_t60']
        dv = r['v_t0'] - r['v_t60']
        print(f"  {r['event']:<25} {r['d_t60']:>8.3f} {r['d_t0']:>8.3f} {dd:>+7.3f}  "
              f"{r['c_t60']:>8.3f} {r['c_t0']:>8.3f} {dc:>+7.3f}  {dv:>+7.4f}")

    print(f"\n  Key: Δδ = defect change, Δρ = correlation change, vol Δ = volatility change")
    print(f"  Positive Δδ with negative/flat Δρ = structural stress without surface signal")


if __name__ == "__main__":
    run_backtest()
