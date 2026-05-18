"""
Prism Node Decomposition Time Series: Structural Pressure Heatmap

Rolling per-node defect contribution over 2016-2023. This is the product:
a risk manager sees WHO is driving structural fragility at any point in time,
and how the fault line migrates between regimes.

Output:
  - Monthly per-node defect contribution (% of total)
  - Sector-level aggregation
  - Fault line migration events (when top contributors change)
  - Concentration risk metric (how concentrated is the defect?)
"""

import numpy as np
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


STOCKS = {
    "Financials": ["JPM", "BAC", "GS", "WFC", "C"],
    "Technology": ["AAPL", "MSFT", "GOOGL", "AMZN", "META"],
    "Energy":     ["XOM", "CVX", "COP", "SLB", "EOG"],
    "Healthcare": ["JNJ", "PFE", "UNH", "MRK", "ABT"],
    "Consumer":   ["PG", "KO", "WMT", "COST", "MCD"],
    "Industrial": ["GE", "MMM", "CAT", "HON", "BA"],
}
TICKERS = [t for tickers in STOCKS.values() for t in tickers]
SECTOR_MAP = {}
for sector, tickers in STOCKS.items():
    for t in tickers:
        SECTOR_MAP[t] = sector


def download_all(tickers, start, end):
    import yfinance as yf
    print(f"Downloading {len(tickers)} tickers ({start} to {end})...")
    data = yf.download(tickers, start=start, end=end,
                       auto_adjust=True, progress=False)
    if isinstance(data.columns, pd.MultiIndex):
        data = data['Close']
    available = [t for t in tickers if t in data.columns and data[t].notna().sum() > 200]
    data = data[available].ffill().dropna(axis=1)
    print(f"Got {len(data)} trading days, {len(data.columns)} tickers")
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
    A = np.maximum(corr - 0.2, 0)
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
    """Concentration index: 1/n = perfectly spread, 1 = one node dominates."""
    if contributions.sum() < 1e-10:
        return 0
    shares = contributions / contributions.sum()
    return (shares ** 2).sum()


def run_time_series():
    data, avail = download_all(TICKERS, "2016-01-01", "2023-12-31")
    returns = data.pct_change().dropna()

    print()
    print("=" * 80)
    print("STRUCTURAL PRESSURE HEATMAP: Rolling Per-Node Defect Decomposition")
    print("=" * 80)
    print(f"Universe: {len(avail)} stocks across {len(STOCKS)} sectors")
    print(f"Period: {returns.index[0].date()} to {returns.index[-1].date()}")
    print()

    window = 60  # trading days
    step = 21    # ~monthly

    records = []
    for i in range(window, len(returns), step):
        w = returns.iloc[i-window:i]
        dt = returns.index[i]
        global_d, node_d = compute_decomposition(w)
        if global_d is None:
            continue

        record = {
            'date': dt,
            'global_defect': global_d,
            'herfindahl': herfindahl(node_d),
        }
        # Per-node contribution as % of total
        total = node_d.sum()
        for j, ticker in enumerate(avail):
            record[f'pct_{ticker}'] = node_d[j] / total * 100 if total > 0 else 0

        # Sector aggregation
        for sector in STOCKS:
            sector_pct = sum(
                node_d[j] / total * 100
                for j, t in enumerate(avail)
                if SECTOR_MAP.get(t) == sector
            ) if total > 0 else 0
            record[f'sector_{sector}'] = sector_pct

        # Top 3 contributors
        top3_idx = np.argsort(node_d)[::-1][:3]
        record['top1'] = avail[top3_idx[0]]
        record['top1_pct'] = node_d[top3_idx[0]] / total * 100 if total > 0 else 0
        record['top2'] = avail[top3_idx[1]]
        record['top2_pct'] = node_d[top3_idx[1]] / total * 100 if total > 0 else 0
        record['top3'] = avail[top3_idx[2]]
        record['top3_pct'] = node_d[top3_idx[2]] / total * 100 if total > 0 else 0

        records.append(record)

    df = pd.DataFrame(records)
    print(f"Computed {len(df)} monthly snapshots\n")

    # ── SECTOR HEATMAP ──────────────────────────────────────────────────────
    print("=" * 80)
    print("SECTOR CONTRIBUTION OVER TIME (% of total defect)")
    print("=" * 80)
    sector_cols = [c for c in df.columns if c.startswith('sector_')]
    sectors = [c.replace('sector_', '') for c in sector_cols]

    print(f"\n  {'Date':<12} {'Global':>7}", end="")
    for s in sectors:
        print(f" {s[:6]:>7}", end="")
    print(f" {'HHI':>6}  Top contributor")
    print(f"  {'-'*100}")

    for _, row in df.iterrows():
        print(f"  {str(row['date'].date()):<12} {row['global_defect']:>7.3f}", end="")
        for sc in sector_cols:
            print(f" {row[sc]:>6.1f}%", end="")
        print(f" {row['herfindahl']:>6.3f}  {row['top1']} ({row['top1_pct']:.1f}%)")

    # ── FAULT LINE MIGRATION ────────────────────────────────────────────────
    print()
    print("=" * 80)
    print("FAULT LINE MIGRATION: When does the top sector change?")
    print("=" * 80)

    df['top_sector'] = df.apply(
        lambda r: SECTOR_MAP.get(r['top1'], '?'), axis=1)

    prev_sector = None
    migrations = []
    for _, row in df.iterrows():
        if row['top_sector'] != prev_sector and prev_sector is not None:
            migrations.append({
                'date': row['date'],
                'from': prev_sector,
                'to': row['top_sector'],
                'new_leader': row['top1'],
                'defect': row['global_defect'],
            })
        prev_sector = row['top_sector']

    print(f"\n  {len(migrations)} fault line migrations detected:\n")
    print(f"  {'Date':<12} {'From':<12} {'To':<12} {'New leader':<10} {'Defect':>7}")
    print(f"  {'-'*58}")
    for m in migrations:
        print(f"  {str(m['date'].date()):<12} {m['from']:<12} {m['to']:<12} "
              f"{m['new_leader']:<10} {m['defect']:>7.3f}")

    # ── CONCENTRATION ANALYSIS ──────────────────────────────────────────────
    print()
    print("=" * 80)
    print("CONCENTRATION RISK: How concentrated is the structural pressure?")
    print("=" * 80)

    print(f"\n  HHI range: {df['herfindahl'].min():.3f} - {df['herfindahl'].max():.3f}")
    print(f"  HHI mean:  {df['herfindahl'].mean():.3f}")
    print(f"  (1/{len(avail)} = {1/len(avail):.3f} = perfectly spread)")
    print(f"  (1.0 = one node dominates)")

    # Top-3 concentration
    df['top3_total'] = df['top1_pct'] + df['top2_pct'] + df['top3_pct']
    print(f"\n  Top-3 concentration: {df['top3_total'].mean():.1f}% average "
          f"(range {df['top3_total'].min():.1f}% - {df['top3_total'].max():.1f}%)")

    # Periods of extreme concentration
    high_conc = df[df['herfindahl'] > df['herfindahl'].quantile(0.80)]
    if len(high_conc) > 0:
        print(f"\n  High-concentration periods (top 20% HHI):")
        print(f"  {'Date':<12} {'HHI':>6} {'Top1':<8} {'Top1%':>6} {'Global d':>9}")
        print(f"  {'-'*48}")
        for _, row in high_conc.iterrows():
            print(f"  {str(row['date'].date()):<12} {row['herfindahl']:>6.3f} "
                  f"{row['top1']:<8} {row['top1_pct']:>5.1f}% {row['global_defect']:>9.3f}")

    # ── ANNUAL SECTOR DOMINANCE ─────────────────────────────────────────────
    print()
    print("=" * 80)
    print("ANNUAL SECTOR DOMINANCE")
    print("=" * 80)

    df['year'] = df['date'].dt.year
    print(f"\n  {'Year':<6}", end="")
    for s in sectors:
        print(f" {s[:6]:>7}", end="")
    print(f" {'Dominant':>12}")
    print(f"  {'-'*80}")

    for year, group in df.groupby('year'):
        print(f"  {year:<6}", end="")
        sector_means = {}
        for sc in sector_cols:
            mean_val = group[sc].mean()
            sector_means[sc.replace('sector_', '')] = mean_val
            print(f" {mean_val:>6.1f}%", end="")
        dominant = max(sector_means, key=sector_means.get)
        print(f" {dominant:>12}")

    # ── KEY NARRATIVE EVENTS ────────────────────────────────────────────────
    print()
    print("=" * 80)
    print("KEY NARRATIVE EVENTS")
    print("=" * 80)

    events = {
        "2017-01": "Trump inauguration, deregulation hopes",
        "2017-09": "Peak fragility period begins",
        "2018-02": "Volmageddon",
        "2018-12": "Fed tightening peak, near-bear market",
        "2019-08": "Yield curve inversion",
        "2020-03": "COVID crash",
        "2020-11": "Vaccine announcement",
        "2021-01": "GameStop / meme stocks",
        "2021-11": "Inflation spike confirmed",
        "2022-01": "Fed pivot hawkish",
        "2022-06": "Bear market official",
        "2023-03": "SVB collapse",
    }

    print()
    for _, row in df.iterrows():
        ym = row['date'].strftime('%Y-%m')
        if ym in events:
            print(f"  {ym}  defect={row['global_defect']:.3f}  "
                  f"top={row['top1']}({row['top1_pct']:.1f}%)  "
                  f"HHI={row['herfindahl']:.3f}  | {events[ym]}")

    # ── PRODUCT SUMMARY ─────────────────────────────────────────────────────
    print()
    print("=" * 80)
    print("PRODUCT VALUE SUMMARY")
    print("=" * 80)
    print("""
  What a risk manager gets from this:

  1. WHO is driving fragility right now (top contributors)
  2. Is the pressure concentrated or diffuse (HHI)
  3. Has the fault line shifted recently (migration events)
  4. Which sector is the structural pressure point (sector dominance)

  Actionable decisions:
  - If top contributor is in your portfolio: hedge or reduce
  - If HHI is high: single-name risk, not systemic
  - If fault line just migrated: regime change, reassess
  - If your sector dominates: sector-wide structural stress
""")


if __name__ == "__main__":
    run_time_series()
