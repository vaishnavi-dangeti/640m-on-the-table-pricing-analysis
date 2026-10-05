# ============================================================
# DYNAMIC PRICING & PROFIT OPTIMIZATION ENGINE
# 01 - BASIC DATA ANALYSIS (synthetic dataset)
# ============================================================

import pandas as pd

# ---------- 1. LOAD DATA ----------
sales = pd.read_csv("../1_DATA/sales_data.csv")
products = pd.read_csv("../1_DATA/products.csv")
competitors = pd.read_csv("../1_DATA/competitor_prices.csv")
inventory = pd.read_csv("../1_DATA/inventory.csv")

print("Data loaded successfully!")

# ---------- 2. DATA CHECK ----------
print("\nDataset sizes (rows, columns)")
print("Sales:      ", sales.shape)
print("Products:   ", products.shape)
print("Competitors:", competitors.shape)
print("Inventory:  ", inventory.shape)

print("\nMissing values in sales data:")
print(sales.isnull().sum())

# ---------- 3. BUSINESS SUMMARY ----------
total_revenue = sales["revenue"].sum()
total_profit = sales["gross_profit"].sum()
total_units = sales["quantity_sold"].sum()

print("\nBusiness summary")
print("----------------")
print("Total revenue:     ", round(total_revenue, 2))
print("Total gross profit:", round(total_profit, 2))
print("Gross margin %:    ", round(total_profit / total_revenue * 100, 2))
print("Total units sold:  ", total_units)

# ---------- 4. CATEGORY PERFORMANCE ----------
category_summary = (
    sales.groupby("category")
    .agg(revenue=("revenue", "sum"),
         profit=("gross_profit", "sum"),
         units_sold=("quantity_sold", "sum"))
    .sort_values("revenue", ascending=False)
)
category_summary["margin_pct"] = (
    category_summary.profit / category_summary.revenue * 100
)

print("\nCategory performance:")
print(category_summary.round(2))

# ---------- 5. TOP 10 PRODUCTS BY CURRENT PROFIT ----------
top_products = (
    sales.groupby("product_id")
    .agg(revenue=("revenue", "sum"),
         profit=("gross_profit", "sum"),
         units_sold=("quantity_sold", "sum"))
    .sort_values("profit", ascending=False)
    .head(10)
)

print("\nTop 10 products by current gross profit:")
print(top_products.round(2))

# ---------- 6. PRICE VS COMPETITORS ----------
sales["price_gap_pct"] = (
    sales["unit_price"] / sales["competitor_price"] - 1
) * 100

print("\nAverage price gap vs competitor (%):",
      round(sales["price_gap_pct"].mean(), 2))
print("Share of sales priced below competitor (%):",
      round((sales["price_gap_pct"] < 0).mean() * 100, 2))

# ---------- 7. SAVE ----------
category_summary.to_csv("../1_DATA/sales_category_summary.csv")
top_products.to_csv("../1_DATA/sales_top_products.csv")

print("\nAnalysis completed successfully!")
