"""
Node Decomposition v2: S&P 100 universe, 120-day window, quarterly step.

Changes from v1:
  - Universe: S&P 100 (top 100 by market cap) instead of 30 hand-picked
  - Window: 120 trading days (~6 months) instead of 60
  - Step: 63 days (~quarterly) instead of 21 (monthly)
  - Threshold: correlation > 0.3 (stricter) to reduce noise in adjacency

Hypothesis: with more nodes and longer window, genuine structural leaders
should emerge and persist across quarters rather than flipping monthly.
"""

import numpy as np
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


# S&P 100 components (as of ~2023, using tickers that existed since 2016)
SP100 = [
    "AAPL", "ABBV", "ABT", "ACN", "ADBE", "AIG", "AMGN", "AMZN", "AXP", "BA",
    "BAC", "BK", "BLK", "BMY", "BRK-B", "C", "CAT", "CHTR", "CL", "CMCSA",
    "COF", "COP", "COST", "CRM", "CSCO", "CVS", "CVX", "D", "DHR", "DIS",
    "DOW", "DUK", "EMR", "EXC", "F", "FDX", "GD", "GE", "GILD", "GM",
    "GOOGL", "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "KHC", "KO",
    "LIN", "LLY", "LMT", "LOW", "MA", "MCD", "MDLZ", "MDT", "MET", "META",
    "MMM", "MO", "MRK", "MS", "MSFT", "NEE", "NFLX", "NKE", "NVDA", "ORCL",
    "PEP", "PFE", "PG", "PM", "PYPL", "QCOM", "RTX", "SBUX", "SLB", "SO",
    "SPG", "T", "TGT", "TMO", "TMUS", "TXN", "UNH", "UNP", "UPS", "USB",
    "V", "VZ", "WBA", "WFC", "WMT", "XOM",
]

SECTOR_MAP = {
    # Technology
    "AAPL": "Tech", "ADBE": "Tech", "AMZN": "Tech", "CRM": "Tech",
    "CSCO": "Tech", "GOOGL": "Tech", "IBM": "Tech", "INTC": "Tech",
    "META": "Tech", "MSFT": "Tech", "NFLX": "Tech", "NVDA": "Tech",
    "ORCL": "Tech", "PYPL": "Tech", "QCOM": "Tech", "TXN": "Tech",
    # Financials
    "AIG": "Fin", "AXP": "Fin", "BAC": "Fin", "BK": "Fin", "BLK": "Fin",
    "BRK-B": "Fin", "C": "Fin", "COF": "Fin", "GS": "Fin", "JPM": "Fin",
    "MA": "Fin", "MET": "Fin", "MS": "Fin", "SPG": "Fin", "USB": "Fin",
    "V": "Fin", "WFC": "Fin",
    # Healthcare
    "ABBV": "Health", "ABT": "Health", "AMGN": "Health", "BMY": "Health",
    "CVS": "Health", "DHR": "Health", "GILD": "Health", "JNJ": "Health",
    "LLY": "Health", "MDT": "Health", "MRK": "Health", "PFE": "Health",
    "TMO": "Health", "UNH": "Health",
    # Consumer
    "CHTR": "Cons", "CL": "Cons", "CMCSA": "Cons", "COST": "Cons",
    "DIS": "Cons", "HD": "Cons", "KHC": "Cons", "KO": "Cons", "LOW": "Cons",
    "MCD": "Cons", "MDLZ": "Cons", "MO": "Cons", "NKE": "Cons",
    "PEP": "Cons", "PG": "Cons", "PM": "Cons", "SBUX": "Cons",
    "TGT": "Cons", "TMUS": "Cons", "VZ": "Cons", "WBA": "Cons",
    "WMT": "Cons", "T": "Cons",
    # Energy
    "COP": "Energy", "CVX": "Energy", "SLB": "Energy", "XOM": "Energy",
    # Industrial
    "BA": "Indust", "CAT": "Indust", "DOW": "Indust", "EMR": "Indust",
    "F": "Indust", "FDX": "Indust", "GD": "Indust", "GE": "Indust",
    "GM": "Indust", "HON": "Indust", "LIN": "Indust", "LMT": "Indust",
    "MMM": "Indust", "RTX": "Indust", "UNP": "Indust", "UPS": "Indust",
    # Utilities
    "D": "Util", "DUK": "Util", "EXC": "Util", "NEE": "Util", "SO": "Util",
    "ACN": "Tech",
}


def download_sp100(start="2016-01-01", end="2023-12-31"):
    import yfinance as yf
    print(f"Downloading {len(SP100)} S&P 100 tickers...")
    data = yf.download(SP100, start=start, end=end,
                       auto_adjust=True, progress=False)
    if isinstance(data.columns, pd.MultiIndex):
        data = data['Close']
    # Keep tickers with >80% data coverage
    min_days = len(data) * 0.8
    available = [t for t in SP100 if t in data.columns and data[t].notna().sum() > min_days]
    data = data[available].ffill().dropna(axis=1)
    print(f"Got {len(data)} trading days, {len(data.columns)} tickers (>{min_days:.0f} days required)")
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


def compute_decomposition(returns_window):
    corr = returns_window.corr().values
    if np.any(np.isnan(corr)):
        return None, None
    n = corr.shape[0]
    A = np.maximum(corr - 0.3, 0)  # stricter threshold
    np.fill_diagonal(A, 0)
    if A.sum() < 1e-10:
        return None, None
    L = laplacian(A)
    P = fiedler_P(L)
    comm = L @ P - P @ L
    L_norm = np.linalg.norm(L, 'fro') + 1e-10
    global_defect = np.linalg.norm(comm, 'fro') / L_norm
    node_defects = np.linalg.norm(comm, axis=1) / L_norm
    return global_defect, node_defects


def herfindahl(contributions):
    if contributions.sum() < 1e-10:
        return 0
    shares = contributions / contributions.sum()
    return (shares ** 2).sum()


def run():
    data, avail = download_sp100()
    returns = data.pct_change().dropna()
    n_stocks = len(avail)

    print()
    print("=" * 80)
    print("NODE DECOMPOSITION v2: S&P 100, 120-day window, quarterly")
    print("=" * 80)
    print(f"Universe: {n_stocks} stocks")
    print(f"Period: {returns.index[0].date()} to {returns.index[-1].date()}")
    print(f"Window: 120 trading days, Step: 63 days (~quarterly)")
    print()

    window = 120
    step = 63

    records = []
    for i in range(window, len(returns), step):
        w = returns.iloc[i-window:i]
        dt = returns.index[i]
        global_d, node_d = compute_decomposition(w)
        if global_d is None:
            continue

        total = node_d.sum()
        top10_idx = np.argsort(node_d)[::-1][:10]

        record = {
            'date': dt,
            'global_defect': global_d,
            'herfindahl': herfindahl(node_d),
            'top5_pct': sum(node_d[np.argsort(node_d)[::-1][:5]]) / total * 100,
            'top10_pct': sum(node_d[top10_idx]) / total * 100,
        }

        # Sector aggregation
        sector_totals = {}
        for j, t in enumerate(avail):
            s = SECTOR_MAP.get(t, 'Other')
            sector_totals[s] = sector_totals.get(s, 0) + node_d[j]
        for s, v in sector_totals.items():
            record[f'sector_{s}'] = v / total * 100

        # Top 5 individual contributors
        for rank in range(5):
            idx = top10_idx[rank]
            record[f'top{rank+1}'] = avail[idx]
            record[f'top{rank+1}_pct'] = node_d[idx] / total * 100

        records.append(record)

    df = pd.DataFrame(records)
    print(f"Computed {len(df)} quarterly snapshots\n")

    # ── SECTOR HEATMAP ──────────────────────────────────────────────────────
    print("=" * 80)
    print("SECTOR STRUCTURAL PRESSURE (% of total defect)")
    print("=" * 80)

    all_sectors = sorted(set(SECTOR_MAP.values()))
    sector_cols = [f'sector_{s}' for s in all_sectors if f'sector_{s}' in df.columns]
    sector_names = [c.replace('sector_', '') for c in sector_cols]

    print(f"\n  {'Date':<12} {'d':>5}", end="")
    for s in sector_names:
        print(f" {s[:5]:>6}", end="")
    print(f" {'HHI':>6} {'Top5%':>6}  Top contributor")
    print(f"  {'-'*105}")

    for _, row in df.iterrows():
        print(f"  {str(row['date'].date()):<12} {row['global_defect']:>5.2f}", end="")
        for sc in sector_cols:
            val = row.get(sc, 0)
            print(f" {val:>5.1f}%", end="")
        print(f" {row['herfindahl']:>6.3f} {row['top5_pct']:>5.1f}%  "
              f"{row['top1']}({row['top1_pct']:.1f}%)")

    # ── PERSISTENCE ANALYSIS ────────────────────────────────────────────────
    print()
    print("=" * 80)
    print("PERSISTENCE: Do top contributors stay on top?")
    print("=" * 80)

    # For each quarter, check if top-5 overlaps with previous quarter's top-5
    print(f"\n  {'Period':<25} {'Overlap with prev top-5':>25} {'New entrants'}")
    print(f"  {'-'*70}")

    for i in range(1, len(df)):
        prev_top5 = set(df.iloc[i-1][[f'top{r}' for r in range(1,6)]].values)
        curr_top5 = set(df.iloc[i][[f'top{r}' for r in range(1,6)]].values)
        overlap = prev_top5 & curr_top5
        new = curr_top5 - prev_top5
        period = f"{df.iloc[i-1]['date'].date()} -> {df.iloc[i]['date'].date()}"
        print(f"  {period:<25} {len(overlap)}/5 ({', '.join(sorted(overlap)) if overlap else 'none':<20}) "
              f"{', '.join(sorted(new))}")

    # ── STRUCTURAL REGIME DETECTION ─────────────────────────────────────────
    print()
    print("=" * 80)
    print("STRUCTURAL REGIMES: Concentrated vs Diffuse pressure")
    print("=" * 80)

    median_hhi = df['herfindahl'].median()
    median_top5 = df['top5_pct'].median()

    print(f"\n  Median HHI: {median_hhi:.4f} (uniform = {1/n_stocks:.4f})")
    print(f"  Median Top-5 concentration: {median_top5:.1f}%")
    print(f"  (If top-5 = {5/n_stocks*100:.1f}% that's uniform distribution)")

    concentrated = df[df['top5_pct'] > df['top5_pct'].quantile(0.75)]
    diffuse = df[df['top5_pct'] < df['top5_pct'].quantile(0.25)]

    print(f"\n  CONCENTRATED quarters (top-5 > {df['top5_pct'].quantile(0.75):.1f}%):")
    print(f"  {'Date':<12} {'Defect':>7} {'Top5%':>6}  Top contributors")
    print(f"  {'-'*70}")
    for _, row in concentrated.iterrows():
        tops = f"{row['top1']}({row['top1_pct']:.1f}%), {row['top2']}({row['top2_pct']:.1f}%), {row['top3']}({row['top3_pct']:.1f}%)"
        print(f"  {str(row['date'].date()):<12} {row['global_defect']:>7.3f} {row['top5_pct']:>5.1f}%  {tops}")

    print(f"\n  DIFFUSE quarters (top-5 < {df['top5_pct'].quantile(0.25):.1f}%):")
    print(f"  {'Date':<12} {'Defect':>7} {'Top5%':>6}  Top contributors")
    print(f"  {'-'*70}")
    for _, row in diffuse.iterrows():
        tops = f"{row['top1']}({row['top1_pct']:.1f}%), {row['top2']}({row['top2_pct']:.1f}%), {row['top3']}({row['top3_pct']:.1f}%)"
        print(f"  {str(row['date'].date()):<12} {row['global_defect']:>7.3f} {row['top5_pct']:>5.1f}%  {tops}")

    # ── DOES CONCENTRATION PREDICT ANYTHING? ────────────────────────────────
    print()
    print("=" * 80)
    print("PREDICTIVE TEST: Does concentration predict future defect change?")
    print("=" * 80)

    df['defect_change'] = df['global_defect'].shift(-1) - df['global_defect']
    valid = df.dropna(subset=['defect_change'])

    if len(valid) > 5:
        corr_hhi = valid['herfindahl'].corr(valid['defect_change'])
        corr_top5 = valid['top5_pct'].corr(valid['defect_change'])
        print(f"\n  Corr(HHI, next-quarter defect change): {corr_hhi:.3f}")
        print(f"  Corr(Top5%, next-quarter defect change): {corr_top5:.3f}")

        high_conc = valid[valid['top5_pct'] > median_top5]
        low_conc = valid[valid['top5_pct'] <= median_top5]
        print(f"\n  When concentrated: mean next-quarter defect change = {high_conc['defect_change'].mean():.3f}")
        print(f"  When diffuse:      mean next-quarter defect change = {low_conc['defect_change'].mean():.3f}")

    # ── SECTOR DOMINANCE STABILITY ──────────────────────────────────────────
    print()
    print("=" * 80)
    print("SECTOR DOMINANCE STABILITY (consecutive quarters as #1)")
    print("=" * 80)

    df['top_sector'] = df['top1'].map(lambda t: SECTOR_MAP.get(t, 'Other'))

    # Find longest runs
    runs = []
    current_sector = None
    run_start = None
    run_length = 0
    for _, row in df.iterrows():
        if row['top_sector'] == current_sector:
            run_length += 1
        else:
            if current_sector is not None and run_length > 1:
                runs.append((run_start, row['date'], current_sector, run_length))
            current_sector = row['top_sector']
            run_start = row['date']
            run_length = 1
    if run_length > 1:
        runs.append((run_start, df.iloc[-1]['date'], current_sector, run_length))

    if runs:
        print(f"\n  Sustained sector dominance (>1 consecutive quarter):")
        print(f"  {'Start':<12} {'End':<12} {'Sector':<10} {'Quarters':>9}")
        print(f"  {'-'*48}")
        for start, end, sector, length in sorted(runs, key=lambda x: -x[3]):
            print(f"  {str(start.date()):<12} {str(end.date()):<12} {sector:<10} {length:>9}")
    else:
        print("\n  No sector maintained top position for >1 consecutive quarter.")
        print("  The fault line rotates every quarter at this resolution.")


if __name__ == "__main__":
    run()
