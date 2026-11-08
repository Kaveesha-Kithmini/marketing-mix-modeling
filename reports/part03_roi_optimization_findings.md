
# Part 03 – Channel Effectiveness & Budget Optimisation Findings

## 1. Introduction

This part analyses the effectiveness of six advertising channels and develops a mathematical budget optimisation algorithm using the trained Marketing Mix Model (MMM).

The main objective is to identify differences in estimated channel responses and recommend an advertising budget allocation that maximises predicted sales revenue under a fixed budget.

## 2. Channel Effectiveness Analysis

Historical advertising expenditure and sales data were analysed using the cleaned dataset.

A trained MMM model was used to estimate how predicted sales change when individual channel spending increases by 10%, while other channel budgets, external factors and previous Adstock values remain constant.

### Channel Effectiveness Results

| Marketing Channel | Predicted Sales Change (LKR) | Response Efficiency |
|---|---:|---:|
| Google Search | 536,925 | 1.620 |
| YouTube | 302,870 | 1.364 |
| Facebook / Instagram | 193,996 | 0.441 |
| TV | 188,777 | 0.433 |
| Outdoor | 93,914 | 0.359 |
| Radio | -41,427 | -0.248 |

Google Search and YouTube showed the highest estimated responses under the selected model assumptions.

Radio showed a negative conditional model response in this scenario. This does not prove that radio advertising causes a decrease in sales.

Response Efficiency is calculated as predicted sales change divided by additional advertising expenditure. It is a model-based measure, not actual ROAS or profit ROI.

## 3. Budget Optimisation Methodology

A mathematical optimisation algorithm was developed using SciPy's SLSQP method.

The objective was to maximise predicted sales revenue using the trained MMM model.

The following constraints were applied:

- Total advertising expenditure must equal the fixed budget.
- Channel budgets cannot be negative.
- Each channel allocation must remain within its historical minimum and maximum spending limits.

The historical average monthly advertising allocation was used as the reference allocation.

## 4. Optimised Budget Allocation

The reference monthly advertising budget was approximately LKR 18.58 million.

### Reference vs Optimised Allocation

| Channel | Reference Budget (LKR) | Optimised Budget (LKR) |
|---|---:|---:|
| TV | 4,360,118 | 3,357,071 |
| Facebook / Instagram | 4,398,434 | 3,998,492 |
| Google Search | 3,315,365 | 5,096,864 |
| YouTube | 2,219,826 | 3,178,264 |
| Radio | 1,669,667 | 1,217,450 |
| Outdoor | 2,612,717 | 1,727,984 |
| **Total** | **18,576,126** | **18,576,126** |

The optimisation results allocated more budget to Google Search and YouTube, while reducing allocations to other channels.

## 5. Predicted Sales Comparison

| Metric | Reference Allocation | Optimised Allocation |
|---|---:|---:|
| Total Advertising Budget | LKR 18,576,126 | LKR 18,576,126 |
| Predicted Sales Revenue | LKR 96,065,072 | LKR 98,784,046 |

- Predicted sales difference: LKR 2,718,973
- Predicted sales improvement: 2.83%

These values represent model-based predictions under the selected assumptions.

## 6. Budget Scenario Analysis

Different total advertising budget scenarios were tested.

| Budget Scenario | Total Budget (LKR) | Predicted Sales Improvement |
|---|---:|---:|
| 80% | 14,860,901 | 2.29% |
| 90% | 16,718,513 | 3.17% |
| 100% | 18,576,126 | 2.83% |
| 110% | 20,433,738 | 2.37% |
| 120% | 22,291,351 | 1.92% |

The 90% budget scenario produced the highest estimated improvement compared with its corresponding reference allocation.

## 7. Limitations

- The dataset contains only 36 monthly observations and is synthetic.
- Model predictions do not establish causal advertising impact.
- Adstock decay rates are assumptions and have not been independently validated.
- External factors and previous Adstock values were held at the December 2025 model reference values during optimisation.
- Historical minimum and maximum spending limits influence the recommended allocation.
- Actual profit-based ROI cannot be calculated because profit margins and complete business cost information are unavailable.
- Predicted sales revenue should not be interpreted as profit or guaranteed future sales.

## 8. Conclusion and Recommendations

The analysis identified Google Search and YouTube as channels with stronger estimated responses under the selected model assumptions.

The SciPy optimisation algorithm successfully generated a budget allocation satisfying the fixed total budget and channel spending constraints.

The optimised allocation produced a 2.83% increase in predicted sales revenue compared with the reference allocation.

These findings can support exploratory advertising budget planning. However, the recommendations should be validated using additional real-world data, profit information and marketing experiments before making actual business investment decisions.

## 9. Generated Outputs

The following files were generated for the project:

- `outputs/optimization/channel_effectiveness.csv`
- `outputs/optimization/optimized_budget.csv`
- `outputs/optimization/prediction_results.csv`
- `outputs/optimization/budget_scenarios.csv`
- `outputs/optimization/channel_comparison.png`
- `outputs/optimization/channel_response_curves.png`
- `outputs/optimization/budget_comparison.png`
- `outputs/optimization/sales_improvement.png`
- `outputs/optimization/budget_scenarios.png`
