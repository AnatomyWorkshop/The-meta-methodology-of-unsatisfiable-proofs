"""
Prism Compression Signal Detection — v2

Revised approach:
- Work directly on daily defect series (not subsampled)
- Compression = defect drops from a sustained high plateau to a lower level
  within ~21 trading days, while correlation stays calm
- "Sustained high" = defect above 80th percentile for at least 40 of the
  prior 60 trading days (not just a single spike)
- Release = realized vol doubles OR correlation jumps >0.20 within 60 days
  (tighter than v1's 0.15 threshold)
- Control = sustained high-defect periods that do NOT compress
- De-duplicate: only count one compression event per 40-day window
"""

import numpy as np
import pandas as pd
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
    ("2018 Vol Shock",     "2018-02-05"),
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


def compute_daily_metrics(returns, window=60):
    """Compute defect and correlation for every trading day (rolling window)."""
    n_days = len(returns)
    defects = np.full(n_days, np.nan)
    corrs = np.full(n_days, np.nan)
    vols = np.full(n_days, np.nan)

    print(f"  Computing daily metrics (window={window})...")
    for i in range(window, n_days):
        w = returns.iloc[i-window:i]
        corr_mat = w.corr().values
        A = np.maximum(corr_mat - 0.2, 0)
        np.fill_diagonal(A, 0)
        L = laplacian(A)
        P = fiedler_P(L)
        defects[i] = duality_defect(L, P)
        corrs[i] = mean_offdiag(corr_mat)
        vols[i] = w.std(axis=0).mean()

        if i % 200 == 0:
            print(f"    day {i}/{n_days}...")

    print(f"  Done. {np.sum(~np.isnan(defects))} valid observations.")
    return defects, corrs, vols


def find_compression_events(defects, corrs, dates,
                            lookback=252, plateau_days=60, plateau_frac=0.67,
                            drop_window=21, drop_threshold=0.25,
                            corr_max_rise=0.12, min_gap=40):
    """
    Find compression events in daily defect series.

    Compression = defect drops >drop_threshold from its recent peak,
    within drop_window days, from a sustained high-pressure regime,
    while correlation stays calm.

    Sustained high = defect above 80th percentile for at least
    plateau_frac of the prior plateau_days.
    """
    n = len(defects)
    events = []
    last_event_idx = -min_gap

    for i in range(lookback + drop_window, n):
        if np.isnan(defects[i]):
            continue

        # Rolling 80th percentile over prior lookback days
        prior = defects[max(0, i-lookback):i]
        prior = prior[~np.isnan(prior)]
        if len(prior) < 60:
            continue
        p80 = np.percentile(prior, 80)

        # Check sustained high plateau: was defect above p80 for most of
        # the prior plateau_days?
        plateau_window = defects[max(0, i-drop_window-plateau_days):i-drop_window]
        plateau_window = plateau_window[~np.isnan(plateau_window)]
        if len(plateau_window) < 20:
            continue
        days_above = np.sum(plateau_window >= p80)
        if days_above < len(plateau_window) * plateau_frac:
            continue

        # Peak defect in the plateau window
        peak_defect = np.max(plateau_window)

        # Current defect
        current_defect = defects[i]

        # Check drop
        drop_pct = (peak_defect - current_defect) / peak_defect
        if drop_pct < drop_threshold:
            continue

        # Check correlation hasn't spiked
        if np.isnan(corrs[i]) or np.isnan(corrs[max(0, i-drop_window)]):
            continue
        corr_rise = corrs[i] - corrs[i - drop_window]
        if corr_rise >= corr_max_rise:
            continue

        # De-duplicate: skip if too close to last event
        if i - last_event_idx < min_gap:
            continue

        events.append({
            'idx': i,
            'date': dates[i],
            'peak_defect': peak_defect,
            'current_defect': current_defect,
            'drop_pct': drop_pct,
            'corr_before': corrs[i - drop_window],
            'corr_now': corrs[i],
            'p80': p80,
        })
        last_event_idx = i

    return events


def check_release_v2(defects, corrs, vols, start_idx, horizon=60,
                     corr_spike=0.20, vol_spike_mult=1.8):
    """
    Check if stress release occurs within horizon days.
    Release = correlation jumps >corr_spike from pre-compression baseline
    OR volatility nearly doubles.
    """
    n = len(defects)
    # Baseline: average corr and vol in the 30 days before compression
    base_start = max(0, start_idx - 30)
    base_corrs = corrs[base_start:start_idx]
    base_vols = vols[base_start:start_idx]
    base_corrs = base_corrs[~np.isnan(base_corrs)]
    base_vols = base_vols[~np.isnan(base_vols)]

    if len(base_corrs) < 10:
        return False, None, 0.0

    baseline_corr = np.mean(base_corrs)
    baseline_vol = np.mean(base_vols)

    best_lead = None
    peak_corr_rise = 0.0

    for j in range(1, min(horizon + 1, n - start_idx)):
        idx = start_idx + j
        if np.isnan(corrs[idx]) or np.isnan(vols[idx]):
            continue
        rise = corrs[idx] - baseline_corr
        if rise > peak_corr_rise:
            peak_corr_rise = rise
        if rise >= corr_spike or vols[idx] >= baseline_vol * vol_spike_mult:
            if best_lead is None:
                best_lead = j

    return best_lead is not None, best_lead, peak_corr_rise


def run_analysis():
    data, avail = download_all(TICKERS, "2009-01-01", "2021-06-30")
    returns = data.pct_change().dropna()
    dates = returns.index

    print()
    print("=" * 72)
    print("Prism Compression Signal Detection v2")
    print("=" * 72)
    print(f"Tickers: {len(avail)}, Trading days: {len(returns)}")
    print()

    defects, corrs, vols = compute_daily_metrics(returns, window=60)

    # ── Find compression events ───────────────────────────────────────────
    events = find_compression_events(defects, corrs, dates)
    print(f"\nCompression events detected: {len(events)}")

    # ── Check each event for subsequent release ───────────────────────────
    print()
    print(f"  {'Date':<12} {'Peak d':>7} {'Now d':>7} {'Drop':>5} "
          f"{'Corr bef':>8} {'Corr now':>8}  {'Release':>8} {'Lead':>6}  Notes")
    print(f"  {'-'*82}")

    event_dates_known = {pd.Timestamp(d): n for n, d in KNOWN_STRESS_EVENTS}
    released_count = 0
    lead_times = []

    for ev in events:
        released, lead, peak_rise = check_release_v2(
            defects, corrs, vols, ev['idx'])
        if released:
            released_count += 1
            lead_times.append(lead)

        # Proximity to known events
        note = ""
        for ed, en in event_dates_known.items():
            diff = (ed - ev['date']).days
            if 0 <= diff <= 60:
                note = f"-> {en} ({diff}d)"
                break

        lead_str = f"{lead}d" if lead else "no"
        print(f"  {str(ev['date'].date()):<12} {ev['peak_defect']:>7.3f} "
              f"{ev['current_defect']:>7.3f} {ev['drop_pct']:>4.0%} "
              f"{ev['corr_before']:>8.3f} {ev['corr_now']:>8.3f}  "
              f"{'YES' if released else 'no':>8} {lead_str:>6}  {note}")

    # ── Control group ─────────────────────────────────────────────────────
    # High-defect days (above global 80th pct) that are NOT near any
    # compression event, sampled every 40 days to avoid overlap
    p80_global = np.nanpercentile(defects, 80)
    compression_indices = {ev['idx'] for ev in events}

    control_released = 0
    control_total = 0
    last_control = -40

    for i in range(252, len(defects)):
        if np.isnan(defects[i]):
            continue
        if defects[i] < p80_global:
            continue
        # Not near any compression event
        if any(abs(i - ci) < 40 for ci in compression_indices):
            continue
        if i - last_control < 40:
            continue

        released, _, _ = check_release_v2(defects, corrs, vols, i)
        control_total += 1
        if released:
            control_released += 1
        last_control = i

    # ── Summary ───────────────────────────────────────────────────────────
    n = len(events)
    print()
    print("=" * 72)
    print("Summary")
    print("=" * 72)
    print(f"  Compression events:          {n}")
    if n > 0:
        print(f"  Followed by release:         {released_count} / {n} "
              f"({released_count/n:.0%})")
    if lead_times:
        print(f"  Median lead time:            {int(np.median(lead_times))} trading days")
        print(f"  Mean lead time:              {np.mean(lead_times):.1f} trading days")
        print(f"  Range:                       {min(lead_times)}-{max(lead_times)} days")

    print()
    print(f"  Control (high-defect, no compression, sampled every 40d):")
    if control_total > 0:
        print(f"  Followed by release:         {control_released} / {control_total} "
              f"({control_released/control_total:.0%})")

    if n > 0 and control_total > 0:
        signal_rate = released_count / n
        control_rate = control_released / control_total
        lift = signal_rate / control_rate if control_rate > 0 else float('inf')
        print()
        print(f"  Signal precision:            {signal_rate:.0%}")
        print(f"  Control baseline:            {control_rate:.0%}")
        print(f"  Lift:                        {lift:.2f}x")
        print()
        if lift > 1.5:
            print("  >> Compression signal has predictive value over baseline.")
        elif lift > 1.2:
            print("  >> Moderate signal. Worth monitoring but not standalone.")
        else:
            print("  >> Weak or no signal above baseline high-defect condition.")

    # ── Known events coverage ─────────────────────────────────────────────
    print()
    print("  Known stress events and nearest compression signal:")
    for name, date_str in KNOWN_STRESS_EVENTS:
        event_ts = pd.Timestamp(date_str)
        best = None
        best_lead = None
        for ev in events:
            diff = (event_ts - ev['date']).days
            if 0 < diff <= 90:
                if best_lead is None or diff < best_lead:
                    best = ev
                    best_lead = diff
        if best:
            print(f"    {name:<25} compression {best_lead}d before "
                  f"(d: {best['peak_defect']:.3f} -> {best['current_defect']:.3f})")
        else:
            print(f"    {name:<25} no compression signal in prior 90d")


if __name__ == "__main__":
    run_analysis()
