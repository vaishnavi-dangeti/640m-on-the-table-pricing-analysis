"""
03_discount_profit.py
How much profit did Walmart's real discounts earn or lose in store CA_1?

For every real discount week, compare the profit at the discount price with the
estimated profit if the product had stayed at its normal price, using each
department's elasticity from 02. Cost is not in the data, so three margins are tested.

Run from 3_PYTHON:  python 03_discount_profit.py
Output: ../1_DATA/discount_profit_by_dept.csv
"""
import numpy as np
import pandas as pd

DATA = "../1_DATA/"
MARGINS = [0.25, 0.35, 0.45]

print("Loading data...")
df = pd.read_csv(DATA + "weekly_sales_CA_1.csv")
df = df.sort_values(["item_id", "wm_yr_wk"])
df["ref_price"] = (df.groupby("item_id")["sell_price"]
                     .transform(lambda p: p.rolling(9, min_periods=1).max()))
df["rel_price"] = df["sell_price"] / df["ref_price"]

el = pd.read_csv(DATA + "dept_elasticity.csv")
el["reliable"] = (el["p_value"] < 0.05) & (el["elasticity"] < 0)
print("Departments with a reliable price effect:", ", ".join(el.loc[el["reliable"], "dept_id"]))
print("Other departments: no measurable effect, so their discounts are assumed to add no units.\n")

d = df[df["rel_price"] < 0.97].merge(el[["dept_id", "elasticity", "reliable"]], on="dept_id")
d["e_used"] = np.where(d["reliable"], d["elasticity"], 0.0)

# Estimated units if the product had stayed at its normal price
d["units_normal"] = d["units"] * d["rel_price"] ** (-d["e_used"])
d["rev_disc"] = d["units"] * d["sell_price"]
d["rev_normal"] = d["units_normal"] * d["ref_price"]

rows = []
for dept, g in d.groupby("dept_id"):
    row = {"dept_id": dept,
           "discount_weeks": len(g),
           "avg_discount_pct": round((1 - g["rel_price"]).mean() * 100, 1),
           "elasticity_used": round(g["e_used"].iloc[0], 2),
           "extra_units_pct": round((g["units"].sum() / g["units_normal"].sum() - 1) * 100, 1),
           "revenue_change": round(g["rev_disc"].sum() - g["rev_normal"].sum()),
           "share_in_snap_weeks_pct": round((g["snap_days"] >= 5).mean() * 100, 1)}
    for m in MARGINS:
        cost = g["ref_price"] * (1 - m)
        profit_disc = ((g["sell_price"] - cost) * g["units"]).sum()
        profit_norm = ((g["ref_price"] - cost) * g["units_normal"]).sum()
        row[f"profit_change_{int(m * 100)}pct_margin"] = round(profit_disc - profit_norm)
    rows.append(row)

r = pd.DataFrame(rows)
r.to_csv(DATA + "discount_profit_by_dept.csv", index=False)

pd.set_option("display.width", 200)
print("WHAT THE DISCOUNTS DID (store CA_1, Jan 2011 - May 2016)")
print("---------------------------------------------------------")
print(r.to_string(index=False))

print("\nTOTAL ACROSS ALL DEPARTMENTS")
print(f"Discount weeks:            {r['discount_weeks'].sum():,}")
print(f"Revenue change:            ${r['revenue_change'].sum():,.0f}")
for m in MARGINS:
    col = f"profit_change_{int(m * 100)}pct_margin"
    print(f"Profit change at {int(m * 100)}% margin: ${r[col].sum():,.0f}")

print("\nBREAK-EVEN: how price-sensitive customers must be for a 10% discount to pay for itself")
for m in MARGINS:
    be = np.log(m / (m - 0.10)) / np.log(0.90)
    print(f"  at {int(m * 100)}% margin: elasticity of {be:.2f} or stronger")
print(f"  Measured in Walmart FOODS: about {el.loc[el['dept_id'].str.startswith('FOODS'), 'elasticity'].median():.2f}")

print("\nSNAP EFFECT: extra sales in a full SNAP week (7 benefit days), no discount needed")
el["full_snap_week_lift_pct"] = ((1 + el["snap_effect_pct"] / 100) ** 7 - 1) * 100
print(el[["dept_id", "full_snap_week_lift_pct"]].round(1).to_string(index=False))

print("\nSaved discount_profit_by_dept.csv")
