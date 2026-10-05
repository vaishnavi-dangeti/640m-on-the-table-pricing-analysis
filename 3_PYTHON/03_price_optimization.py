import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# ---------- 1. LOAD DATA ----------
sales = pd.read_csv("../1_DATA/sales_data.csv")
products = pd.read_csv("../1_DATA/products.csv")

sales = sales[(sales.quantity_sold > 0) & (sales.unit_price > 0)].copy()
sales["unit_cost"] = sales.unit_price - sales.gross_profit / sales.quantity_sold

# ---------- 2. ELASTICITY PER PRODUCT (log-log) ----------
rows = []
for pid, g in sales.groupby("product_id"):
    e = np.nan
    if len(g) >= 30 and g.unit_price.nunique() >= 10:
        m = smf.ols("np.log(quantity_sold) ~ np.log(unit_price)"
                    " + promotion_flag", data=g).fit()
        e = m.params["np.log(unit_price)"]
    rows.append((pid, e))
el = pd.DataFrame(rows, columns=["product_id", "raw_elasticity"])
el = el.merge(sales[["product_id", "category"]].drop_duplicates(),
              on="product_id")

# unreliable values fall back to the category median, then to -1.5
cat_med = el.groupby("category").raw_elasticity.transform("median")
el["price_elasticity"] = el.raw_elasticity.where(
    el.raw_elasticity.between(-5, -0.2), cat_med)
el["price_elasticity"] = el.price_elasticity.fillna(-1.5)

# ---------- 3. PRODUCT SUMMARY ----------
s = (sales.groupby("product_id")
     .agg(current_price=("unit_price", "mean"),
          competitor_price=("competitor_price", "mean"),
          unit_cost=("unit_cost", "median"),
          units_sold=("quantity_sold", "sum"))
     .reset_index()
     .merge(products[["product_id", "product_name", "min_price", "max_price"]],
            on="product_id", how="left")
     .merge(el[["product_id", "category", "price_elasticity"]],
            on="product_id"))

# ---------- 4. TEST PRICES, KEEP THE MOST PROFITABLE ----------
def optimise(r):
    p0, c, e, q0 = r.current_price, r.unit_cost, r.price_elasticity, r.units_sold
    base_profit = (p0 - c) * q0
    best_p, best_profit = p0, base_profit
    for ch in np.arange(-0.05, 0.0801, 0.005):
        p = p0 * (1 + ch)
        p = min(max(p, r.min_price), r.max_price)
        p = min(p, r.competitor_price * 1.10)       # guardrail
        profit = (p - c) * q0 * (p / p0) ** e
        if profit > best_profit:
            best_p, best_profit = p, profit
    q1 = q0 * (best_p / p0) ** e
    return pd.Series({
        "recommended_price": round(best_p, 2),
        "volume_change_pct": (q1 / q0 - 1) * 100,
        "revenue_current": p0 * q0,
        "revenue_modelled": best_p * q1,
        "revenue_uplift": best_p * q1 - p0 * q0,
        "profit_current": base_profit,
        "profit_modelled": best_profit,
        "profit_uplift": best_profit - base_profit})

s = s.join(s.apply(optimise, axis=1))
s["price_change_pct"] = (s.recommended_price / s.current_price - 1) * 100
s = s.sort_values("profit_uplift", ascending=False)

# ---------- 5. PRINT AND SAVE ----------
print(s[["product_id", "price_elasticity", "price_change_pct",
         "volume_change_pct", "profit_uplift"]].head(10))
print("Elasticity range:", s.price_elasticity.min(), s.price_elasticity.max())
print("Avg price change %:", s.price_change_pct.mean())
print("Total profit uplift:", s.profit_uplift.sum())
print("Total revenue uplift:", s.revenue_uplift.sum())

s.to_csv("../1_DATA/pricing_recommendations.csv", index=False)
print("Saved pricing_recommendations.csv")
