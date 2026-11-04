"""
Member 1 - Channel Effectiveness & ROI Analysis
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from src.predict_sales import (
    predict_budget_allocation,
    SPEND_CHANNELS
)

import joblib

ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = ROOT / "data/processed/cleaned_data.csv"
MODEL_PATH = ROOT / "models/mmm_model.joblib"

OUTPUT_DIR = ROOT / "outputs/optimization"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():

    print("Loading data...")

    df = pd.read_csv(DATA_PATH)

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

    effectiveness_df.sort_values(
        by="Response_Efficiency",
        ascending=False,
        inplace=True
    )

    effectiveness_df["Performance_Rank"] = (
        effectiveness_df["Response_Efficiency"]
        .rank(ascending=False)
        .astype(int)
    )

    effectiveness_df.to_csv(
        OUTPUT_DIR / "channel_effectiveness.csv",
        index=False
    )

    print("CSV exported")

    plt.figure(figsize=(10, 6))

    sns.barplot(
        data=effectiveness_df,
        x="Channel",
        y="Predicted_Sales_Change_LKR",
        palette="magma"
    )

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