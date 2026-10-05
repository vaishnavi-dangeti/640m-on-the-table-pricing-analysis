import numpy as np
import pandas as pd

sales = pd.read_csv("../1_DATA/sales_data.csv")
rec = pd.read_csv("../1_DATA/pricing_recommendations.csv")
out = "../4_DASHBOARD/"

# ---------- 1. CATEGORY SUMMARY ----------
cat = rec.groupby("category").agg(
    revenue_current=("revenue_current", "sum"),
    revenue_modelled=("revenue_modelled", "sum"),
    profit_current=("profit_current", "sum"),
    profit_modelled=("profit_modelled", "sum"),
    profit_uplift=("profit_uplift", "sum"),
    avg_price_change_pct=("price_change_pct", "mean"),
    avg_elasticity=("price_elasticity", "mean")).reset_index()
cat["share_of_uplift_pct"] = cat.profit_uplift / cat.profit_uplift.sum() * 100
cat.to_csv(out + "category_summary.csv", index=False)
print("\nCATEGORY SUMMARY\n", cat.round(2))

# ---------- 2. MONTHLY TREND ----------
# each product's modelled/current ratio is applied to its monthly sales
sales["month"] = pd.to_datetime(sales["date"]).dt.month
ratio = rec[["product_id"]].copy()
ratio["rev_ratio"] = rec.revenue_modelled / rec.revenue_current
ratio["profit_ratio"] = rec.profit_modelled / rec.profit_current
m = sales.merge(ratio, on="product_id", how="left")
m["revenue_modelled"] = m.revenue * m.rev_ratio
m["profit_modelled"] = m.gross_profit * m.profit_ratio
monthly = m.groupby("month").agg(
    revenue_current=("revenue", "sum"),
    revenue_modelled=("revenue_modelled", "sum"),
    profit_current=("gross_profit", "sum"),
    profit_modelled=("profit_modelled", "sum")).reset_index()
monthly["profit_uplift"] = monthly.profit_modelled - monthly.profit_current
monthly.to_csv(out + "monthly_trend.csv", index=False)
print("\nMONTHLY TREND\n", monthly.round(0))

# ---------- 3. COMPETITIVE POSITION ----------
gap = rec.current_price / rec.competitor_price - 1
pos = np.where(gap < -0.01, "Priced below competitors",
      np.where(gap > 0.01, "Higher than competitors", "Same price"))
comp = (pd.Series(pos).value_counts(normalize=True) * 100).round(2)
comp = comp.reset_index()
comp.columns = ["position", "pct"]
comp.to_csv(out + "competitive_position.csv", index=False)
print("\nCOMPETITIVE POSITION\n", comp)

# ---------- 4. TOP 10 ----------
top = rec.sort_values("profit_uplift", ascending=False).head(10)[
    ["product_id", "category", "current_price", "competitor_price",
     "price_elasticity", "recommended_price", "price_change_pct",
     "volume_change_pct", "profit_uplift"]]
top.to_csv(out + "top10_products.csv", index=False)
print("\nTOP 10\n", top.round(2))

# ---------- 5. HEADLINE NUMBERS ----------
print("\nHEADLINE")
print("Profit uplift:", round(rec.profit_uplift.sum()))
print("Revenue uplift:", round(rec.revenue_uplift.sum()))
print("Avg price change %:", round(rec.price_change_pct.mean(), 2))
