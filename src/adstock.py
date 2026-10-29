
"""
Member 1: Advertising Adstock transformations
Marketing Mix Modeling (MMM)

Geometric Adstock:
A[t] = spend[t] + decay * A[t-1]
"""

import numpy as np
import pandas as pd


# Six advertising channels in the cleaned dataset.
CHANNELS = [
    "tv_spend_lkr",
    "facebook_instagram_spend_lkr",
    "google_search_spend_lkr",
    "youtube_spend_lkr",
    "radio_spend_lkr",
    "outdoor_spend_lkr",
]


# Initial illustrative decay-rate assumptions.
# These are NOT empirically fitted decay rates.
DECAY_RATES = {
    "tv_spend_lkr": 0.60,
    "facebook_instagram_spend_lkr": 0.30,
    "google_search_spend_lkr": 0.20,
    "youtube_spend_lkr": 0.40,
    "radio_spend_lkr": 0.40,
    "outdoor_spend_lkr": 0.50,
}


def geometric_adstock(spend, decay=0.5):
    """
    Apply geometric Adstock to a monthly spending series.

    Parameters:
        spend: 1D advertising spend sequence.
        decay: Carryover rate between 0 and 1.

    Returns:
        numpy array containing transformed values.
    """

    if not 0 <= decay < 1:
        raise ValueError(
            "Decay rate must be between 0 and 1."
        )

    values = np.asarray(spend, dtype=float)

    if values.ndim != 1:
        raise ValueError("Spend must be one-dimensional.")

    if not np.isfinite(values).all():
        raise ValueError("Spend contains invalid values.")

    if (values < 0).any():
        raise ValueError("Spend cannot be negative.")

    adstock = np.zeros(len(values), dtype=float)

    for t in range(len(values)):
        previous = adstock[t - 1] if t > 0 else 0
        adstock[t] = values[t] + decay * previous

    return adstock


def apply_adstock(df, decay_rates=None):
    """
    Add six Adstock-transformed advertising features.

    The dataframe must already be sorted by month.
    """

    if decay_rates is None:
        decay_rates = DECAY_RATES

    result = df.copy()

    for channel in CHANNELS:

        if channel not in result.columns:
            raise KeyError(
                f"Required channel missing: {channel}"
            )

        if channel not in decay_rates:
            raise KeyError(
                f"Decay rate missing for: {channel}"
            )

        new_column = channel.replace(
            "_spend_lkr", "_adstock_lkr"
        )

        result[new_column] = geometric_adstock(
            result[channel].values,
            decay_rates[channel]
        )

    return result


def adstock_half_life(decay):
    """
    Calculate advertising carryover half-life in months.

    The half-life is the time required for a past
    advertisement's remaining effect to halve.
    """

    if not 0 <= decay < 1:
        raise ValueError("Invalid decay rate.")

    if decay == 0:
        return 0.0

    return float(np.log(0.5) / np.log(decay))


if __name__ == "__main__":

    # Small functionality test.
    example_spend = [100, 200, 150]

    result = geometric_adstock(
        example_spend, decay=0.5
    )

    print("Original:", example_spend)
    print("Adstock:", result)

    assert np.allclose(
        result, [100, 250, 275]
    )

    print("Adstock test passed!")
