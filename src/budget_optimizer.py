"""Part 03 - Member 2: fixed-budget optimisation of monthly advertising allocation.

The objective is the trained MMM's PREDICTED sales revenue for one month. It is a model
prediction under stated assumptions, not a causal ROI measurement.

Assumptions (taken from the saved model bundle, i.e. the December 2025 snapshot):
  * external factors (price, promo, season ...) are held fixed
  * previous-month adstock state is held fixed
"""
from __future__ import annotations
from pathlib import Path
import sys

import numpy as np
import pandas as pd
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:          # predict_sales imports `src.saturation`
    sys.path.insert(0, str(ROOT))

from src.predict_sales import (SPEND_CHANNELS, ADSTOCK_CHANNELS,  # noqa: E402
                               load_model, predict_budget_allocation)

SCALE = 1_000_000  # optimise in LKR millions: SLSQP behaves badly with values ~1e6


# ------------------------------------------------------------------ inputs
def load_inputs():
    """Return model bundle, historical data, scenario assumptions."""
    bundle = load_model()
    hist = pd.read_csv(ROOT / 'data/processed/cleaned_data.csv')
    controls = dict(bundle['external_factors_reference'])
    prev_adstock = dict(bundle['previous_adstock_reference'])
    return bundle, hist, controls, prev_adstock


def spending_limits(hist: pd.DataFrame, lower_pct=0.0, upper_pct=0.0):
    """Realistic limits = observed historical min / max per channel (avoids extrapolation)."""
    lo = hist[list(SPEND_CHANNELS)].min() * (1 - lower_pct)
    hi = hist[list(SPEND_CHANNELS)].max() * (1 + upper_pct)
    return lo, hi


def reference_allocation(hist: pd.DataFrame) -> pd.Series:
    """Reference/current allocation = historical average monthly spend per channel."""
    return hist[list(SPEND_CHANNELS)].mean()


# ------------------------------------------------------------------ prediction
def predicted_sales(allocation, controls, prev_adstock) -> float:
    """Wrapper around the project's predict_budget_allocation()."""
    alloc = {c: float(allocation[c]) for c in SPEND_CHANNELS}
    return predict_budget_allocation(alloc, controls, prev_adstock)


# ------------------------------------------------------------------ optimiser
def optimise_budget(total_budget, lower, upper, controls, prev_adstock,
                    start=None, n_starts=8, seed=42):
    """Maximise predicted sales subject to:
         sum(spend) == total_budget      (equality constraint)
         lower <= spend <= upper         (bounds; lower >= 0 so no negative budgets)
    SciPy SLSQP; the response is S-shaped (Hill), so several starting points are tried.
    """
    lo = lower[list(SPEND_CHANNELS)].to_numpy(float) / SCALE
    hi = upper[list(SPEND_CHANNELS)].to_numpy(float) / SCALE
    budget = total_budget / SCALE
    if not lo.sum() <= budget <= hi.sum():
        raise ValueError('Budget infeasible for the given channel limits')

    def objective(x):  # minimise negative sales
        alloc = dict(zip(SPEND_CHANNELS, x * SCALE))
        return -predict_budget_allocation(alloc, controls, prev_adstock) / SCALE  # sales in LKR millions

    constraints = [{'type': 'eq', 'fun': lambda x: x.sum() - budget}]
    bounds = list(zip(lo, hi))

    rng = np.random.default_rng(seed)
    starts = []
    if start is not None:
        starts.append(np.clip(np.asarray(start, float) / SCALE, lo, hi))
    while len(starts) < n_starts:      # random feasible-ish starts, rescaled to the budget
        x = rng.uniform(lo, hi)
        x = np.clip(x * budget / x.sum(), lo, hi)
        starts.append(x)

    best = None
    for x0 in starts:
        res = minimize(objective, x0, method='SLSQP', bounds=bounds,
                       constraints=constraints, options={'maxiter': 300, 'ftol': 1e-10, 'eps': 1e-4})
        feasible = abs(res.x.sum() - budget) < 1e-4 and np.all(res.x >= lo - 1e-6) \
            and np.all(res.x <= hi + 1e-6)
        if feasible and (best is None or res.fun < best.fun):
            best = res
    if best is None:
        raise RuntimeError('SLSQP found no feasible solution')
    return pd.Series(best.x * SCALE, index=SPEND_CHANNELS), -best.fun * SCALE, best


# ------------------------------------------------------------------ comparison
def compare(reference: pd.Series, optimised: pd.Series, lower, upper, controls, prev_adstock):
    """Allocation table + prediction table for reference vs optimised budgets."""
    alloc_tbl = pd.DataFrame({
        'channel': SPEND_CHANNELS,
        'min_limit_lkr': lower[list(SPEND_CHANNELS)].values,
        'max_limit_lkr': upper[list(SPEND_CHANNELS)].values,
        'reference_budget_lkr': reference[list(SPEND_CHANNELS)].values,
        'optimized_budget_lkr': optimised[list(SPEND_CHANNELS)].values,
    })
    alloc_tbl['change_lkr'] = alloc_tbl.optimized_budget_lkr - alloc_tbl.reference_budget_lkr
    alloc_tbl['change_pct'] = 100 * alloc_tbl.change_lkr / alloc_tbl.reference_budget_lkr
    alloc_tbl['optimized_share_pct'] = 100 * alloc_tbl.optimized_budget_lkr / alloc_tbl.optimized_budget_lkr.sum()

    ref_sales = predicted_sales(reference, controls, prev_adstock)
    opt_sales = predicted_sales(optimised, controls, prev_adstock)
    pred_tbl = pd.DataFrame([{
        'total_budget_lkr': float(reference.sum()),
        'reference_predicted_sales_lkr': ref_sales,
        'optimized_predicted_sales_lkr': opt_sales,
        'sales_difference_lkr': opt_sales - ref_sales,
        'improvement_pct': 100 * (opt_sales - ref_sales) / ref_sales,
    }])
    return alloc_tbl, pred_tbl


def run_scenarios(reference, lower, upper, controls, prev_adstock,
                  multipliers=(0.8, 0.9, 1.0, 1.1, 1.2)):
    """Re-optimise for several total budgets; reference = reference mix scaled to that budget."""
    rows = []
    for m in multipliers:
        budget = float(reference.sum()) * m
        ref_scaled = reference * m
        opt, opt_sales, _ = optimise_budget(budget, lower, upper, controls, prev_adstock,
                                            start=ref_scaled.values)
        ref_sales = predicted_sales(ref_scaled, controls, prev_adstock)
        row = {'budget_multiplier': m, 'total_budget_lkr': budget,
               'reference_predicted_sales_lkr': ref_sales,
               'optimized_predicted_sales_lkr': opt_sales,
               'sales_difference_lkr': opt_sales - ref_sales,
               'improvement_pct': 100 * (opt_sales - ref_sales) / ref_sales}
        row.update({f'opt_{c}': opt[c] for c in SPEND_CHANNELS})
        rows.append(row)
    return pd.DataFrame(rows)


if __name__ == '__main__':
    bundle, hist, controls, prev = load_inputs()
    ref = reference_allocation(hist)
    lo, hi = spending_limits(hist)
    opt, sales, res = optimise_budget(ref.sum(), lo, hi, controls, prev, start=ref.values)
    a, p = compare(ref, opt, lo, hi, controls, prev)
    print(a.round(0).to_string(index=False)); print(p.round(2).to_string(index=False))
