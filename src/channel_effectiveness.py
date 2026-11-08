"""
Member 1 - Channel Effectiveness & ROI Analysis
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from src.predict_sales import (
    predict_budget_allocation,
    SPEND_CHANNELS
)

DATA_PATH = ROOT / "data/processed/cleaned_data.csv"
MODEL_PATH = ROOT / "models/mmm_model.joblib"

OUTPUT_DIR = ROOT / "outputs/optimization"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():

    print("Loading data...")

    df = pd.read_csv(DATA_PATH)

    spend_summary = pd.DataFrame({
    "Channel": list(SPEND_CHANNELS),

    "Total_Spend_LKR": [
        df[channel].sum()
        for channel in SPEND_CHANNELS
    ],

    "Average_Spend_LKR": [
        df[channel].mean()
        for channel in SPEND_CHANNELS
    ],

    "Min_Spend_LKR": [
        df[channel].min()
        for channel in SPEND_CHANNELS
    ],

    "Max_Spend_LKR": [
        df[channel].max()
        for channel in SPEND_CHANNELS
    ]
    })

    spend_summary["Spend_Share_Percent"] = (
        spend_summary["Total_Spend_LKR"]
        / spend_summary["Total_Spend_LKR"].sum()
    ) * 100

    spend_summary = spend_summary.sort_values(
        by="Total_Spend_LKR",
        ascending=False
    )

    model_bundle = joblib.load(MODEL_PATH)

    reference_controls = model_bundle["external_factors_reference"]
    reference_adstock = model_bundle["previous_adstock_reference"]

    baseline_allocation = {
        channel: df[channel].mean()
        for channel in SPEND_CHANNELS
    }

    baseline_prediction = predict_budget_allocation(
        allocation=baseline_allocation,
        external_factors=reference_controls,
        previous_adstock=reference_adstock
    )

    results = []

    for channel in SPEND_CHANNELS:

        allocation = baseline_allocation.copy()

        allocation[channel] *= 1.10

        new_prediction = predict_budget_allocation(
            allocation=allocation,
            external_factors=reference_controls,
            previous_adstock=reference_adstock
        )

        sales_change = new_prediction - baseline_prediction

        spend_change = (
            allocation[channel]
            - baseline_allocation[channel]
        )

        results.append({
            "Channel": channel,
            "Baseline_Spend": baseline_allocation[channel],
            "New_Spend": allocation[channel],
            "Predicted_Sales_Change_LKR": sales_change,
            "Spend_Increase_LKR": spend_change,
            "Response_Efficiency":
                sales_change / spend_change
        })

    effectiveness_df = pd.DataFrame(results)

    effectiveness_df = effectiveness_df.sort_values(
        by="Response_Efficiency",
        ascending=False,
    )

    effectiveness_df["Performance_Rank"] = (
        effectiveness_df["Response_Efficiency"]
        .rank(ascending=False)
        .astype(int)
    )

    channel_performance = spend_summary.merge(
    effectiveness_df[
        [
            "Channel",
            "Predicted_Sales_Change_LKR",
            "Response_Efficiency"
        ]
    ],
    on="Channel",
    how="left"
    )

    channel_performance["Performance_Rank"] = (
        channel_performance["Response_Efficiency"]
        .rank(ascending=False)
        .astype(int)
    )

    channel_performance = channel_performance.sort_values(
        by="Performance_Rank"
    )

    csv_columns = [
        "Channel",
        "Total_Spend_LKR",
        "Average_Spend_LKR",
        "Min_Spend_LKR",
        "Max_Spend_LKR",
        "Spend_Share_Percent",
        "Predicted_Sales_Change_LKR",
        "Response_Efficiency",
        "Performance_Rank"
    ]

    channel_performance = channel_performance[csv_columns]

    channel_performance.to_csv(
        OUTPUT_DIR / "channel_effectiveness.csv",
        index=False
    )

    print("Channel effectiveness CSV exported successfully.")

    plt.figure(figsize=(10, 6))

    ax = sns.barplot(
    data=effectiveness_df,
    x="Channel",
    y="Predicted_Sales_Change_LKR",
    hue="Channel",
    palette="magma",
    dodge=False
    )

    if ax.legend_ is not None:
        ax.legend_.remove()

    plt.axhline(
        y=0,
        color="black",
        linestyle="--"
    )

    plt.title("Channel Effectiveness Comparison")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "channel_comparison.png",
        dpi=300
    )

    plt.close()

    print("Channel comparison chart saved")

    response_curves = {}

    for channel in SPEND_CHANNELS:

        spend_range = np.linspace(
            df[channel].min(),
            df[channel].max(),
            20
        )

        predictions = []

        for spend in spend_range:

            allocation = baseline_allocation.copy()
            allocation[channel] = spend

            prediction = predict_budget_allocation(
                allocation=allocation,
                external_factors=reference_controls,
                previous_adstock=reference_adstock
            )

            predictions.append(prediction)

        response_curves[channel] = {
            "spend": spend_range,
            "sales": predictions
        }

    fig, axes = plt.subplots(
        2,
        3,
        figsize=(16, 10)
    )

    axes = axes.flatten()

    for i, channel in enumerate(SPEND_CHANNELS):

        axes[i].plot(
            response_curves[channel]["spend"],
            response_curves[channel]["sales"]
        )

        axes[i].set_title(
            channel.replace("_spend_lkr", "")
        )

        axes[i].grid(True)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "channel_response_curves.png",
        dpi=300
    )

    plt.close()

    print("Response curves saved")
    print("Analysis complete.")


if __name__ == "__main__":
    main()