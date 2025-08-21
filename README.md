# Amazon-Sales-Data-Exploratory-Data-Analysis-EDA-
This project performs an in-depth Exploratory Data Analysis (EDA) on Amazon Sales data to uncover insights about sales performance, customer behavior, discounts, and returns. The goal is to identify key business drivers and provide actionable recommendations to optimize performance.

# 📊 Amazon Sales Data — Exploratory Data Analysis (EDA)

## 📌 Project Overview
This repository contains an end-to-end EDA of Amazon Sales data to uncover insights about sales performance, discounts, returns, delivery performance, and customer behavior. The outcome is a set of business-ready insights and recommendations.

> **Tip:** Replace all placeholders (marked like `<<this>>`) with your project-specific details.

---

## 📂 Dataset Description
- **Source**: <<link or note if synthetic](https://docs.google.com/spreadsheets/d/1XU8dWfq_MbKqgRsXFcUNZCtpnk2fWmNlMX-Hq1IO4mc/edit?usp=sharing)>>
- **Size**: <<25000>> × <<19>>
- **Date Range**: <<2025 Sales DATA>>
- **Key Columns**:
  - `OrderID` — Unique order identifier
  - `OrderDate` — Order date
  - `Category` — Product category
  - `Brand` — Brand name
  - `Price`, `Quantity`, `Revenue` — Transaction metrics
  - `Age` — Customer age
  - `Device` — Platform (Mobile, Desktop, Tablet)
  - `Region` — Customer region/country/state
  - `DiscountPercent` — Discount applied
  - `DeliveryStatus` — On-Time / Late
  - `Returned` — 1 if returned, else 0

---

## 🛠️ Methodology
1. Data Quality Assessment & Cleaning (missingness, duplicates, types, outliers)
2. Univariate Analysis
3. Bivariate/Multivariate Analysis
4. Cross-Analysis (e.g., Category × Device returns, Region × Delivery)
5. Hypothesis Testing (at least 5)
6. Insight Synthesis & Recommendations

---

## 📊 Data Quality Report
See `reports/data_quality_report.md` for details on:
- Missing values
- Duplicates
- Data types
- Outliers
- Cleaning actions

---

## 🔑 Key Insights & Actions
See `reports/insight_summary.md` for the top **5–8 business insights** with visuals and **recommended actions**.

---

## 🧪 Hypothesis Testing
See `reports/hypothesis_testing.md` for hypotheses, methods (Chi-square, t-test/ANOVA), results and business interpretation.

---

## 🖼️ Visualizations
All plots are saved in `visuals/plots/` and embedded in the notebook/script outputs.

---

## ▶️ Reproducibility
1. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Put your data file at `data/amazon_sales.csv` (or pass a custom path).

3. Run the report generator (will produce plots + markdown reports):
   ```bash
   python scripts/eda_report_generator.py --csv data/amazon_sales.csv
   ```

4. (Optional) Open the notebook and explore interactively.

---

## 📚 Tech Stack
- Python (pandas, numpy, scipy, statsmodels, matplotlib)
- Jupyter Notebook

---

## 🙌 Credits
Created by <<Hira Barlas>> — Last updated: 2025-08-21

