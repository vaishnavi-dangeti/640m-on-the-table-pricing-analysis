"""
01_prepare_data.py
Builds a weekly, product-level dataset for one Walmart store (CA_1)
from the real M5 files: units sold, price, SNAP days and events.

Run from inside the 3_PYTHON folder:
    python 01_prepare_data.py

Output: ../1_DATA/weekly_sales_CA_1.csv
"""
import pandas as pd

STORE = "CA_1"
DATA = "../1_DATA/"

# ---------- 1. Calendar ----------
print("Loading calendar...")
cal = pd.read_csv(DATA + "calendar.csv")
cal["is_event"] = cal["event_name_1"].notna().astype(int)

# ---------- 2. Daily sales for one store ----------
print("Loading sales (this can take a minute)...")
sales = pd.read_csv(DATA + "sales_train_evaluation.csv")
sales = sales[sales["store_id"] == STORE].reset_index(drop=True)
day_cols = [c for c in sales.columns if c.startswith("d_")]
print(f"  {len(sales):,} products in store {STORE}, {len(day_cols):,} days")

# Week-level info from the calendar (same for every product)
cal = cal[cal["d"].isin(day_cols)]
week_info = (cal.groupby("wm_yr_wk")
                .agg(week_start=("date", "min"),
                     days=("d", "count"),
                     snap_days=("snap_CA", "sum"),
                     event_days=("is_event", "sum"))
                .reset_index())
week_info = week_info[week_info["days"] == 7]          # keep full weeks only

# ---------- 3. Daily units -> weekly units ----------
print("Summing daily sales into weeks...")
week_of_day = cal.set_index("d")["wm_yr_wk"]
units = sales[day_cols].T                                # rows = days
units.index = units.index.map(week_of_day)
units = units.groupby(level=0).sum().T                   # rows = products, cols = weeks
units.index = sales["item_id"]

weekly = units.stack().reset_index()
weekly.columns = ["item_id", "wm_yr_wk", "units"]
weekly = weekly.merge(sales[["item_id", "dept_id", "cat_id"]], on="item_id")
weekly = weekly.merge(week_info, on="wm_yr_wk", how="inner")

# ---------- 4. Prices ----------
print("Loading prices...")
prices = pd.read_csv(DATA + "sell_prices.csv")
prices = prices[prices["store_id"] == STORE].drop(columns="store_id")

# Inner join: weeks with no price mean the product was not on sale yet
weekly = weekly.merge(prices, on=["item_id", "wm_yr_wk"], how="inner")
weekly["revenue"] = weekly["units"] * weekly["sell_price"]

# Regular price = the price the product sells at most often
regular = (weekly.groupby("item_id")["sell_price"]
                 .agg(lambda s: s.mode().iloc[0])
                 .rename("regular_price"))
weekly = weekly.merge(regular, on="item_id")
weekly["discount_pct"] = ((weekly["regular_price"] - weekly["sell_price"])
                          / weekly["regular_price"] * 100).round(2)

weekly = weekly.sort_values(["item_id", "wm_yr_wk"])
weekly.to_csv(DATA + "weekly_sales_CA_1.csv", index=False)

# ---------- 5. Summary ----------
n_prices = weekly.groupby("item_id")["sell_price"].nunique()
print("\nSUMMARY")
print("-------")
print(f"Product-weeks:                    {len(weekly):,}")
print(f"Products:                         {weekly['item_id'].nunique():,}")
print(f"Weeks:                            {weekly['wm_yr_wk'].nunique()}")
print(f"Date range:                       {weekly['week_start'].min()} to {weekly['week_start'].max()}")
print(f"Total units:                      {weekly['units'].sum():,}")
print(f"Total revenue:                    ${weekly['revenue'].sum():,.0f}")
print(f"Products with 5+ distinct prices: {(n_prices >= 5).sum():,}")
print(f"Product-weeks below regular price: {(weekly['discount_pct'] > 0).mean() * 100:.1f}%")

print("\nBy category:")
print(weekly.groupby("cat_id")
            .agg(products=("item_id", "nunique"),
                 units=("units", "sum"),
                 revenue=("revenue", "sum"))
            .round(0))

print("\nSaved weekly_sales_CA_1.csv")
