"""
Prism Financial Demo: Risk Community Detection in S&P 500

Three-part story:
  Part 1 — Historical validation: 2008 crisis (pre/crisis/post)
            Prism recovers stable communities even when correlations spike.
  Part 2 — Today's forecast: current 90-day correlation structure
            Prism identifies live risk communities and coupling strength.
  Part 3 — Duality defect as early-warning signal
            Track defect over rolling windows to detect regime change.
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
SECTOR_LABELS = []
for sector, tickers in STOCKS.items():
    TICKERS.extend(tickers)
    SECTOR_LABELS.extend([sector] * len(tickers))

N = len(TICKERS)
SECTOR_NAMES = list(STOCKS.keys())
GROUND_TRUTH = np.array([SECTOR_NAMES.index(s) for s in SECTOR_LABELS])


def download_prices(tickers, start, end):
    import yfinance as yf
    print(f"  Downloading {len(tickers)} tickers ({start} to {end})...")
    data = yf.download(tickers, start=start, end=end,
                       auto_adjust=True, progress=False)
    # yfinance 1.3+ returns MultiIndex columns: (field, ticker)
    if hasattr(data.columns, 'levels'):
        if 'Close' in data.columns.get_level_values(0):
            data = data['Close']
        elif 'close' in data.columns.get_level_values(0):
            data = data['close']
    # Keep only requested tickers that are present
    available = [t for t in tickers if t in data.columns]
    if not available:
        raise ValueError("No tickers downloaded successfully")
    data = data[available]
    # Drop rows where more than 20% of tickers have NaN
    threshold = int(len(available) * 0.8)
    data = data.dropna(thresh=threshold)
    # Forward-fill remaining NaNs, then drop any still-NaN columns
    data = data.ffill().dropna(axis=1)
    available = list(data.columns)
    if len(available) < len(tickers):
        missing = set(tickers) - set(available)
        print(f"  Warning: dropped {len(missing)} tickers with insufficient data")
    print(f"  Got {len(data)} trading days, {len(available)} tickers")
    return data, available


def corr_from_prices(data):
    returns = data.pct_change().dropna()
    return returns.corr().values


def corr_to_adjacency(corr: np.ndarray, threshold: float = 0.2) -> np.ndarray:
    A = np.maximum(corr - threshold, 0)
    np.fill_diagonal(A, 0)
    return A


def laplacian(A: np.ndarray) -> np.ndarray:
    D = np.diag(A.sum(axis=1))
    return D - A


def fiedler_cluster_k(L: np.ndarray, k: int) -> np.ndarray:
    from sklearn.cluster import KMeans
    _, evecs = np.linalg.eigh(L)
    V = evecs[:, 1:k+1]
    norms = np.linalg.norm(V, axis=1, keepdims=True)
    V = V / np.where(norms < 1e-10, 1.0, norms)
    return KMeans(n_clusters=k, n_init=20, random_state=42).fit_predict(V)


def nmi(pred, truth):
    from sklearn.metrics import normalized_mutual_info_score
    return normalized_mutual_info_score(truth, pred)


def duality_defect(L: np.ndarray, P: np.ndarray) -> float:
    comm = L @ P - P @ L
    return np.linalg.norm(comm, 'fro') / (np.linalg.norm(L, 'fro') + 1e-10)


def mean_offdiag(M):
    n = M.shape[0]
    return (M.sum() - np.trace(M)) / (n * (n - 1))


def print_communities(labels, tickers, sector_labels, title=""):
    from collections import defaultdict
    if title:
        print(f"\n  {title}")
    communities = defaultdict(list)
    for i, lbl in enumerate(labels):
        communities[lbl].append(f"{tickers[i]}({sector_labels[i][:3]})")
    for cid in sorted(communities):
        print(f"    Community {cid}: {', '.join(communities[cid])}")


def coupling_matrix(labels, corr, k):
    """Inter-community mean correlation (k x k matrix)."""
    C = np.zeros((k, k))
    counts = np.zeros((k, k))
    n = len(labels)
    for i in range(n):
        for j in range(n):
            if i != j:
                C[labels[i], labels[j]] += corr[i, j]
                counts[labels[i], labels[j]] += 1
    with np.errstate(invalid='ignore'):
        C = np.where(counts > 0, C / counts, 0)
    return C


# ─────────────────────────────────────────────────────────────────────────────
# Part 1: Historical validation (2008 crisis)
# ─────────────────────────────────────────────────────────────────────────────

def run_historical(tickers, sector_labels, ground_truth):
    from prism.unsupervised import unsupervised_prism
    k = len(SECTOR_NAMES)

    periods = [
        ("Pre-crisis",  "2006-01-01", "2007-06-30"),
        ("Crisis",      "2008-01-01", "2009-06-30"),
        ("Post-crisis", "2010-01-01", "2011-06-30"),
    ]

    print("\n" + "=" * 65)
    print("Part 1: Historical Validation — 2008 Financial Crisis")
    print("=" * 65)
    print(f"{'Period':<20} {'Mean corr':>10} {'Base NMI':>10} {'Prism NMI':>11} {'Winner':>8}")
    print("-" * 65)

    for period, start, end in periods:
        data, avail = download_prices(tickers, start, end)
        if len(avail) < 10:
            print(f"  {period}: insufficient data, skipping")
            continue

        # Remap ground truth to available tickers
        idx = [tickers.index(t) for t in avail]
        gt = ground_truth[idx]
        sl = [sector_labels[i] for i in idx]

        corr = corr_from_prices(data)
        A = corr_to_adjacency(corr)
        L = laplacian(A)

        base_labels = fiedler_cluster_k(L, k)
        base_nmi = nmi(base_labels, gt)

        res = unsupervised_prism(A, n_outer=20, verbose=False)
        prism_labels = fiedler_cluster_k(res.L_constrained, k)
        prism_nmi = nmi(prism_labels, gt)

        winner = "Prism" if prism_nmi > base_nmi + 0.02 else (
                 "tie"   if abs(prism_nmi - base_nmi) <= 0.02 else "Base")
        mc = mean_offdiag(corr)
        print(f"  {period:<18} {mc:>10.3f} {base_nmi:>10.3f} {prism_nmi:>11.3f} {winner:>8}")

    print("-" * 65)
    print("  NMI = Normalized Mutual Information with GICS sector labels.")


# ─────────────────────────────────────────────────────────────────────────────
# Part 2: Today's forecast
# ─────────────────────────────────────────────────────────────────────────────

def run_today_forecast(tickers, sector_labels):
    from prism.unsupervised import unsupervised_prism

    today = date.today()
    start_90 = today - timedelta(days=120)  # ~90 trading days
    start_30 = today - timedelta(days=45)

    print("\n" + "=" * 65)
    print(f"Part 2: Today's Forecast — {today}")
    print("=" * 65)

    data_90, avail = download_prices(tickers, start_90.isoformat(), today.isoformat())
    if len(avail) < 10:
        print("  Insufficient data for today's forecast.")
        return None

    sl_avail = [sector_labels[tickers.index(t)] for t in avail]
    n = len(avail)

    corr_90 = corr_from_prices(data_90)
    A_90 = corr_to_adjacency(corr_90)
    L_90 = laplacian(A_90)

    print(f"  Tickers available: {n}/{len(tickers)}")
    print(f"  Window: {start_90} to {today} (~90 trading days)")
    print(f"  Mean pairwise correlation: {mean_offdiag(corr_90):.3f}")

    # Prism community detection
    k = 6
    res = unsupervised_prism(A_90, n_outer=20, verbose=False)
    prism_labels = fiedler_cluster_k(res.L_constrained, k)
    base_labels  = fiedler_cluster_k(L_90, k)

    # Duality defect: structural health
    P_learned = res.P_learned
    defect_now = duality_defect(L_90, P_learned)

    print(f"\n  Duality defect (current): {defect_now:.4f}")
    print(f"  RMSE (Prism deformation): {res.rmse:.4f}")
    print(f"  Interpretation: {'LOW — market structure is coherent' if defect_now < 0.3 else 'ELEVATED — structural stress detected' if defect_now < 0.5 else 'HIGH — regime instability'}")

    print_communities(prism_labels, avail, sl_avail, "Prism risk communities (today):")
    print_communities(base_labels,  avail, sl_avail, "Baseline communities (today):")

    # Inter-community coupling
    C = coupling_matrix(prism_labels, corr_90, k)
    nonempty = sorted(set(prism_labels))
    print(f"\n  Inter-community coupling matrix (mean correlation):")
    header = "       " + "".join(f"  C{c}" for c in nonempty)
    print(f"  {header}")
    for i in nonempty:
        row = "".join(f"  {C[i,j]:.2f}" for j in nonempty)
        print(f"    C{i}  {row}")

    # 30-day vs 90-day: is structure changing?
    data_30, avail_30 = download_prices(avail, start_30.isoformat(), today.isoformat())
    if len(avail_30) >= 10:
        corr_30 = corr_from_prices(data_30)
        A_30 = corr_to_adjacency(corr_30)
        L_30 = laplacian(A_30)
        res_30 = unsupervised_prism(A_30, n_outer=20, verbose=False)
        defect_30 = duality_defect(L_30, res_30.P_learned)
        mc_30 = mean_offdiag(corr_30)

        print(f"\n  Trend (30-day vs 90-day):")
        print(f"    Mean correlation:  90d={mean_offdiag(corr_90):.3f}  30d={mc_30:.3f}  "
              f"{'rising' if mc_30 > mean_offdiag(corr_90) + 0.02 else 'falling' if mc_30 < mean_offdiag(corr_90) - 0.02 else 'stable'}")
        print(f"    Duality defect:    90d={defect_now:.4f}  30d={defect_30:.4f}  "
              f"{'rising (stress)' if defect_30 > defect_now + 0.02 else 'falling (stabilizing)' if defect_30 < defect_now - 0.02 else 'stable'}")

    return prism_labels, avail, sl_avail, corr_90, defect_now


# ─────────────────────────────────────────────────────────────────────────────
# Part 3: Rolling duality defect (early-warning signal)
# ─────────────────────────────────────────────────────────────────────────────

def run_rolling_defect(tickers, window_days=60, n_windows=8):
    from prism.unsupervised import unsupervised_prism

    today = date.today()
    # 6 windows × 60 trading days ≈ 360 trading days ≈ 500 calendar days
    lookback = window_days * n_windows * 2 + 60
    start_all = today - timedelta(days=lookback)

    print("\n" + "=" * 65)
    print("Part 3: Rolling Duality Defect — Structural Health Over Time")
    print("=" * 65)

    data_all, avail = download_prices(tickers, start_all.isoformat(), today.isoformat())
    if len(avail) < 10 or len(data_all) < window_days * 2:
        print("  Insufficient data for rolling analysis.")
        return

    returns_all = data_all.pct_change().dropna()
    T = len(returns_all)
    step = max(T // n_windows, window_days)

    print(f"  Window: {window_days} trading days, step: {step} days")
    print(f"  {'Window end':<14} {'Mean corr':>10} {'Defect':>8} {'Signal':>20}")
    print("  " + "-" * 58)

    defects = []
    dates_out = []

    for i in range(n_windows):
        end_idx = min((i + 1) * step + window_days, T)
        start_idx = end_idx - window_days
        if start_idx < 0:
            continue
        window_returns = returns_all.iloc[start_idx:end_idx]
        if len(window_returns) < 20:
            continue

        corr_w = window_returns.corr().values
        A_w = corr_to_adjacency(corr_w)
        L_w = laplacian(A_w)

        res_w = unsupervised_prism(A_w, n_outer=15, verbose=False)
        defect_w = duality_defect(L_w, res_w.P_learned)
        mc_w = mean_offdiag(corr_w)

        window_end_date = returns_all.index[end_idx - 1].date()
        defects.append(defect_w)
        dates_out.append(window_end_date)

        if len(defects) >= 2:
            trend = defects[-1] - defects[-2]
            signal = ("RISING  +" if trend > 0.03 else
                      "FALLING -" if trend < -0.03 else
                      "stable   ")
        else:
            signal = "baseline "

        print(f"  {str(window_end_date):<14} {mc_w:>10.3f} {defect_w:>8.4f}  {signal}")

    if len(defects) >= 3:
        slope = np.polyfit(range(len(defects)), defects, 1)[0]
        print(f"\n  Trend slope: {slope:+.4f}/window")
        if slope > 0.02:
            print("  WARNING: Duality defect is rising — structural stress accumulating.")
        elif slope < -0.02:
            print("  Market structure is stabilizing.")
        else:
            print("  Market structure is stable.")


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def run_demo():
    print("=" * 65)
    print("Prism Financial Demo: S&P 500 Risk Community Detection")
    print("=" * 65)
    print(f"Stocks: {N} ({len(SECTOR_NAMES)} sectors x 5 stocks each)")

    try:
        run_historical(TICKERS, SECTOR_LABELS, GROUND_TRUTH)
    except Exception as e:
        print(f"  Historical demo failed: {e}")

    try:
        run_today_forecast(TICKERS, SECTOR_LABELS)
    except Exception as e:
        print(f"  Today's forecast failed: {e}")

    try:
        run_rolling_defect(TICKERS, window_days=60, n_windows=6)
    except Exception as e:
        print(f"  Rolling defect failed: {e}")


if __name__ == "__main__":
    run_demo()
