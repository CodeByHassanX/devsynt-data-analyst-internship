# Project 4 — Customer Churn & Retention Analysis

Analysis of the Telco Customer Churn dataset (7,043 customers, IBM sample / BlastChar version) to
identify why customers leave, which groups are highest-risk, and what retention actions the data
supports. No machine-learning prediction model was built, per the task's instructions.

## Deliverables

| File | Maps to required deliverable |
|---|---|
| `Project4_Customer_Churn_Analysis.ipynb` | **Python Notebook** — data cleaning, churn analysis (6 breakdowns with charts + interpretation), 2 statistical tests, segmentation, revenue at risk |
| `Project4_Final_Summary.pdf` | **Short Summary** — 1 page: KPIs, statistical results, key segment, revenue at risk, 5 findings, 5 recommendations |
| `power_bi/` | **Power BI Dashboard** inputs — cleaned/segmented CSV + `POWER_BI_GUIDE.md` with KPI/visual/DAX build steps for `Project4_Churn_Dashboard.pbix` |
| `telco.csv` | Raw source dataset used by the notebook |
| `build_notebook.py` / `build_summary_pdf.py` | Scripts used to generate the notebook and PDF (kept for transparency/reproducibility) |

## Power BI note

A `.pbix` binary can't be produced outside Power BI Desktop itself (it's a Windows GUI app), so
`power_bi/POWER_BI_GUIDE.md` gives you the exact data, KPI cards, 5 visuals, slicers, and DAX
measures to build `Project4_Churn_Dashboard.pbix` in about 15 minutes.

## Headline numbers

- **Total customers:** 7,043 | **Churned:** 1,869 | **Churn rate:** 26.54%
- **Avg. monthly charges:** $64.76 overall ($74.44 churned vs. $61.27 retained)
- **Revenue at risk:** $139,130.85/month (30.5% of total monthly charges)
- **Highest-risk segment:** New customers (tenure ≤ 12 months) — 47.0% churn, $68,954/month at risk

## Data cleaning applied

`TotalCharges` was stored as text with 11 blank values, all belonging to brand-new customers with
`tenure == 0`. Converted to numeric and filled those 11 rows with 0 (not imputed — it's the correct
value for a customer who hasn't been billed yet). No duplicate rows or customer IDs were found.

## Statistical tests (α = 0.05)

- **Chi-Square (Contract vs. Churn):** χ² = 1,184.60, p ≈ 5.9e-258 → reject H0, contract type and
  churn are associated.
- **T-Test (Monthly Charges vs. Churn):** t = 18.41, p ≈ 8.6e-73 → reject H0, churned customers pay
  significantly more per month than retained customers.

## Segmentation logic

Four mutually-exclusive segments built from tenure and monthly charges (churn is used to *evaluate*
each segment's outcome, not to define it, avoiding circular 0%/100% churn rates):

1. **New** — tenure ≤ 12 months
2. **High-Value** — tenure > 12 months and MonthlyCharges ≥ $70
3. **Loyal** — tenure > 24 months and MonthlyCharges < $70
4. **Standard** — everything else
