"""
04_dashboard_tables.py
Builds small, clean tables for the Power BI dashboard.

Run from 3_PYTHON:  python 04_dashboard_tables.py
Output folder: ../4_DASHBOARD/
"""
import os
import numpy as np
import pandas as pd

DATA = "../1_DATA/"
OUT = "../4_DASHBOARD/"
os.makedirs(OUT, exist_ok=True)

print("Loading data...")
w = pd.read_csv(DATA + "weekly_sales_CA_1.csv")
w = w.sort_values(["item_id", "wm_yr_wk"])
w["ref_price"] = (w.groupby("item_id")["sell_price"]
                    .transform(lambda p: p.rolling(9, min_periods=1).max()))
w["is_discount"] = (w["sell_price"] / w["ref_price"] < 0.97).astype(int)

el = pd.read_csv(DATA + "dept_elasticity.csv")
dp = pd.read_csv(DATA + "discount_profit_by_dept.csv")

# 1. Weekly trend by category
trend = (w.groupby(["week_start", "cat_id"])
           .agg(units=("units", "sum"),
                revenue=("revenue", "sum"),
                snap_days=("snap_days", "first"),
                discount_share_pct=("is_discount", "mean"))
           .reset_index())
trend["discount_share_pct"] = (trend["discount_share_pct"] * 100).round(2)
trend["revenue"] = trend["revenue"].round(2)
trend.to_csv(OUT + "weekly_trend.csv", index=False)

# 2. Department elasticity + discount vs SNAP comparison
el["category"] = el["dept_id"].str.rsplit("_", n=1).str[0]
el["reliable_price_effect"] = np.where((el["p_value"] < 0.05) & (el["elasticity"] < 0), "Yes", "No")
el["full_snap_week_lift_pct"] = (((1 + el["snap_effect_pct"] / 100) ** 7 - 1) * 100).round(1)
el.to_csv(OUT + "dept_elasticity.csv", index=False)

# 3. Profit change by department and margin (long format for a slicer)
pcols = [c for c in dp.columns if c.startswith("profit_change_")]
long = dp.melt(id_vars=["dept_id", "discount_weeks", "avg_discount_pct",
                        "extra_units_pct", "revenue_change"],
               value_vars=pcols, var_name="margin_pct", value_name="profit_change")
long["margin_pct"] = long["margin_pct"].str.extract(r"(\d+)")[0].astype(int)
long["category"] = long["dept_id"].str.rsplit("_", n=1).str[0]
long.to_csv(OUT + "discount_profit.csv", index=False)

# 4. Break-even elasticity vs measured
foods_e = el.loc[el["category"] == "FOODS", "elasticity"].median()
be = pd.DataFrame({"margin_pct": [25, 35, 45]})
be["breakeven_elasticity"] = (np.log((be["margin_pct"] / 100) / (be["margin_pct"] / 100 - 0.10))
                              / np.log(0.90)).round(2)
be["measured_foods_elasticity"] = round(foods_e, 2)
be["times_short"] = (be["breakeven_elasticity"] / be["measured_foods_elasticity"]).round(1)
be.to_csv(OUT + "breakeven.csv", index=False)

# 5. KPI cards
food_snap = el.loc[el["category"] == "FOODS", "full_snap_week_lift_pct"]
kpi = pd.DataFrame([{
    "total_revenue": round(w["revenue"].sum()),
    "total_units": int(w["units"].sum()),
    "products": w["item_id"].nunique(),
    "weeks": w["wm_yr_wk"].nunique(),
    "start_date": w["week_start"].min(),
    "end_date": w["week_start"].max(),
    "discount_weeks": int(dp["discount_weeks"].sum()),
    "profit_change_25": int(dp["profit_change_25pct_margin"].sum()),
    "profit_change_35": int(dp["profit_change_35pct_margin"].sum()),
    "profit_change_45": int(dp["profit_change_45pct_margin"].sum()),
    "revenue_change": int(dp["revenue_change"].sum()),
    "foods_elasticity": round(foods_e, 2),
    "foods_snap_week_lift_max": food_snap.max(),
}])
kpi.to_csv(OUT + "kpis.csv", index=False)

print("\nSaved to 4_DASHBOARD:")
for f in ["kpis.csv", "discount_profit.csv", "breakeven.csv",
          "dept_elasticity.csv", "weekly_trend.csv"]:
    print(f"  {f:22s} {len(pd.read_csv(OUT + f)):>6,} rows")
print("\nKPIs:")
print(kpi.T.to_string(header=False))
