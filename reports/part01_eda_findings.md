# Exploratory Data Analysis (EDA) Findings

**Project:** Marketing Mix Modelling & Budget Optimisation   


## 1. Dataset Overview

The cleaned dataset contains 36 monthly observations and 25 columns, covering sales revenue, advertising expenditure across six channels, and external market factors. No missing values were identified. The original data is labelled synthetic.

## 2. Monthly Sales Trends

Monthly sales revenue fluctuated during the analysis period, with an average of approximately LKR 85.09 million. The highest revenue occurred in April 2023 (LKR 100.71 million), while the lowest occurred in January 2023 (LKR 68.73 million).

Average revenue declined in 2024 compared with 2023, before recovering in 2025. The chart does not show a consistent upward or downward sales trend.

## 3. Advertising Expenditure by Channel

Facebook/Instagram received the highest total advertising expenditure of approximately LKR 158.34 million, followed by TV with LKR 156.96 million. Radio received the lowest expenditure at LKR 60.11 million.

The spending distribution indicates that the company allocated more resources to Facebook/Instagram and TV than to other channels. However, higher expenditure does not necessarily indicate higher advertising effectiveness.

## 4. Advertising Spend and Sales Relationships

Total advertising expenditure demonstrated a moderate positive correlation with sales revenue (r = 0.45).

Outdoor advertising showed the strongest positive correlation among individual channels (r = 0.44), followed by Google Search (r = 0.38) and YouTube (r = 0.37). Radio showed a very weak relationship (r = 0.04).

These correlations describe associations and do not establish the causal impact or ROI of individual channels.

## 5. Seasonal Sales Patterns

Seasonal analysis indicated that December and April recorded the highest average sales revenue, at approximately LKR 96.65 million and LKR 95.87 million respectively.

February recorded the lowest average at approximately LKR 78.84 million. These findings suggest potential seasonal variation, although only three years of data are available.

## 6. External Factors Affecting Sales

Seasonal demand demonstrated a positive correlation with sales revenue (r = 0.61). Promotional discounts also demonstrated a positive relationship (r = 0.58).

Competitor pressure was negatively correlated with sales revenue (r = -0.33), suggesting that greater competitive pressure tended to coincide with lower sales. Economic sentiment showed a weaker positive correlation (r = 0.18).

These variables should be considered when developing the Marketing Mix Model.

## 7. Recommendations

The MMM team should investigate the relationship between sales and advertising expenditure while controlling for promotions, seasonality and competitor pressure.

The model should also explore delayed advertising effects, diminishing returns, and correlations among advertising channels. Time-based model validation is recommended because the dataset contains only 36 observations.

## 8. Conclusion

The EDA identified fluctuating sales revenue, concentrated advertising expenditure, and meaningful associations between sales, advertising spend, and external factors.

These findings provide a foundation for Marketing Mix Modelling. Further analysis is required to estimate incremental advertising effectiveness and optimise budget allocation.

**Limitations:** The dataset is synthetic, the sample is relatively small, and correlation analysis alone cannot establish causation or channel ROI.