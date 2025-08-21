#!/usr/bin/env python3
"""
EDA Report Generator for Amazon Sales
-------------------------------------
Usage:
    python scripts/eda_report_generator.py --csv data/amazon_sales.csv

Outputs:
- reports/data_quality_report.md
- reports/insight_summary.md (skeleton to fill after reviewing plots)
- reports/hypothesis_testing.md (auto-fills key stats where possible)
- visuals/plots/*.png
"""
import argparse, os, sys, textwrap, warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm

warnings.filterwarnings("ignore")

# ---------- Helpers ----------
def ensure_dirs(base):
    for d in ["reports", "visuals/plots"]:
        os.makedirs(os.path.join(base, d), exist_ok=True)

def save_bar(series, title, ylabel, path):
    ax = series.sort_values(ascending=False).plot(kind="bar", title=title)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()

def iqr_outliers_count(s):
    q1, q3 = s.quantile([0.25, 0.75])
    iqr = q3 - q1
    lower, upper = q1 - 1.5*iqr, q3 + 1.5*iqr
    return ((s < lower) | (s > upper)).sum()

def chi_square_test(df, col_a, col_b, min_count=5):
    tab = pd.crosstab(df[col_a], df[col_b])
    if (tab < min_count).any().any():
        # combine rare categories
        tab = tab.loc[tab.sum(axis=1) >= min_count, tab.sum(axis=0) >= min_count]
    chi2, p, dof, exp = stats.chi2_contingency(tab)
    return chi2, p, dof, tab

def safe_mean(series):
    try:
        return series.mean()
    except Exception:
        return np.nan

# ---------- Main ----------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Path to CSV file")
    parser.add_argument("--base", default=".", help="Project root (default: current)")
    args = parser.parse_args()

    base = args.base
    ensure_dirs(base)

    df = pd.read_csv(args.csv)
    # Basic enrichments
    if "OrderDate" in df.columns:
        try:
            df["OrderDate"] = pd.to_datetime(df["OrderDate"])
        except:
            pass
    if "Age" in df.columns:
        bins = [18,25,35,45,55,200]
        labels = ["18-25","26-35","36-45","46-55","55+"]
        try:
            df["AgeGroup"] = pd.cut(df["Age"], bins=bins, labels=labels, right=True)
        except Exception:
            pass
    if ("Price" in df.columns) and ("Quantity" in df.columns) and ("Revenue" not in df.columns):
        df["Revenue"] = df["Price"] * df["Quantity"]

    # ---------- Data Quality Report ----------
    rows, cols = df.shape
    missing_pct = df.isna().mean().sort_values(ascending=False) * 100
    top_missing = missing_pct[missing_pct>0].head(10).round(2)
    dup_count = df.duplicated().sum()
    dtypes_table = df.dtypes.astype(str)

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    outlier_counts = {c: iqr_outliers_count(df[c].dropna()) for c in numeric_cols}

    start_date = df["OrderDate"].min().date().isoformat() if "OrderDate" in df.columns and pd.api.types.is_datetime64_any_dtype(df["OrderDate"]) else "<<unknown>>"
    end_date   = df["OrderDate"].max().date().isoformat() if "OrderDate" in df.columns and pd.api.types.is_datetime64_any_dtype(df["OrderDate"]) else "<<unknown>>"

    dq = f"""# 🧼 Data Quality Report

## 1) Overview
- Rows: {rows}
- Columns: {cols}
- Time range: {start_date} to {end_date}

## 2) Missingness
Top columns by missing %:
```
{top_missing.to_string() if len(top_missing)>0 else "No missing values"}
```

## 3) Duplicates
- Duplicate rows detected: {dup_count}

## 4) Data Types
```
{dtypes_table.to_string()}
```

## 5) Outliers (Numeric via IQR)
- Columns assessed: {numeric_cols}
- Outlier counts by column:
```
{pd.Series(outlier_counts).to_string() if len(numeric_cols)>0 else "No numeric columns"}
```

## 6) Cleaning Suggestions
- Impute or drop columns with high missingness
- Remove duplicates
- Cast types (e.g., dates) where appropriate
- Cap or transform extreme outliers if they distort analysis
"""
    with open(os.path.join(base, "reports/data_quality_report.md"), "w", encoding="utf-8") as f:
        f.write(dq)

    # ---------- Univariate / Key KPIs ----------
    # Revenue by Category
    if {"Revenue","Category"}.issubset(df.columns):
        rev_cat = df.groupby("Category")["Revenue"].sum().sort_values(ascending=False)
        save_bar(rev_cat, "Revenue by Category", "Revenue", os.path.join(base, "visuals/plots/revenue_by_category.png"))

    # Return rate by Category/Brand/Device
    if "Returned" in df.columns:
        if "Category" in df.columns:
            rr_cat = df.groupby("Category")["Returned"].mean() * 100
            save_bar(rr_cat, "Return Rate by Category", "Return Rate (%)", os.path.join(base, "visuals/plots/return_rate_by_category.png"))
        if "Brand" in df.columns:
            rr_brand = df.groupby("Brand")["Returned"].mean() * 100
            top = rr_brand.sort_values(ascending=False).head(20)
            save_bar(top, "Return Rate by Brand (Top 20)", "Return Rate (%)", os.path.join(base, "visuals/plots/return_rate_by_brand.png"))
        if "Device" in df.columns:
            rr_device = df.groupby("Device")["Returned"].mean() * 100
            save_bar(rr_device, "Return Rate by Device", "Return Rate (%)", os.path.join(base, "visuals/plots/return_rate_by_device.png"))

    # Discount vs Quantity (basic correlation)
    corr_line = ""
    if {"DiscountPercent","Quantity"}.issubset(df.columns):
        c = df[["DiscountPercent","Quantity"]].dropna().corr().iloc[0,1]
        corr_line = f"Correlation(DiscountPercent, Quantity) = {c:.3f}"

    # ---------- Hypothesis Tests (auto where possible) ----------
    results = []

    # H1: Device × Returned (chi-square)
    if {"Device","Returned"}.issubset(df.columns):
        chi2, p, dof, tab = chi_square_test(df.dropna(subset=["Device","Returned"]), "Device", "Returned")
        results.append(("Device vs Returned (Chi-square)", chi2, p, dof))

    # H2: Region × DeliveryStatus
    if {"Region","DeliveryStatus"}.issubset(df.columns):
        chi2, p, dof, tab = chi_square_test(df.dropna(subset=["Region","DeliveryStatus"]), "Region", "DeliveryStatus")
        results.append(("Region vs DeliveryStatus (Chi-square)", chi2, p, dof))

    # H3: AgeGroup × Returned
    if {"AgeGroup","Returned"}.issubset(df.columns):
        chi2, p, dof, tab = chi_square_test(df.dropna(subset=["AgeGroup","Returned"]), "AgeGroup", "Returned")
        results.append(("AgeGroup vs Returned (Chi-square)", chi2, p, dof))

    # H4: Brand × Returned (restrict to top brands by count)
    if {"Brand","Returned"}.issubset(df.columns):
        top_brands = df["Brand"].value_counts().head(15).index
        sub = df[df["Brand"].isin(top_brands)]
        if len(sub) > 0:
            chi2, p, dof, tab = chi_square_test(sub.dropna(subset=["Brand","Returned"]), "Brand", "Returned")
            results.append(("Top Brands vs Returned (Chi-square)", chi2, p, dof))

    # H5: Discount impact on Quantity (simple regression)
    reg_line = ""
    if {"DiscountPercent","Quantity"}.issubset(df.columns):
        x = df["DiscountPercent"].astype(float)
        y = df["Quantity"].astype(float)
        m = sm.OLS(y.dropna(), sm.add_constant(x.dropna().loc[y.dropna().index])).fit()
        reg_line = f"Quantity ~ DiscountPercent: coef={m.params.get('DiscountPercent', float('nan')):.4f}, p={m.pvalues.get('DiscountPercent', float('nan')):.4g}"

    # Save hypothesis report
    hyp_lines = ["# 🧪 Hypothesis Testing (Auto)"]
    if results:
        for name, chi2, p, dof in results:
            decision = "Reject H0" if p < 0.05 else "Fail to reject H0"
            hyp_lines.append(f"- **{name}** → chi2={chi2:.3f}, dof={dof}, p={p:.4g} → **{decision}**")
    if corr_line:
        hyp_lines.append(f"- {corr_line}")
    if reg_line:
        hyp_lines.append(f"- {reg_line}")

    with open(os.path.join(base, "reports/hypothesis_testing.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(hyp_lines) if hyp_lines else "# 🧪 Hypothesis Testing\n(No eligible columns found.)")

    # Create insight skeleton
    with open(os.path.join(base, "reports/insight_summary.md"), "w", encoding="utf-8") as f:
        f.write("""# 🔑 Insight Summary (Top 5–8)

Fill this section using the generated plots in `visuals/plots/` and the stats in `reports/hypothesis_testing.md`.

- Example insights to consider:
  - Categories with highest **revenue** and **return rate**
  - **Device** with higher return tendency
  - **Regions** with late deliveries
  - **Discount** impact on **quantity** or **returns**
  - **Top brands** by return rate

Attach plot filenames next to each insight and add a specific recommended action.
""")

    print("Reports and scaffolding generated successfully.")

if __name__ == "__main__":
    main()
