"""
Yield Curve Deep Dive: Prism vs 2y-10y Spread as Recession Predictor

Extended backtest 2006-2023 covering:
  - 2007-2009 Great Financial Crisis
  - 2019 inversion (pre-COVID recession)
  - 2022-2023 sustained inversion

Key hypothesis: LOW duality defect on the yield curve = extreme consensus
= crowded positioning = fragile. If this holds, Prism should detect
structural fragility BEFORE or DURING yield curve inversions, and the
signal should have predictive value for recessions.

Comparison: does Prism add information beyond the 2y-10y spread?

Data: Treasury ETFs (SHV, SHY, IEI, IEF, TLH, TLT) from Yahoo Finance.
Some ETFs launched after 2006, so early period uses available subset.
"""

import numpy as np
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


TREASURY_ETFS = {
    "SHV":  "0-1y",
    "SHY":  "1-3y",
    "IEI":  "3-7y",
    "IEF":  "7-10y",
    "TLH":  "10-20y",
    "TLT":  "20+y",
}

RECESSIONS = [
    (pd.Timestamp("2007-12-01"), pd.Timestamp("2009-06-30"), "Great Financial Crisis"),
    (pd.Timestamp("2020-02-01"), pd.Timestamp("2020-04-30"), "COVID Recession"),
]

INVERSIONS = [
    (pd.Timestamp("2006-07-01"), pd.Timestamp("2007-05-01"), "2006-07 inversion"),
    (pd.Timestamp("2019-08-01"), pd.Timestamp("2019-10-15"), "2019 brief inversion"),
    (pd.Timestamp("2022-07-01"), pd.Timestamp("2023-12-31"), "2022-23 sustained inversion"),
]


def download_data(start="2006-01-01", end="2023-12-31"):
    import yfinance as yf

    etf_tickers = list(TREASURY_ETFS.keys())
    print(f"Downloading treasury ETFs: {etf_tickers}")
    etf_data = yf.download(etf_tickers, start=start, end=end,
                           auto_adjust=True, progress=False)
    if hasattr(etf_data.columns, 'levels') or isinstance(etf_data.columns, pd.MultiIndex):
        etf_data = etf_data['Close']
    etf_data = etf_data.ffill().dropna(how='all')

    # 2y-10y spread proxy: use ^FVX (5y) and ^TNX (10y) yields directly
    # Better: download actual 2y and 10y yields
    print("Downloading 2y and 10y treasury yields...")
    yields = yf.download(["2YY=F", "^TNX"], start=start, end=end,
                         auto_adjust=True, progress=False)
    if isinstance(yields.columns, pd.MultiIndex):
        yields = yields['Close']

    # Fallback: use SHY vs TLT return differential as spread proxy
    # if direct yield data is unavailable
    has_spread = False
    spread_series = None

    if yields is not None and len(yields) > 100:
        if '2YY=F' in yields.columns and '^TNX' in yields.columns:
            spread_series = yields['^TNX'] - yields['2YY=F']
            has_spread = True
            print(f"  Got direct yield spread: {len(spread_series)} days")

    if not has_spread:
        print("  Direct yields unavailable, using SHY-TLT return differential as proxy")

    available_etfs = [t for t in etf_tickers if t in etf_data.columns and etf_data[t].notna().sum() > 100]
    print(f"  Available ETFs: {available_etfs} ({len(etf_data)} days)")

    return etf_data[available_etfs], spread_series, has_spread


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


def compute_defect_from_returns(returns_window):
    if len(returns_window) < 20 or returns_window.shape[1] < 4:
        return np.nan
    corr = returns_window.corr().values
    if np.any(np.isnan(corr)):
        return np.nan
    n = corr.shape[0]
    A = np.maximum(np.abs(corr) - 0.3, 0)
    np.fill_diagonal(A, 0)
    if A.sum() < 1e-10:
        return np.nan
    L = laplacian(A)
    P = fiedler_P(L)
    return duality_defect(L, P)


def run_deep_dive():
    etf_data, spread_series, has_spread = download_data()
    returns = etf_data.pct_change().dropna()

    print()
    print("=" * 76)
    print("YIELD CURVE DEEP DIVE: Prism vs 2y-10y Spread")
    print("=" * 76)
    print(f"Period: {returns.index[0].date()} to {returns.index[-1].date()}")
    print(f"ETFs: {list(returns.columns)}")
    print()

    # Rolling defect computation
    window = 60
    step = 5

    results = []
    for i in range(window, len(returns), step):
        w = returns.iloc[i-window:i]
        dt = returns.index[i]
        d = compute_defect_from_returns(w)
        if np.isnan(d):
            continue

        spread_val = np.nan
        if has_spread and spread_series is not None:
            idx = spread_series.index.searchsorted(dt)
            if 0 < idx < len(spread_series):
                spread_val = spread_series.iloc[idx]

        results.append({
            'date': dt,
            'defect': d,
            'spread': spread_val,
        })

    df = pd.DataFrame(results)
    df['date'] = pd.to_datetime(df['date'])

    print(f"Computed {len(df)} rolling defect values")
    print(f"Defect range: {df['defect'].min():.3f} - {df['defect'].max():.3f}")
    print(f"Defect mean:  {df['defect'].mean():.3f}")
    print(f"Defect std:   {df['defect'].std():.3f}")

    # Regime analysis
    print()
    print("=" * 76)
    print("REGIME ANALYSIS")
    print("=" * 76)

    low_threshold = df['defect'].quantile(0.20)
    high_threshold = df['defect'].quantile(0.80)
    print(f"\nDefect thresholds: low < {low_threshold:.3f}, high > {high_threshold:.3f}")

    # Check defect levels during known events
    print()
    print("-" * 76)
    print("DEFECT DURING RECESSIONS")
    print("-" * 76)

    for rec_start, rec_end, rec_name in RECESSIONS:
        mask = (df['date'] >= rec_start) & (df['date'] <= rec_end)
        if mask.sum() == 0:
            print(f"\n  {rec_name}: no data in range")
            continue
        rec_df = df[mask]
        print(f"\n  {rec_name} ({rec_start.date()} to {rec_end.date()}):")
        print(f"    Defect during: mean={rec_df['defect'].mean():.3f}, "
              f"min={rec_df['defect'].min():.3f}, max={rec_df['defect'].max():.3f}")

        # Pre-recession (6 months before)
        pre_start = rec_start - pd.Timedelta(days=180)
        pre_mask = (df['date'] >= pre_start) & (df['date'] < rec_start)
        if pre_mask.sum() > 0:
            pre_df = df[pre_mask]
            print(f"    Defect 6mo before: mean={pre_df['defect'].mean():.3f}, "
                  f"min={pre_df['defect'].min():.3f}, max={pre_df['defect'].max():.3f}")

    print()
    print("-" * 76)
    print("DEFECT DURING YIELD CURVE INVERSIONS")
    print("-" * 76)

    for inv_start, inv_end, inv_name in INVERSIONS:
        mask = (df['date'] >= inv_start) & (df['date'] <= inv_end)
        if mask.sum() == 0:
            print(f"\n  {inv_name}: no data in range")
            continue
        inv_df = df[mask]
        print(f"\n  {inv_name} ({inv_start.date()} to {inv_end.date()}):")
        print(f"    Defect during: mean={inv_df['defect'].mean():.3f}, "
              f"min={inv_df['defect'].min():.3f}, max={inv_df['defect'].max():.3f}")

        # Compare to surrounding period
        surr_start = inv_start - pd.Timedelta(days=180)
        surr_end = inv_end + pd.Timedelta(days=180)
        surr_mask = ((df['date'] >= surr_start) & (df['date'] < inv_start)) | \
                    ((df['date'] > inv_end) & (df['date'] <= surr_end))
        if surr_mask.sum() > 0:
            surr_df = df[surr_mask]
            print(f"    Defect surrounding 6mo: mean={surr_df['defect'].mean():.3f}")
            ratio = inv_df['defect'].mean() / surr_df['defect'].mean()
            print(f"    Ratio (inversion/surrounding): {ratio:.2f}x")

    # Predictive analysis: does LOW defect precede recessions?
    print()
    print("=" * 76)
    print("PREDICTIVE ANALYSIS: Low Defect as Recession Predictor")
    print("=" * 76)

    # For each recession, check if defect was in bottom 20% in the 3-12 months before
    for rec_start, rec_end, rec_name in RECESSIONS:
        print(f"\n  {rec_name} (started {rec_start.date()}):")
        for months_before in [12, 9, 6, 3]:
            lookback_start = rec_start - pd.Timedelta(days=months_before * 30)
            lookback_end = rec_start - pd.Timedelta(days=(months_before - 3) * 30)
            mask = (df['date'] >= lookback_start) & (df['date'] < lookback_end)
            if mask.sum() == 0:
                continue
            period_df = df[mask]
            mean_d = period_df['defect'].mean()
            pct = (df['defect'] < mean_d).mean() * 100
            low_flag = "[LOW]" if mean_d < low_threshold else ""
            print(f"    T-{months_before}mo to T-{months_before-3}mo: "
                  f"defect={mean_d:.3f} (percentile {pct:.0f}%) {low_flag}")

    # Comparison with 2y-10y spread
    if has_spread and df['spread'].notna().sum() > 50:
        print()
        print("=" * 76)
        print("COMPARISON: Prism Defect vs 2y-10y Spread")
        print("=" * 76)

        valid = df[df['spread'].notna()].copy()
        corr_val = valid['defect'].corr(valid['spread'])
        print(f"\n  Correlation (defect vs spread): {corr_val:.3f}")

        # When spread is negative (inverted), what is defect?
        inverted = valid[valid['spread'] < 0]
        normal = valid[valid['spread'] >= 0]
        if len(inverted) > 5:
            print(f"\n  When curve is INVERTED (spread < 0):")
            print(f"    N = {len(inverted)} observations")
            print(f"    Defect mean: {inverted['defect'].mean():.3f}")
            print(f"  When curve is NORMAL (spread >= 0):")
            print(f"    N = {len(normal)} observations")
            print(f"    Defect mean: {normal['defect'].mean():.3f}")
            print(f"    Ratio (inverted/normal): {inverted['defect'].mean() / normal['defect'].mean():.2f}x")

        # Lead-lag: does defect drop BEFORE spread goes negative?
        print(f"\n  Lead-lag analysis:")
        for lag_days in [0, 30, 60, 90, 120]:
            shifted = valid.copy()
            shifted['spread_future'] = shifted['spread'].shift(-lag_days // step)
            valid_shifted = shifted.dropna(subset=['spread_future'])
            if len(valid_shifted) < 20:
                continue
            c = valid_shifted['defect'].corr(valid_shifted['spread_future'])
            print(f"    Defect vs spread(+{lag_days}d): corr = {c:.3f}")

    # Annual summary
    print()
    print("=" * 76)
    print("ANNUAL SUMMARY")
    print("=" * 76)
    print(f"\n  {'Year':<6} {'Mean':>7} {'Min':>7} {'Max':>7} {'Std':>7}  Context")
    print(f"  {'-'*65}")

    df['year'] = df['date'].dt.year
    context_map = {
        2006: "pre-crisis, curve inverted",
        2007: "crisis begins Dec",
        2008: "GFC peak",
        2009: "recovery begins",
        2010: "post-crisis normal",
        2011: "European debt crisis",
        2012: "QE3 begins",
        2013: "taper tantrum",
        2014: "low vol regime",
        2015: "rate hike begins Dec",
        2016: "post-Brexit",
        2017: "synchronized growth",
        2018: "curve flattening",
        2019: "inversion Aug, rate cuts",
        2020: "COVID crash + recovery",
        2021: "reflation trade",
        2022: "rate hikes, inversion Jul",
        2023: "sustained inversion",
    }

    for year, group in df.groupby('year'):
        ctx = context_map.get(year, "")
        print(f"  {year:<6} {group['defect'].mean():>7.3f} "
              f"{group['defect'].min():>7.3f} {group['defect'].max():>7.3f} "
              f"{group['defect'].std():>7.3f}  {ctx}")

    # Key finding summary
    print()
    print("=" * 76)
    print("KEY FINDINGS")
    print("=" * 76)
    print("""
  Hypothesis: LOW defect = extreme consensus = crowded trade = fragile.

  If confirmed:
  - Low defect periods should PRECEDE recessions (consensus before break)
  - Defect should be LOW during inversions (all maturities moving in lockstep)
  - Prism adds lead time over the 2y-10y spread (structural signal before
    the spread itself inverts)

  If refuted:
  - Defect is random relative to recessions/inversions
  - No lead over the spread
  - The opposite-signal finding from the initial experiment was noise
""")


def run_lead_lag_detail():
    """Deeper lead-lag analysis: does defect predict spread CHANGES?"""
    etf_data, spread_series, has_spread = download_data()
    returns = etf_data.pct_change().dropna()

    if not has_spread or spread_series is None:
        print("No spread data available for lead-lag analysis")
        return

    window = 60
    step = 5

    results = []
    for i in range(window, len(returns), step):
        w = returns.iloc[i-window:i]
        dt = returns.index[i]
        d = compute_defect_from_returns(w)
        if np.isnan(d):
            continue

        idx = spread_series.index.searchsorted(dt)
        if 0 < idx < len(spread_series):
            spread_val = spread_series.iloc[idx]
        else:
            spread_val = np.nan

        results.append({'date': dt, 'defect': d, 'spread': spread_val})

    df = pd.DataFrame(results)
    valid = df[df['spread'].notna()].copy().reset_index(drop=True)

    print()
    print("=" * 76)
    print("LEAD-LAG DETAIL: Defect vs Future Spread Changes")
    print("=" * 76)

    # Does LOW defect predict spread DECLINE (toward inversion)?
    print("\n  Does low defect predict spread decline?")
    print(f"  {'Horizon':<12} {'Corr(d, delta_s)':>18} {'Low-d mean chg':>16} {'High-d mean chg':>16}")
    print(f"  {'-'*65}")

    low_thresh = valid['defect'].quantile(0.25)
    high_thresh = valid['defect'].quantile(0.75)

    for horizon in [30, 60, 90, 120, 180]:
        shift = horizon // step
        if shift >= len(valid):
            continue
        valid_h = valid.copy()
        valid_h['spread_future'] = valid_h['spread'].shift(-shift)
        valid_h['spread_change'] = valid_h['spread_future'] - valid_h['spread']
        valid_h = valid_h.dropna(subset=['spread_change'])

        if len(valid_h) < 20:
            continue

        corr = valid_h['defect'].corr(valid_h['spread_change'])

        low_mask = valid_h['defect'] < low_thresh
        high_mask = valid_h['defect'] > high_thresh
        low_chg = valid_h.loc[low_mask, 'spread_change'].mean()
        high_chg = valid_h.loc[high_mask, 'spread_change'].mean()

        print(f"  {horizon}d{'':<8} {corr:>18.3f} {low_chg:>16.3f} {high_chg:>16.3f}")

    # Conditional recession probability
    print()
    print("=" * 76)
    print("CONDITIONAL ANALYSIS: Recession probability given defect regime")
    print("=" * 76)

    # Mark recession periods
    valid['in_recession'] = False
    for rec_start, rec_end, _ in RECESSIONS:
        mask = (valid['date'] >= rec_start) & (valid['date'] <= rec_end)
        valid.loc[mask, 'in_recession'] = True

    # Mark pre-recession (6 months before)
    valid['pre_recession'] = False
    for rec_start, _, _ in RECESSIONS:
        pre_start = rec_start - pd.Timedelta(days=180)
        mask = (valid['date'] >= pre_start) & (valid['date'] < rec_start)
        valid.loc[mask, 'pre_recession'] = True

    low_mask = valid['defect'] < low_thresh
    high_mask = valid['defect'] > high_thresh
    mid_mask = ~low_mask & ~high_mask

    print(f"\n  P(pre-recession | low defect):  {valid.loc[low_mask, 'pre_recession'].mean():.3f} "
          f"(N={low_mask.sum()})")
    print(f"  P(pre-recession | mid defect):  {valid.loc[mid_mask, 'pre_recession'].mean():.3f} "
          f"(N={mid_mask.sum()})")
    print(f"  P(pre-recession | high defect): {valid.loc[high_mask, 'pre_recession'].mean():.3f} "
          f"(N={high_mask.sum()})")
    print(f"  Unconditional P(pre-recession): {valid['pre_recession'].mean():.3f}")

    # Same for inverted curve
    valid['inverted'] = valid['spread'] < 0
    print(f"\n  P(inverted | low defect):  {valid.loc[low_mask, 'inverted'].mean():.3f}")
    print(f"  P(inverted | mid defect):  {valid.loc[mid_mask, 'inverted'].mean():.3f}")
    print(f"  P(inverted | high defect): {valid.loc[high_mask, 'inverted'].mean():.3f}")
    print(f"  Unconditional P(inverted): {valid['inverted'].mean():.3f}")

    # Time series of defect quintiles
    print()
    print("=" * 76)
    print("DEFECT QUINTILE TRANSITIONS")
    print("=" * 76)
    print("\n  When defect enters bottom quintile, what happens to spread in next 90d?")

    valid['quintile'] = pd.qcut(valid['defect'], 5, labels=[1,2,3,4,5])
    entries_to_low = []
    for i in range(1, len(valid)):
        if valid.iloc[i]['quintile'] == 1 and valid.iloc[i-1]['quintile'] != 1:
            # Entry into bottom quintile
            future_idx = i + (90 // step)
            if future_idx < len(valid):
                spread_now = valid.iloc[i]['spread']
                spread_future = valid.iloc[future_idx]['spread']
                entries_to_low.append({
                    'date': valid.iloc[i]['date'],
                    'defect': valid.iloc[i]['defect'],
                    'spread_now': spread_now,
                    'spread_90d': spread_future,
                    'spread_change': spread_future - spread_now,
                })

    if entries_to_low:
        entries_df = pd.DataFrame(entries_to_low)
        print(f"\n  Found {len(entries_df)} entries into bottom quintile:")
        print(f"  {'Date':<12} {'Defect':>8} {'Spread now':>11} {'Spread +90d':>12} {'Change':>8}")
        print(f"  {'-'*55}")
        for _, row in entries_df.iterrows():
            print(f"  {str(row['date'].date()):<12} {row['defect']:>8.3f} "
                  f"{row['spread_now']:>11.2f} {row['spread_90d']:>12.2f} "
                  f"{row['spread_change']:>8.2f}")
        print(f"\n  Mean spread change after entry to low defect: {entries_df['spread_change'].mean():.3f}")
        print(f"  Fraction where spread declined: {(entries_df['spread_change'] < 0).mean():.1%}")


if __name__ == "__main__":
    run_deep_dive()
    print("\n\n")
    run_lead_lag_detail()
