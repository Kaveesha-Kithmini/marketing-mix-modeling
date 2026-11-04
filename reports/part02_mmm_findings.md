# Part 02 — Marketing Mix Model Evaluation and Integration (Member 3)

## Dataset and methodology

- **36 monthly observations:** January 2023–December 2025; target: `sales_revenue_lkr`.
- **Six channels:** TV, Facebook/Instagram, Google Search, YouTube, Radio, Outdoor.
- **External controls:** price, promotions, competitor pressure, economic sentiment, exchange rate, inflation proxy, seasonal demand, holidays, and cyclic month indicators.
- **Chronological split:** 28 training months (January 2023–April 2025) and 8 holdout months (May–December 2025). **No shuffle.**
- Four candidate estimators and their fitting came from Member 2. **Member 3 reuses saved fitted estimators and independently verifies metrics** rather than fitting on the holdout.
- **Selection criterion:** Member 2's 3-fold expanding-window CV mean RMSE, not the holdout score; the separate holdout provides an out-of-sample check. Member 2's three CV folds have substantial score variability and use a small sample.

## Model comparison

| model                                | train_r2 | test_r2 | test_mae_lkr | test_rmse_lkr | cv_rmse_lkr_mean | selected_by_cv |
| :----------------------------------- | -------: | ------: | -----------: | ------------: | ---------------: | :------------- |
| saturated_ridge_regression           |    0.837 |   0.932 |  1145613.245 |   1325303.972 |      3660068.004 | True           |
| ridge_regression                     |    0.827 |   0.884 |  1592005.120 |   1729419.896 |      3825470.816 | False          |
| saturated_multiple_linear_regression |    0.916 |  -2.172 |  7361841.189 |   9025368.289 |      7802946.969 | False          |
| multiple_linear_regression           |    0.901 |  -1.131 |  6316696.841 |   7397996.571 |      9285440.006 | False          |

**Selected:** `saturated_ridge_regression` (lowest reported expanding-CV RMSE). Holdout R² = **0.9316**, MAE = **LKR 1,145,613**, RMSE = **LKR 1,325,304**. Train R² = 0.8367; train RMSE = LKR 3,244,754. The linear regression candidates have negative holdout R² despite high training R², indicating poor generalisation. The selected model's holdout error is lower than its training error; this is **not proof of no overfitting**, because samples are small and periods differ.

## Diagnostics and integration

- `outputs/mmm/actual_vs_predicted.png` compares the eight holdout months.
- `outputs/mmm/residual_analysis.png` contains **six diagnostic panels**: residual vs prediction, residual over time, residual histogram, Q–Q plot, lag correlation and absolute error per month. With only eight holdout observations, diagnostic conclusions are limited.
- Exact holdout predictions and residuals are **displayed in the notebook** (not exported as a separate CSV; The notebook generates the four required model and evaluation outputs. The complete Member 3 submission contains seven deliverables).
- `models/mmm_model.joblib` contains the saved fitted estimator, its **training-derived Hill midpoints**, saturation slope 1.5, ordered model feature columns, and adstock decay assumptions.
- `src/predict_sales.py` exposes `predict_sales(features)` for existing Member 1 adstock rows, plus `predict_budget_allocation(allocation, external_factors, previous_adstock)` for monthly raw budgets. The recurrence is `current_adstock = current_spend + decay * previous_adstock`.
- Three equal-total-spend budget scenario forecasts are **displayed in the notebook** (not exported as a separate CSV). External controls and adstock state are held at the **December 2025 peak-season snapshot**; these are hypothetical comparisons rather than measured ROI or typical-month forecasts.
- Additional integration checks verify matching feature-path and raw-spend-path forecasts, rejection of negative spend, and propagation of month-to-month adstock states. A radio-spend sensitivity probe indicates a **negative conditional association** in the saved model (+LKR 100,000 radio is associated with approximately **LKR 15,221 lower predicted revenue** near the fixed reference allocation); this is not a causal channel effect.

## Additional rolling-origin robustness evaluation

- **Eight expanding-window, one-month-ahead refits** were conducted within January 2023–April 2025 (first 28 observations only); each fit used the earliest 20 to 27 observations to predict the next month. Each fold independently fitted its Ridge scaler, coefficients, and training-only Hill midpoints. The final May–December 2025 holdout was not used in these refits.
- Results: **R² = 0.5860, MAE = LKR 2,832,744, RMSE = LKR 4,529,052** (rounded). These additional figures are stored on the selected model's row of the required `outputs/mmm/model_evaluation.csv`, under `rolling_8x1_*` columns.
- This check is substantially weaker than the held-out eight-month score (R² = 0.9316; RMSE = LKR 1,325,304). Different training horizons, one-step forecast validation months, sample sizes and time-varying data relationships can create such a gap. It argues against promising the holdout accuracy for future periods.
- **Selection remains based on Member 2’s earlier three-fold expanding-window CV**, not this secondary check or the final holdout. This secondary test diagnoses robustness and does not replace model selection.

## Interpretation, limitations, and recommendations

1. **Predictive accuracy is not causal attribution.** Correlation, coefficients, and scenario differences do not establish advertising incrementality, channel ROI, or true returns from moving budgets. Causal MMM would require stronger identification and ideally experiments/holdouts.
2. Member 1's **adstock decays are illustrative assumptions**, not estimated or validated channel carryover. Hill slope is fixed (1.5); midpoints come from the training period. Optimisation is sensitive to these choices.
3. There are only 36 rows, with 28 training observations versus 16 input features. Estimates are fragile, affected by collinearity, time trends, and unobserved confounders. More historical data, proper nested rolling backtests, uncertainty intervals, and stability checks are recommended.
4. **Do not treat budget scenarios as validated ROI optimisation outcomes.** They use an observational prediction model and fixed future controls. The budget team should set clear assumptions for all economic/seasonal fields, adstock state, feasible channel bounds and pacing; remain near observed spend ranges and avoid extrapolation.
5. Because adstock is stateful, multi-month optimisation must propagate each month's updated adstock to the next. Never treat consecutive months as independent.
6. Bundle is **not refitted on all 36 months**: saved weights remain trained through April 2025 so May–December 2025 metrics remain an honest holdout. Retraining for a real future deployment should occur only after documenting this evaluation.
7. Avoid interpreting high in-sample/holdout R² as a guarantee of future success. Track drift, data availability, uncertainty and sales definitions.

## Important data caveats

- The data have only 36 monthly rows and May–December 2025 is a single eight-month test period; the rolling backtest does not cover every season equally.
- Adstock decay rates were chosen as initial assumptions by Member 1 rather than empirically identified, and some modeled channel response directions (notably radio in a local sensitivity probe) are counterintuitive. Treat channels as conditional regressors, not causal contribution measurements.
- The reported December 2025 scenario controls reflect a peak-season reference. Future planning requires future values for all external factors and updated prior-month adstock; it is invalid to call these typical-month predictions.

## Deliverables

- `notebooks/02_mmm_model/03_model_evaluation.ipynb`
- `src/predict_sales.py`
- `models/mmm_model.joblib`
- `outputs/mmm/model_evaluation.csv`, `actual_vs_predicted.png`, `residual_analysis.png`
- Budget scenarios and holdout results are displayed within the notebook
- `reports/part02_mmm_findings.md`

## Reproduce

From the cloned project root, install dependencies, start Jupyter, and run all cells in `notebooks/02_mmm_model/03_model_evaluation.ipynb`. This notebook generates the four required files. Only load trusted local `.joblib` files; joblib uses Python pickle.
