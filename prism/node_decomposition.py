"""
Prism per-node defect decomposition.

The commutator [L, P] = LP - PL is an n×n matrix. Its Frobenius norm
gives the global defect. But we can decompose it per-node:

  node_defect(i) = ||row_i([L,P])||_2 / ||L||_F

This tells us which nodes contribute most to the symmetry breaking.
In financial networks: which stocks are driving structural fragility.

We run this on:
1. The 2017 high-defect regime (peak fragility)
2. The 2018 post-crash regime (resolved)
3. The 2020 pre-COVID regime

And compare: do the same nodes always drive defect, or does the
fault line shift?
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


STOCKS = {
    "Financials": ["JPM", "BAC", "GS", "WFC", "C"],
    "Technology": ["AAPL", "MSFT", "INTC", "IBM", "ORCL"],
    "Energy":     ["XOM", "CVX", "COP", "SLB", "HAL"],
    "Healthcare": ["JNJ", "PFE", "MRK", "ABT", "MDT"],
    "Consumer":   ["PG", "KO", "WMT", "MCD", "PEP"],
    "Industrial": ["GE", "MMM", "CAT", "HON", "BA"],
}
TICKERS = [t for tickers in STOCKS.values() for t in tickers]
SECTOR_MAP = {}
for sector, tickers in STOCKS.items():
    for t in tickers:
        SECTOR_MAP[t] = sector


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


def per_node_defect(L, P):
    """Decompose duality defect per node."""
    comm = L @ P - P @ L
    L_norm = np.linalg.norm(L, 'fro') + 1e-10
    node_defects = np.linalg.norm(comm, axis=1) / L_norm
    return node_defects


def compute_window(returns_window, tickers):
    """Compute per-node defect for a window of returns."""
    corr = returns_window.corr().values
    A = np.maximum(corr - 0.2, 0)
    np.fill_diagonal(A, 0)
    L = laplacian(A)
    P = fiedler_P(L)

    global_defect = np.linalg.norm(L @ P - P @ L, 'fro') / (np.linalg.norm(L, 'fro') + 1e-10)
    node_d = per_node_defect(L, P)
    mean_corr = (corr.sum() - np.trace(corr)) / (len(corr) * (len(corr) - 1))

    return global_defect, mean_corr, node_d


def print_node_ranking(node_d, tickers, top_n=10):
    """Print top contributors to defect."""
    order = np.argsort(node_d)[::-1]
    print(f"  {'Rank':<5} {'Ticker':<7} {'Sector':<12} {'Node defect':>12} {'% of total':>10}")
    print(f"  {'-'*50}")
    total = node_d.sum()
    for rank, idx in enumerate(order[:top_n]):
        t = tickers[idx]
        sector = SECTOR_MAP.get(t, '?')
        pct = node_d[idx] / total * 100
        print(f"  {rank+1:<5} {t:<7} {sector:<12} {node_d[idx]:>12.4f} {pct:>9.1f}%")
    return order[:top_n]


def sector_contribution(node_d, tickers):
    """Aggregate defect by sector."""
    sector_totals = {}
    for i, t in enumerate(tickers):
        s = SECTOR_MAP.get(t, '?')
        sector_totals[s] = sector_totals.get(s, 0) + node_d[i]
    total = sum(sector_totals.values())
    print(f"\n  {'Sector':<12} {'Defect contrib':>14} {'% of total':>10}")
    print(f"  {'-'*40}")
    for s, v in sorted(sector_totals.items(), key=lambda x: -x[1]):
        print(f"  {s:<12} {v:>14.4f} {v/total*100:>9.1f}%")


def run_decomposition():
    import pandas as pd

    data, avail = download_all(TICKERS, "2016-01-01", "2021-06-30")
    returns = data.pct_change().dropna()

    print()
    print("=" * 72)
    print("Prism Per-Node Defect Decomposition")
    print("=" * 72)
    print(f"Tickers: {len(avail)}")

    # Define analysis windows
    windows = [
        ("2017 Peak Fragility (Nov)", "2017-09-01", "2017-11-30"),
        ("2018 Post-Crash (Mar-Apr)", "2018-02-01", "2018-04-30"),
        ("2019 Pre-COVID Build (Nov-Dec)", "2019-10-01", "2019-12-31"),
        ("2020 COVID Onset (Jan-Feb)", "2020-01-01", "2020-02-24"),
        ("2020 Post-COVID (Apr-May)", "2020-04-01", "2020-05-31"),
    ]

    all_rankings = {}

    for label, start, end in windows:
        print(f"\n{'─'*72}")
        print(f"Window: {label} ({start} to {end})")
        print(f"{'─'*72}")

        mask = (returns.index >= pd.Timestamp(start)) & (returns.index <= pd.Timestamp(end))
        w = returns.loc[mask]
        if len(w) < 20:
            print("  Insufficient data, skipping.")
            continue

        global_d, mean_c, node_d = compute_window(w, avail)
        print(f"  Global defect: {global_d:.4f}, Mean correlation: {mean_c:.3f}")
        print(f"  Window size: {len(w)} trading days\n")

        print("  Top defect contributors:")
        top = print_node_ranking(node_d, avail)
        sector_contribution(node_d, avail)
        all_rankings[label] = (node_d, avail)

    # ── Cross-window comparison ───────────────────────────────────────────
    print(f"\n\n{'='*72}")
    print("Cross-Window Comparison: Who drives fragility?")
    print(f"{'='*72}")

    labels = list(all_rankings.keys())
    if len(labels) >= 2:
        print(f"\n  Does the fault line shift between regimes?\n")
        print(f"  {'Ticker':<7} {'Sector':<12}", end="")
        for l in labels:
            short = l.split("(")[0].strip()[:12]
            print(f" {short:>12}", end="")
        print()
        print(f"  {'-'*(19 + 13*len(labels))}")

        # Show all tickers sorted by max contribution across windows
        max_contrib = np.zeros(len(avail))
        for label, (nd, _) in all_rankings.items():
            for i in range(len(avail)):
                max_contrib[i] = max(max_contrib[i], nd[i])

        order = np.argsort(max_contrib)[::-1]
        for idx in order[:15]:
            t = avail[idx]
            s = SECTOR_MAP.get(t, '?')
            print(f"  {t:<7} {s:<12}", end="")
            for label in labels:
                nd, _ = all_rankings[label]
                total = nd.sum()
                pct = nd[idx] / total * 100
                print(f" {pct:>11.1f}%", end="")
            print()

    print()


if __name__ == "__main__":
    run_decomposition()
