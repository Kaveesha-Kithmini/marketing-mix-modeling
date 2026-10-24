## Project Workflow

The project follows these main steps:

**Step 1: Data Preparation**

Clean and prepare the historical marketing dataset.

↓

**Step 2: Exploratory Data Analysis**

Identify sales patterns, advertising trends, and relationships between variables.

↓

**Step 3: Marketing Mix Model Development**

Train a Machine Learning model to estimate advertising effectiveness and predict sales.

↓

**Step 4: Budget Optimisation**

Use the trained model and mathematical optimisation to find the best advertising budget allocation.

↓

**Step 5: Power BI Dashboard**

Visualise marketing performance, model predictions, and recommended budget allocations.

---

# Project Task Allocation

The project is divided into four main parts.

Each part has specific responsibilities, expected outputs, and deadlines.

## PART 01 - Data Preparation & Exploratory Data Analysis (EDA)

**Required Members:** 2

**Deadline:** October 28, 2026

### Task 1: Data Cleaning & Preprocessing

Responsibilities:

- Understand the marketing dataset.
- Identify important columns and variables.
- Check for missing values.
- Identify and remove duplicate records.
- Correct incorrect data types.
- Check data consistency.
- Handle invalid values where necessary.
- Prepare the cleaned dataset.
- Create a data dictionary explaining the variables.

### Task 2: Exploratory Data Analysis (EDA)

Responsibilities:

- Analyse overall sales performance.
- Analyse advertising expenditure across channels.
- Identify monthly sales trends.
- Compare marketing channel spending.
- Analyse relationships between advertising spending and sales.
- Create correlation visualisations.
- Analyse seasonal patterns.
- Explore external factors affecting sales.
- Create graphs and charts using Matplotlib and Seaborn.
- Summarise important findings.

### Expected Deliverables

- `cleaned_data.csv`
- Data cleaning Jupyter Notebook
- EDA Jupyter Notebook
- Data dictionary
- Sales and advertising visualisations
- EDA findings summary

### Tools

Python, Pandas, NumPy, Matplotlib, Seaborn

---

## PART 02 - Marketing Mix Model Development (ML)

**Required Members:** 3

**Deadline:** November 4, 2026

### Task 1: Adstock Analysis & Feature Engineering

Responsibilities:

- Understand advertising time-delay effects.
- Analyse how previous advertising spending may affect current sales.
- Implement Adstock transformations.
- Prepare advertising features for model training.
- Include relevant external factors.
- Prepare the final model input dataset.

### Task 2: Diminishing Returns & Model Training

Responsibilities:

- Understand diminishing returns in advertising.
- Analyse advertising saturation effects.
- Implement saturation transformations.
- Develop a baseline Multiple Linear Regression model.
- Train a Ridge Regression model.
- Compare baseline and transformed models.
- Identify a suitable model for sales prediction.

### Task 3: Model Evaluation & Integration

Responsibilities:

- Evaluate Machine Learning model performance.
- Calculate R² Score, MAE, and RMSE.
- Perform time-based model validation.
- Check for overfitting.
- Compare model results.
- Select a suitable final model.
- Save the trained model.
- Prepare a reusable sales prediction function.
- Connect the prediction function with the optimisation team.

### Expected Deliverables

- Feature engineering code
- Adstock analysis
- Diminishing returns analysis
- Trained Marketing Mix Model
- Model training Jupyter Notebook
- Model evaluation results
- Saved model (`mmm_model.joblib`)
- Reusable sales prediction function

### Tools

Python, NumPy, Scikit-learn, Statsmodels, SciPy

---

## PART 03 - Channel Effectiveness, ROI Analysis & Budget Optimisation

**Required Members:** 2

**Deadline:** November 9, 2026

### Task 1: Channel Effectiveness & ROI Analysis

Responsibilities:

- Analyse marketing channel effectiveness.
- Estimate individual channel contributions using the MMM results.
- Compare advertising channel performance.
- Calculate Return on Ad Spend (ROAS).
- Calculate ROI if suitable profit or margin data is available.
- Identify high-performing marketing channels.
- Identify channels with lower estimated returns.
- Prepare channel performance comparisons.
- Summarise marketing recommendations.

### Task 2: Mathematical Budget Optimisation

Responsibilities:

- Understand the fixed advertising budget problem.
- Develop a mathematical optimisation algorithm using SciPy.
- Connect the algorithm with the trained Marketing Mix Model.
- Apply budget constraints.
- Generate different marketing budget allocations.
- Identify the allocation with the highest predicted return.
- Compare current and optimised advertising budgets.
- Calculate predicted sales for the recommended allocation.
- Export optimisation results for the dashboard.

### Expected Deliverables

- Channel effectiveness analysis
- ROI / ROAS analysis
- Budget optimisation Python code
- `optimized_budget.csv`
- `prediction_results.csv`
- Current vs optimised budget comparison
- Marketing budget recommendations

### Tools

Python, Pandas, NumPy, SciPy, Scikit-learn

---

## PART 04 - Interactive Power BI Dashboard

**Required Members:** 2

**Deadline:** November 12, 2026

### Task 1: Dashboard Design & Marketing Analytics

Responsibilities:

- Plan the Power BI dashboard layout.
- Import the cleaned marketing dataset.
- Create marketing performance visualisations.
- Display total advertising expenditure.
- Display sales revenue trends.
- Create channel spending comparisons.
- Visualise ROI / ROAS results.
- Create key performance indicators (KPIs).
- Design a clean and user-friendly dashboard.

### Task 2: Optimisation Dashboard & Interactivity

Responsibilities:

- Import Machine Learning prediction results.
- Import budget optimisation results.
- Display current vs optimised advertising budgets.
- Create optimal budget allocation charts.
- Visualise predicted sales improvements.
- Add interactive filters.
- Add budget scenario comparisons where available.
- Check dashboard calculations.
- Test dashboard functionality.
- Prepare the final dashboard.

### Expected Deliverables

- `marketing_dashboard.pbix`
- Interactive Power BI dashboard
- Advertising performance visualisations
- ROI / ROAS comparison charts
- Budget optimisation visualisations
- Dashboard screenshots

### Tools

Power BI, Power Query, DAX

---

# 7. Project Timeline

| Project Part | Members | Deadline |
|--------------|---------|----------|
| Part 01 - Data Preparation & EDA | 2 | October 28 |
| Part 02 - MMM Model Development | 3 | November 4 |
| Part 03 - ROI & Budget Optimisation | 2 | November 9 |
| Part 04 - Power BI Dashboard | 2 | November 12 |
| Final Integration & Testing | November 13 |
| Final Submission | November 13 |

**Total Members: 10**

---

# 8. Project Integration

All four parts must work together as one complete analytical solution.

### Integration Process

1. The Data Preparation team provides the cleaned dataset.
2. The Machine Learning team uses the cleaned data to train the Marketing Mix Model.
3. The Optimisation team uses the trained model to generate recommended budget allocations.
4. The Power BI team uses the analysis, prediction, and optimisation results to create the dashboard.
5. All members work together to test and finalise the project.

### Integration Tasks

- Verify that the cleaned data works with the ML model.
- Check that the optimisation algorithm uses the correct prediction function.
- Check budget constraints and optimisation calculations.
- Verify that Power BI displays the correct results.
- Test the complete workflow.
- Organise project files in GitHub.
- Resolve integration errors.

**Integration Deadline: November 16, 2026**

---

# 9. GitHub Repository Structure

```text
marketing-mix-modeling/
|
|-- data/
|   |-- raw/
|   |-- processed/
|
|-- notebooks/
|   |-- 01_data_eda/
|   |-- 02_mmm_model/
|   |-- 03_roi_optimization/
|
|-- src/
|
|-- models/
|
|-- outputs/
|
|-- dashboard/
|
|-- reports/
|
|-- README.md
|-- requirements.txt
|-- .gitignore
```

### Folder Descriptions

| Folder | Purpose |
|--------|---------|
| data/raw | Original marketing dataset |
| data/processed | Cleaned and processed datasets |
| notebooks/01_data_eda | Data cleaning and EDA notebooks |
| notebooks/02_mmm_model | Machine Learning development notebooks |
| notebooks/03_roi_optimization | ROI analysis and optimisation notebooks |
| src | Reusable Python source code |
| models | Saved trained Machine Learning models |
| outputs | Prediction results, graphs, and optimisation outputs |
| dashboard | Power BI dashboard files |
| reports | Final report  |

---
