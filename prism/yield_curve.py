"""
Prism on the US Treasury yield curve.

Nodes = maturities (1m, 3m, 6m, 1y, 2y, 3y, 5y, 7y, 10y, 20y, 30y)
Edges = correlation of yield changes over rolling window

Key question: does duality defect rise before yield curve inversions?
Yield curve inversion (2y-10y spread going negative) is a classic
recession predictor. If Prism detects structural stress in the yield
curve before the inversion becomes visible, that's a new signal.

Known inversions:
  - 2019-08-14: 2y-10y inverted briefly (pre-COVID recession signal)
  - 2022-07-05: 2y-10y inverted and stayed inverted for months

We use FRED data via yfinance treasury tickers.
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


# Treasury yield tickers on Yahoo Finance
TREASURY_TICKERS = {
    "^IRX": "3m",    # 13-week T-bill
    "^FVX": "5y",    # 5-year
    "^TNX": "10y",   # 10-year
    "^TYX": "30y",   # 30-year
}

# Better: use pandas_datareader for FRED, or construct from ETFs
# For broader coverage, use treasury ETFs as proxies
TREASURY_ETFS = {
    "SHV":  "0-1y",
    "SHY":  "1-3y",
    "IEI":  "3-7y",
    "IEF":  "7-10y",
    "TLH":  "10-20y",
    "TLT":  "20+y",
}


def download_treasury_etfs(start, end):
    import yfinance as yf
    tickers = list(TREASURY_ETFS.keys())
    print(f"  Downloading treasury ETFs: {tickers}")
    data = yf.download(tickers, start=start, end=end,
                       auto_adjust=True, progress=False)
    if hasattr(data.columns, 'levels'):
        data = data['Close']
    available = [t for t in tickers if t in data.columns]
    data = data[available].ffill().dropna(axis=1)
    print(f"  Got {len(data)} trading days, {len(data.columns)} ETFs")
    return data, available


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


def duality_defect(L, P):
    comm = L @ P - P @ L
    return np.linalg.norm(comm, 'fro') / (np.linalg.norm(L, 'fro') + 1e-10)


def mean_offdiag(M):
    n = M.shape[0]
    return (M.sum() - np.trace(M)) / (n * (n - 1))


def compute_yield_curve_metrics(returns_window):
    corr = returns_window.corr().values
    n = corr.shape[0]
    # For yield curve: use absolute correlation (all maturities should move together)
    A = np.maximum(np.abs(corr) - 0.3, 0)
    np.fill_diagonal(A, 0)
    L = laplacian(A)
    P = fiedler_P(L)
    return {
        'defect': duality_defect(L, P),
        'mean_corr': mean_offdiag(corr),
    }


def run_yield_curve_analysis():
    import pandas as pd

    data, avail = download_treasury_etfs("2015-01-01", "2023-12-31")
    returns = data.pct_change().dropna()

    print()
    print("=" * 72)
    print("Prism on US Treasury Yield Curve (ETF proxies)")
    print("=" * 72)
    print(f"ETFs: {[f'{t} ({TREASURY_ETFS[t]})' for t in avail]}")
    print(f"Period: {returns.index[0].date()} to {returns.index[-1].date()}")
    print()

    # Rolling 60-day analysis
    window = 60
    step = 10

    # Known events
    events = {
        pd.Timestamp("2019-08-14"): "2y-10y inversion",
        pd.Timestamp("2020-02-24"): "COVID onset",
        pd.Timestamp("2022-07-05"): "2y-10y sustained inversion",
    }

    print(f"Rolling {window}-day defect (step={step} days):")
    print(f"  {'Date':<12} {'Defect':>8} {'Mean corr':>10}  Notes")
    print(f"  {'-'*55}")

    series = []
    for i in range(window, len(returns), step):
        w = returns.iloc[i-window:i]
        m = compute_yield_curve_metrics(w)
        dt = returns.index[i]

        note = ""
        for ed, en in events.items():
            if abs((dt - ed).days) < 15:
                note = f"<< {en}"
                break

        series.append({'date': dt, **m})
        print(f"  {str(dt.date()):<12} {m['defect']:>8.3f} {m['mean_corr']:>10.3f}  {note}")

    # Summary statistics
    defects = [s['defect'] for s in series]
    print(f"\n  Defect range: {min(defects):.3f} - {max(defects):.3f}")
    print(f"  Defect mean:  {np.mean(defects):.3f}")
    print(f"  Defect std:   {np.std(defects):.3f}")

    # Pre-event analysis
    print(f"\n\n{'='*72}")
    print("Pre-Event Defect Levels")
    print(f"{'='*72}")

    for event_date, event_name in events.items():
        print(f"\n  {event_name} ({event_date.date()}):")
        for offset_label, offset_days in [("T-90", -90), ("T-60", -60),
                                           ("T-30", -30), ("T", 0)]:
            target = event_date + pd.Timedelta(days=offset_days)
            idx = returns.index.searchsorted(target)
            idx = min(idx, len(returns) - 1)
            if idx < window:
                print(f"    {offset_label}: insufficient data")
                continue
            w = returns.iloc[idx-window:idx]
            m = compute_yield_curve_metrics(w)
            print(f"    {offset_label}: defect={m['defect']:.3f}, corr={m['mean_corr']:.3f}")


if __name__ == "__main__":
    run_yield_curve_analysis()
