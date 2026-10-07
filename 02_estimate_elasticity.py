"""
02_estimate_elasticity.py  (v3: department level)
Estimates how sales react to short-term price changes, pooling products
within each Walmart department, and validates on the last 52 weeks.

History:
  v1 per product, raw price      -> failed: inflation confused with price (564% error)
  v2 per product, relative price -> no explosion, but too noisy per product
  v3 per department, relative price, product fixed effects (this file)

Run from 3_PYTHON:  python 02_estimate_elasticity.py
Output: ../1_DATA/dept_elasticity.csv
"""
import warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm

warnings.filterwarnings("ignore")
DATA = "../1_DATA/"

print("Loading weekly data...")
df = pd.read_csv(DATA + "weekly_sales_CA_1.csv", parse_dates=["week_start"])
df = df.sort_values(["item_id", "week_start"])

# Normal price = highest price in the last 8 weeks (including this week)
df["ref_price"] = (df.groupby("item_id")["sell_price"]
                     .transform(lambda p: p.rolling(9, min_periods=1).max()))
df["rel_price"] = df["sell_price"] / df["ref_price"]          # 1.0 = normal, 0.9 = 10% off
df["is_discount"] = (df["rel_price"] < 0.97).astype(int)

df = df[df["units"] > 0].copy()
df = df[df.groupby("item_id")["units"].transform("size") >= 52].copy()   # 1+ year of sales
df["log_q"] = np.log(df["units"])
df["log_rel"] = np.log(df["rel_price"])
df["t"] = (df["week_start"] - df["week_start"].min()).dt.days / 365.25
months = pd.get_dummies(df["week_start"].dt.month, prefix="m",
                        drop_first=True, dtype=float)
df = pd.concat([df, months], axis=1)

CTRL = ["snap_days", "event_days", "t"] + list(months.columns)
X_PRICE = ["log_rel"] + CTRL
X_BASE = CTRL
cutoff = df["week_start"].max() - pd.Timedelta(weeks=52)


def fit_fe(data, xcols):
    """OLS with a separate sales level per product (product fixed effects)."""
    cols = ["log_q"] + xcols
    means = data.groupby("item_id")[cols].mean()
    dm = data[cols] - means.loc[data["item_id"]].values
    groups = data["item_id"].astype("category").cat.codes.values
    model = sm.OLS(dm["log_q"], dm[xcols]).fit(cov_type="cluster",
                                                cov_kwds={"groups": groups})
    return model, means


def predict_fe(model, means, data, xcols):
    m = means.reindex(data["item_id"].values)
    adj = (data[xcols].values - m[xcols].values) @ model.params[xcols].values
    return np.exp(m["log_q"].values + adj)


def wape(a, p):
    return (a - p).abs().sum() / a.sum() * 100


results, val = [], []
print("Fitting one model per department...")
for dept, g in df.groupby("dept_id"):
    full, _ = fit_fe(g, X_PRICE)
    el, se = full.params["log_rel"], full.bse["log_rel"]

    train, test = g[g["week_start"] < cutoff], g[g["week_start"] >= cutoff]
    m_p, means_p = fit_fe(train, X_PRICE)
    m_b, means_b = fit_fe(train, X_BASE)
    tt = test.copy()
    tt["pred_with_price"] = predict_fe(m_p, means_p, tt, X_PRICE)
    tt["pred_without_price"] = predict_fe(m_b, means_b, tt, X_BASE)
    tt = tt.dropna(subset=["pred_with_price", "pred_without_price"])
    val.append(tt[["dept_id", "units", "is_discount",
                   "pred_with_price", "pred_without_price"]])
    d = tt[tt["is_discount"] == 1]

    results.append({
        "dept_id": dept,
        "products": g["item_id"].nunique(),
        "discount_weeks": int(g["is_discount"].sum()),
        "elasticity": round(el, 2),
        "ci_low": round(el - 1.96 * se, 2),
        "ci_high": round(el + 1.96 * se, 2),
        "p_value": round(full.pvalues["log_rel"], 4),
        "lift_10pct_cut": round((0.9 ** el - 1) * 100, 1),
        "snap_effect_pct": round((np.exp(full.params["snap_days"]) - 1) * 100, 2),
        "err_disc_with": round(wape(d["units"], d["pred_with_price"]), 1),
        "err_disc_without": round(wape(d["units"], d["pred_without_price"]), 1),
    })

r = pd.DataFrame(results)
r.to_csv(DATA + "dept_elasticity.csv", index=False)

pd.set_option("display.width", 200)
print("\nDEPARTMENT ELASTICITY")
print("---------------------")
print(r[["dept_id", "products", "discount_weeks", "elasticity",
         "ci_low", "ci_high", "p_value", "lift_10pct_cut", "snap_effect_pct"]].to_string(index=False))

v = pd.concat(val)
disc = v[v["is_discount"] == 1]
print("\nVALIDATION ON THE LAST 52 WEEKS (never seen by the model)")
print("---------------------------------------------------------")
print(f"Error, all weeks      - with price:    {wape(v['units'], v['pred_with_price']):.1f}%")
print(f"                      - without price: {wape(v['units'], v['pred_without_price']):.1f}%")
print(f"Error, discount weeks ({len(disc):,} weeks)")
print(f"                      - with price:    {wape(disc['units'], disc['pred_with_price']):.1f}%")
print(f"                      - without price: {wape(disc['units'], disc['pred_without_price']):.1f}%")
print("\nBy department, discount weeks only (lower is better):")
print(r[["dept_id", "err_disc_with", "err_disc_without"]].to_string(index=False))

print("\nSaved dept_elasticity.csv")
