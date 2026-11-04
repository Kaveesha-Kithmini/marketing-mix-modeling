"""Member 3: reproducible MMM inference for feature rows and raw budget scenarios.

IMPORTANT: The model predicts SALES REVENUE, not causal incremental revenue or ROI.
The optional budget interface applies one-month geometric adstock carryover.
"""
from __future__ import annotations
from pathlib import Path
from collections.abc import Mapping
import joblib
import numpy as np
import pandas as pd

SPEND_CHANNELS = (
    'tv_spend_lkr', 'facebook_instagram_spend_lkr',
    'google_search_spend_lkr', 'youtube_spend_lkr',
    'radio_spend_lkr', 'outdoor_spend_lkr',
)
ADSTOCK_CHANNELS = tuple(c.replace('_spend_lkr', '_adstock_lkr') for c in SPEND_CHANNELS)
DECAY_RATES = dict(zip(SPEND_CHANNELS, (0.6, 0.3, 0.2, 0.4, 0.4, 0.5)))
DEFAULT_BUNDLE_PATH = Path(__file__).resolve().parents[1] / 'models' / 'mmm_model.joblib'


def load_model(path=DEFAULT_BUNDLE_PATH):
    """Load the trusted project model bundle, not arbitrary untrusted joblib files."""
    bundle = joblib.load(path)
    if not isinstance(bundle, dict) or 'estimator' not in bundle or 'feature_columns' not in bundle:
        raise ValueError('Invalid MMM model bundle')
    return bundle


def _predict_bundle(bundle, frame: pd.DataFrame) -> pd.Series:
    if not isinstance(frame, pd.DataFrame) or frame.empty:
        raise ValueError('features must be a non-empty pandas DataFrame')
    variant = bundle['feature_variant']
    data = frame.copy()
    if variant == 'hill_saturated':
        from src.saturation import apply_saturation
        data = apply_saturation(data, half_saturation=bundle['saturation_midpoints'],
                                slope=bundle['saturation_slope'])
    elif variant != 'linear_adstock':
        raise ValueError(f'Unsupported feature variant: {variant}')
    columns = bundle['feature_columns']
    missing = [c for c in columns if c not in data]
    if missing:
        raise ValueError(f'Missing model features: {missing}')
    matrix = data.loc[:, columns].apply(pd.to_numeric, errors='raise')
    if not np.isfinite(matrix.to_numpy(dtype=float)).all():
        raise ValueError('Model features must be finite')
    prediction = np.asarray(bundle['estimator'].predict(matrix), dtype=float)
    if not np.isfinite(prediction).all():
        raise ValueError('Invalid model prediction')
    return pd.Series(prediction, index=frame.index, name='predicted_sales_revenue_lkr')


def predict_sales(features: pd.DataFrame, model_path=DEFAULT_BUNDLE_PATH) -> pd.Series:
    """Predict revenue for precomputed Member 1 adstock + external features."""
    return _predict_bundle(load_model(model_path), features)


def predict_budget_allocation(allocation: Mapping[str, float],
                              external_factors: Mapping[str, float] | None = None,
                              previous_adstock: Mapping[str, float] | None = None,
                              model_path=DEFAULT_BUNDLE_PATH) -> float:
    """Forecast ONE month's revenue from a raw monthly spending allocation.

    allocation: every *_spend_lkr channel (LKR, not millions).
    previous_adstock: state at end of preceding month keyed by *_adstock_lkr.
    external_factors: EVERY non-ad channel feature from the trained model;
        no implicit defaults, to avoid silently fabricated economic assumptions.
    When using multiple consecutive months, update previous_adstock after each month.
    """
    bundle = load_model(model_path)
    if not isinstance(allocation, Mapping) or set(allocation) != set(SPEND_CHANNELS):
        raise ValueError(f'allocation must specify exactly {list(SPEND_CHANNELS)}')
    if external_factors is None or previous_adstock is None:
        raise ValueError('Supply explicit external_factors and previous_adstock scenario assumptions')
    if not isinstance(external_factors, Mapping) or not isinstance(previous_adstock, Mapping):
        raise TypeError('external_factors and previous_adstock must be mappings')
    if set(previous_adstock) != set(ADSTOCK_CHANNELS):
        raise ValueError(f'previous_adstock must specify exactly {list(ADSTOCK_CHANNELS)}')
    needed_controls = set(bundle['feature_columns']) - set(ADSTOCK_CHANNELS) - {
        c + '_saturated' for c in ADSTOCK_CHANNELS
    }
    if set(external_factors) != needed_controls:
        raise ValueError(f'external_factors must specify exactly {sorted(needed_controls)}')
    def _number(value, name):
        try:
            number = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f'{name} must be numeric') from exc
        if not np.isfinite(number):
            raise ValueError(f'{name} must be finite')
        return number
    row = {}
    for spend, adstock in zip(SPEND_CHANNELS, ADSTOCK_CHANNELS):
        amount = _number(allocation[spend], spend)
        previous = _number(previous_adstock[adstock], adstock)
        if amount < 0 or previous < 0:
            raise ValueError('Advertising spend and previous adstock cannot be negative')
        row[adstock] = amount + DECAY_RATES[spend] * previous
    row.update({k: _number(v, k) for k, v in external_factors.items()})
    return float(_predict_bundle(bundle, pd.DataFrame([row])).iloc[0])


def next_adstock_state(allocation: Mapping[str, float], previous_adstock: Mapping[str, float]):
    """Return the post-allocation adstock state to use in the following month."""
    if set(allocation) != set(SPEND_CHANNELS) or set(previous_adstock) != set(ADSTOCK_CHANNELS):
        raise ValueError('Complete allocation and previous_adstock are required')
    out = {}
    for spend, adstock in zip(SPEND_CHANNELS, ADSTOCK_CHANNELS):
        amount, previous = float(allocation[spend]), float(previous_adstock[adstock])
        if not np.isfinite(amount) or not np.isfinite(previous) or min(amount, previous) < 0:
            raise ValueError('Advertising entries must be finite and nonnegative')
        out[adstock] = amount + DECAY_RATES[spend] * previous
    return out


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    data = pd.read_csv(root / 'data/processed/mmm_features.csv')
    print('Feature-row forecast:', predict_sales(data.tail(1)).iloc[0])
    previous = data.iloc[-1]
    controls = {c: float(previous[c]) for c in load_model()['feature_columns']
                if c not in ADSTOCK_CHANNELS and not c.endswith('_saturated')}
    budget = 18_000_000
    allocation = dict(zip(SPEND_CHANNELS, [budget / 6] * 6))
    print('Equal-budget scenario:', predict_budget_allocation(
        allocation, controls, {c: float(previous[c]) for c in ADSTOCK_CHANNELS}))
