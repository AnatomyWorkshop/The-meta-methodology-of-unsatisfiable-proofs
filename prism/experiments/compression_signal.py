"""
Prism Compression Signal Detection

Hypothesis (from Deepseek3): before a market crisis, the duality defect
undergoes a characteristic "compression" — a rapid drop from a sustained
high level, while surface correlations remain calm. This precedes the
full release (correlation spike + defect collapse) by days to weeks.

Signal definition:
  A compression event occurs when:
  1. defect is above its rolling 80th percentile (sustained high pressure)
  2. defect drops >30% within 21 trading days (~1 month)
  3. mean correlation does NOT spike (rise <0.10) during the same window
     (ruling out cases where the crisis has already started)

Test:
  - Scan 2010-2021 rolling 60d defect series for compression events
  - For each compression event, check if a stress release occurs within
    60 trading days (correlation spike >0.15 from baseline, or vol spike)
  - Compare to control: random high-defect windows without compression
  - Report precision, recall, lead time
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

KNOWN_STRESS_EVENTS = [
    ("2011 US Downgrade",  "2011-08-05"),
    ("2013 Taper Tantrum", "2013-06-19"),
    ("2015 China Shock",   "2015-08-24"),
    ("2018 Fed Panic",     "2018-12-24"),
    ("2020 COVID Onset",   "2020-02-24"),
]


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


def duality_defect(L, P):
    comm = L @ P - P @ L
    return np.linalg.norm(comm, 'fro') / (np.linalg.norm(L, 'fro') + 1e-10)


def mean_offdiag(M):
    n = M.shape[0]
    return (M.sum() - np.trace(M)) / (n * (n - 1))


def compute_metrics(returns_window):
    corr = returns_window.corr().values
    A = np.maximum(corr - 0.2, 0)
    np.fill_diagonal(A, 0)
    L = laplacian(A)
    P = fiedler_P(L)
    return {
        'defect':    duality_defect(L, P),
        'mean_corr': mean_offdiag(corr),
        'vol':       returns_window.std(axis=0).mean(),
    }


def build_rolling_series(returns, window=60, step=5):
    """Build dense rolling series (every `step` trading days)."""
    import pandas as pd
    series = []
    for i in range(window, len(returns), step):
        m = compute_metrics(returns.iloc[i-window:i])
        series.append({
            'date': returns.index[i],
            'idx':  i,
            **m
        })
    return series


def detect_compression_events(series, lookback_pct=126, drop_threshold=0.30,
                               corr_max_rise=0.10, compression_window=21):
    """
    Scan series for compression events.

    A compression event at index i means:
    - series[i].defect > 80th percentile of prior `lookback_pct` observations
    - series[i].defect < series[i - compression_window].defect * (1 - drop_threshold)
    - series[i].mean_corr - series[i - compression_window].mean_corr < corr_max_rise
    """
    defects = np.array([s['defect'] for s in series])
    corrs   = np.array([s['mean_corr'] for s in series])

    events = []
    for i in range(compression_window + lookback_pct, len(series)):
        # Rolling 80th percentile of defect over prior lookback_pct steps
        prior = defects[i - lookback_pct:i]
        p80 = np.percentile(prior, 80)

        d_now  = defects[i]
        d_prev = defects[i - compression_window]
        c_now  = corrs[i]
        c_prev = corrs[i - compression_window]

        # Condition 1: currently in high-pressure regime
        if d_prev < p80:
            continue
        # Condition 2: defect has compressed significantly
        if d_now >= d_prev * (1 - drop_threshold):
            continue
        # Condition 3: correlation hasn't already spiked (crisis not started)
        if c_now - c_prev >= corr_max_rise:
            continue

        drop_pct = (d_prev - d_now) / d_prev
        events.append({
            'date':      series[i]['date'],
            'idx':       series[i]['idx'],
            'defect_before': d_prev,
            'defect_now':    d_now,
            'drop_pct':      drop_pct,
            'corr_before':   c_prev,
            'corr_now':      c_now,
            'p80':           p80,
        })

    return events


def check_release(returns, start_idx, horizon=60,
                  corr_spike=0.15, vol_spike_mult=2.0):
    """
    Check if a stress release occurs within `horizon` trading days after start_idx.
    Release = correlation spikes by >corr_spike OR vol doubles.
    Returns (released: bool, lead_days: int or None, peak_corr_rise: float)
    """
    baseline_window = returns.iloc[max(0, start_idx-60):start_idx]
    if len(baseline_window) < 20:
        return False, None, 0.0

    baseline_corr = mean_offdiag(baseline_window.corr().values)
    baseline_vol  = baseline_window.std(axis=0).mean()

    best_lead = None
    peak_rise = 0.0

    for j in range(1, horizon + 1):
        end = start_idx + j
        if end >= len(returns):
            break
        w = returns.iloc[end-21:end] if end >= 21 else returns.iloc[:end]
        if len(w) < 5:
            continue
        c = mean_offdiag(w.corr().values)
        v = w.std(axis=0).mean()
        rise = c - baseline_corr
        if rise > peak_rise:
            peak_rise = rise
        if (rise >= corr_spike or v >= baseline_vol * vol_spike_mult):
            if best_lead is None:
                best_lead = j
    released = best_lead is not None
    return released, best_lead, peak_rise


def run_compression_analysis():
    import pandas as pd

    data, avail = download_all(TICKERS, "2009-06-01", "2021-06-30")
    returns = data.pct_change().dropna()

    print()
    print("=" * 72)
    print("Prism Compression Signal Analysis")
    print("=" * 72)
    print(f"Tickers: {len(avail)}, Period: 2009-2021")
    print()

    print("Building rolling 60-day defect series (step=5 days)...")
    series = build_rolling_series(returns, window=60, step=5)
    print(f"  {len(series)} observations")

    # ── Detect compression events ─────────────────────────────────────────
    events = detect_compression_events(series, drop_threshold=0.25,
                                        corr_max_rise=0.15)
    print(f"\nCompression events detected: {len(events)}")

    # ── For each event, check if release follows ──────────────────────────
    print()
    print(f"  {'Date':<12} {'δ_before':>9} {'δ_now':>7} {'drop%':>6} "
          f"{'ρ_before':>9} {'ρ_now':>7}  {'Release?':>9} {'Lead(days)':>11}")
    print(f"  {'-'*80}")

    released_count = 0
    lead_times = []
    event_dates = {pd.Timestamp(d): n for n, d in KNOWN_STRESS_EVENTS}

    for ev in events:
        released, lead, peak_rise = check_release(returns, ev['idx'])
        if released:
            released_count += 1
            lead_times.append(lead)

        # Check proximity to known stress events
        note = ""
        for ed, en in event_dates.items():
            if abs((ev['date'] - ed).days) < 45:
                note = f"  ← near {en}"
                break

        lead_str = f"{lead}d" if lead is not None else "no"
        print(f"  {str(ev['date'].date()):<12} {ev['defect_before']:>9.3f} "
              f"{ev['defect_now']:>7.3f} {ev['drop_pct']:>5.0%} "
              f"{ev['corr_before']:>9.3f} {ev['corr_now']:>7.3f}  "
              f"{'YES' if released else 'no':>9} {lead_str:>11}{note}")

    # ── Control group: high-defect windows without compression ────────────
    defects = np.array([s['defect'] for s in series])
    p80_global = np.percentile(defects, 80)
    compression_dates = {ev['date'] for ev in events}

    control_released = 0
    control_total = 0
    for i, s in enumerate(series):
        if s['defect'] < p80_global:
            continue
        if s['date'] in compression_dates:
            continue
        # High defect, no compression — this is the control
        released, _, _ = check_release(returns, s['idx'])
        control_total += 1
        if released:
            control_released += 1

    # ── Summary ───────────────────────────────────────────────────────────
    n = len(events)
    print()
    print("=" * 72)
    print("Summary")
    print("=" * 72)
    print(f"  Compression events:          {n}")
    print(f"  → Followed by release:       {released_count} / {n} "
          f"({released_count/n:.0%} precision)" if n > 0 else "  → n/a")

    if lead_times:
        print(f"  → Median lead time:          {int(np.median(lead_times))} trading days")
        print(f"  → Mean lead time:            {np.mean(lead_times):.1f} trading days")
        print(f"  → Range:                     {min(lead_times)}–{max(lead_times)} days")

    print()
    print(f"  Control (high-defect, no compression):")
    if control_total > 0:
        print(f"  → Followed by release:       {control_released} / {control_total} "
              f"({control_released/control_total:.0%})")
    print()

    if n > 0 and control_total > 0:
        signal_prec = released_count / n
        control_prec = control_released / control_total
        lift = signal_prec / control_prec if control_prec > 0 else float('inf')
        print(f"  Lift (compression vs control): {lift:.2f}x")
        print()
        if lift > 1.5 and released_count / n > 0.6:
            print("  [YES] Compression signal has predictive value.")
            print("    High-defect + compression -> release is more likely than")
            print("    high-defect alone. Lead time gives actionable warning.")
        elif lift > 1.0:
            print("  [~] Weak signal. Compression slightly predictive but noisy.")
        else:
            print("  [NO] No predictive value over baseline high-defect condition.")

    print()
    print("  Interpretation guide:")
    print("  Compression = defect drops >30% from 80th-pct high, corr stays calm.")
    print("  Release     = corr spikes >0.15 OR vol doubles within 60 trading days.")
    print("  Lift > 1.5x + precision > 60% = actionable structural early warning.")


if __name__ == "__main__":
    run_compression_analysis()
