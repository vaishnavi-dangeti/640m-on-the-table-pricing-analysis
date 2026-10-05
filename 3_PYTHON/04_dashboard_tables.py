# AI-POWERED DYNAMIC PRICING & REVENUE OPTIMIZATION ENGINE
# PRICE ELASTICITY ANALYSIS

import pandas as pd
import numpy as np

# ---------------------------------------------------------
# 1. LOAD SALES DATA
# ---------------------------------------------------------

sales = pd.read_csv("../1_DATA/sales_data.csv")

print("Sales data loaded successfully")
print("Rows:", len(sales))


# ---------------------------------------------------------
# 2. PREPARE DATA
# ---------------------------------------------------------

sales["date"] = pd.to_datetime(sales["date"])

# Sort by product and date
sales = sales.sort_values(["product_id", "date"])

# Create price and demand changes
sales["price_change_pct"] = (
    sales.groupby("product_id")["unit_price"]
    .pct_change()
)

sales["demand_change_pct"] = (
    sales.groupby("product_id")["quantity_sold"]
    .pct_change()
)


# ---------------------------------------------------------
# 3. CALCULATE PRICE ELASTICITY
# ---------------------------------------------------------

sales["price_elasticity"] = (
    sales["demand_change_pct"] /
    sales["price_change_pct"]
)

# Remove infinite values
sales["price_elasticity"] = sales["price_elasticity"].replace(
    [np.inf, -np.inf],
    np.nan
)


# ---------------------------------------------------------
# 4. PRODUCT-LEVEL ELASTICITY
# ---------------------------------------------------------

elasticity = (
    sales.groupby("product_id")["price_elasticity"]
    .median()
    .reset_index()
)

elasticity.columns = [
    "product_id",
    "price_elasticity"
]


# ---------------------------------------------------------
# 5. CLASSIFY PRODUCTS
# ---------------------------------------------------------

def classify_elasticity(value):

    if pd.isna(value):
        return "Insufficient Data"

    if value < -1:
        return "Elastic"

    elif value > -1:
        return "Inelastic"

    else:
        return "Unit Elastic"


elasticity["elasticity_type"] = (
    elasticity["price_elasticity"]
    .apply(classify_elasticity)
)


# ---------------------------------------------------------
# 6. DISPLAY RESULTS
# ---------------------------------------------------------

print("\nPrice Elasticity Results")
print("--------------------------------")

print(elasticity.head(10))


# ---------------------------------------------------------
# 7. SUMMARY
# ---------------------------------------------------------

print("\nElasticity Classification")
print("--------------------------------")

print(
    elasticity["elasticity_type"]
    .value_counts()
)


# ---------------------------------------------------------
# 8. SAVE RESULTS
# ---------------------------------------------------------

elasticity.to_csv(
    "../4_DASHBOARD/price_elasticity.csv",
    index=False
)

print("\nPrice elasticity analysis completed successfully.")
print("Results saved to 4_DASHBOARD/price_elasticity.csv")
