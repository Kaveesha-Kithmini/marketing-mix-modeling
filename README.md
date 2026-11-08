## Project Workflow

The project follows these main steps:

**Step 1: Data Preparation**

Clean and prepare the historical marketing dataset.

## Files
- `data/processed/cleaned_data.csv`: required handoff, 36 rows × 25 columns.
- `notebooks/01_data_eda/01_data_cleaning.ipynb`: executed notebook with validation outputs.
- `data/processed/data_dictionary.csv`: updated dictionary for every column.
- `reports/advertising_spend_reconciliation.csv`: original and recalculated totals for all months.
- `data/raw/Dataset.xlsx`: unchanged source workbook, included for reproducibility.

## Run the Full Project (Windows)

From the project root, create the environment and install the pinned dependencies:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

In VS Code, open each notebook below, select the `.venv` Python kernel, and run all
cells in order. Do not delete `data/raw/Dataset.xlsx`; it is the original input.

1. `notebooks/01_data_eda/01_data_cleaning.ipynb`
2. `notebooks/01_data_eda/02_eda.ipynb`
3. `notebooks/02_mmm_model/01_feature_engineering.ipynb`
4. `notebooks/02_mmm_model/02_model_training.ipynb`
5. `notebooks/02_mmm_model/03_model_evaluation.ipynb`
6. `notebooks/03_roi_optimization/01_channel_effectiveness.ipynb`
7. `notebooks/03_roi_optimization/02_budget_optimization.ipynb`

The notebooks regenerate `data/processed/cleaned_data.csv`,
`data/processed/data_dictionary.csv`, and `data/processed/mmm_features.csv`, as
well as the model files under `models/` and analysis results under `outputs/`.
Manual deletion is not required for a normal rerun.

If the named kernel is not listed, choose the `.venv (Python 3.13)` interpreter.
It can also be registered with Jupyter from the project root:

```powershell
.\.venv\Scripts\python.exe -m ipykernel install --user --name marketing-mix-modeling --display-name "Python (Marketing Mix Modeling)"
```

To verify the notebook is using the project environment, run this in a cell:

```python
import sys
print(sys.executable)
```

The printed path must end with `.venv\Scripts\python.exe`. If a notebook reports
`ModuleNotFoundError` for a dependency such as `openpyxl`, switch to the `.venv`
kernel; installing packages into a different Python installation will not fix a
kernel mismatch.

### Generated Files

| Notebook stage | Generated files |
|---|---|
| Data cleaning | `data/processed/cleaned_data.csv`, `data/processed/data_dictionary.csv`, `reports/advertising_spend_reconciliation.csv` |
| EDA | Six charts under `outputs/eda/` |
| Feature engineering | `data/processed/mmm_features.csv`, `outputs/mmm/adstock_analysis.png` |
| Model training | Four candidate models under `models/`, `outputs/mmm/model_comparison.csv`, `outputs/mmm/saturation_curves.png` |
| Model evaluation | `models/mmm_model.joblib`, `outputs/mmm/model_evaluation.csv`, `outputs/mmm/actual_vs_predicted.png`, `outputs/mmm/residual_analysis.png` |
| Channel effectiveness | `outputs/optimization/channel_effectiveness.csv`, `outputs/optimization/channel_comparison.png`, `outputs/optimization/channel_response_curves.png` |
| Budget optimisation | `outputs/optimization/optimized_budget.csv`, `outputs/optimization/prediction_results.csv`, `outputs/optimization/budget_scenarios.csv`, and three charts under `outputs/optimization/` |

Rerunning notebooks may overwrite these generated files and save execution outputs
inside the notebooks. It does not require deleting generated files first. The raw
workbook under `data/raw/` is the input and must be kept.

## Member 2: Diminishing Returns & Model Training

After generating `data/processed/mmm_features.csv` with the Member 1 feature
engineering workflow, run
`notebooks/02_mmm_model/02_model_training.ipynb` from the project root.
It compares linear-adstock and Hill-saturated inputs using Multiple Linear
Regression and Ridge on a chronological holdout. It writes the model
comparison and saturation/response figure to `outputs/mmm/`, and saves four
serialized model candidates to `models/`. The source implementation of the
Hill saturation transform is in `src/saturation.py`.

No missing values or duplicates needed removal. The 16 total-spend differences of LKR 1–2 were reconciled using the six channel amounts; the reason for the source differences is unconfirmed. The dictionary wildcard for channel spending was expanded into named columns. No other numeric source values were changed.


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

**Deadline:** November 2, 2026

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
- Identify the allocation with the highest model-predicted sales revenue.
- Compare current and optimised advertising budgets.
- Calculate predicted sales for the recommended allocation.
- Export optimisation results for the dashboard.

### Expected Deliverables

- Channel effectiveness analysis
- Model-based channel response analysis; ROI / ROAS where suitable profit and attribution data are available
- Budget optimisation Python code
- `optimized_budget.csv`
- `prediction_results.csv`
- Current vs optimised budget comparison
- Marketing budget recommendations

The current optimizer maximises **model-predicted sales revenue** under a fixed
budget; it does not calculate actual ROI. Profit-margin and causal incrementality
data are not available. Treat the results as scenario-based sales forecasts, not
causal returns. Actual ROI optimisation requires incremental profit estimates.

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
| Part 03 - ROI & Budget Optimisation | 2 | November 5 |
| Part 04 - Power BI Dashboard | 2 | November 10 |
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
