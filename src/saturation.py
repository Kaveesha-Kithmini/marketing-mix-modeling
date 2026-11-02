"""Advertising saturation transformations for Marketing Mix Modeling."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Protocol, runtime_checkable

import numpy as np
import pandas as pd


ADSTOCK_CHANNELS = (
    "tv_adstock_lkr",
    "facebook_instagram_adstock_lkr",
    "google_search_adstock_lkr",
    "youtube_adstock_lkr",
    "radio_adstock_lkr",
    "outdoor_adstock_lkr",
)

SATURATION_SUFFIX = "_saturated"


@runtime_checkable
class Regressor(Protocol):
    """Minimal prediction interface expected from a saved estimator."""

    def predict(self, features: pd.DataFrame) -> np.ndarray: ...


def hill_saturation(values, half_saturation: float, slope: float = 1.0):
    """Apply a Hill curve, returning values bounded between zero and one."""
    if not np.isfinite(half_saturation) or half_saturation <= 0:
        raise ValueError("half_saturation must be a finite positive number.")
    if not np.isfinite(slope) or slope <= 0:
        raise ValueError("slope must be a finite positive number.")

    values_array = np.asarray(values, dtype=float)
    if not np.isfinite(values_array).all():
        raise ValueError("values contain invalid entries.")
    if (values_array < 0).any():
        raise ValueError("Advertising values cannot be negative.")

    powered = np.power(values_array, slope)
    midpoint = half_saturation**slope
    result = np.divide(
        powered,
        powered + midpoint,
        out=np.zeros_like(powered, dtype=float),
        where=(powered + midpoint) != 0,
    )
    return float(result) if result.ndim == 0 else result


def apply_saturation(
    df: pd.DataFrame,
    channels: Sequence[str] = ADSTOCK_CHANNELS,
    half_saturation: Mapping[str, float] | None = None,
    slope: float = 1.5,
    suffix: str = SATURATION_SUFFIX,
) -> pd.DataFrame:
    """Add Hill-saturated channel columns without modifying the input frame.

    When no midpoint is supplied for a channel, its positive observed median is
    used. Midpoints can be supplied explicitly to make a fitted transform
    reusable on later data.
    """
    result = df.copy()
    midpoints = {} if half_saturation is None else dict(half_saturation)

    for channel in channels:
        if channel not in result.columns:
            raise KeyError(f"Required channel missing: {channel}")

        midpoint = midpoints.get(channel)
        if midpoint is None:
            positive = pd.to_numeric(result[channel], errors="raise")
            positive = positive[positive > 0]
            if positive.empty:
                raise ValueError(
                    f"Cannot infer half-saturation for {channel}: "
                    "no positive observations."
                )
            midpoint = float(positive.median())

        result[f"{channel}{suffix}"] = hill_saturation(
            result[channel].to_numpy(),
            half_saturation=float(midpoint),
            slope=slope,
        )

    return result


def predict_sales(
    model_bundle: Mapping[str, object], features: pd.DataFrame
) -> pd.Series:
    """Predict sales from Member 1 feature rows using a saved model bundle."""
    estimator = model_bundle.get("estimator")
    if not isinstance(estimator, Regressor):
        raise TypeError("model_bundle must contain an estimator with predict().")

    variant = model_bundle.get("feature_variant")
    if variant not in {"linear_adstock", "hill_saturated"}:
        raise ValueError(f"Unsupported feature variant: {variant!r}")

    feature_columns = model_bundle.get("feature_columns")
    if (
        not isinstance(feature_columns, list)
        or not feature_columns
        or not all(isinstance(column, str) for column in feature_columns)
    ):
        raise ValueError("model_bundle must contain a non-empty feature_columns list.")

    missing_channels = [channel for channel in ADSTOCK_CHANNELS if channel not in features]
    if missing_channels:
        raise KeyError(f"Required adstock features missing: {missing_channels}")

    model_features = features.copy()
    if variant == "hill_saturated":
        midpoints = model_bundle.get("saturation_midpoints")
        slope = model_bundle.get("saturation_slope")
        if not isinstance(midpoints, Mapping) or not isinstance(slope, (int, float)):
            raise ValueError("Saturated model bundle is missing valid Hill settings.")
        model_features = apply_saturation(
            model_features,
            half_saturation=midpoints,
            slope=float(slope),
        )

    missing_columns = [
        column for column in feature_columns if column not in model_features
    ]
    if missing_columns:
        raise KeyError(f"Model input features missing: {missing_columns}")

    matrix = model_features.loc[:, feature_columns].astype(float)
    if not np.isfinite(matrix.to_numpy()).all():
        raise ValueError("Model input features contain invalid values.")

    predictions = estimator.predict(matrix)
    return pd.Series(predictions, index=features.index, name="predicted_sales_revenue_lkr")
