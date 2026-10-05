# ============================================================
# DYNAMIC PRICING & PROFIT OPTIMIZATION ENGINE
# 02 - DEMAND PREDICTION (EXPLORATORY)
#
# Purpose: test how well a Random Forest predicts units sold,
# and which features matter most.
#
# Note: final price recommendations do NOT use this model.
# Tree models are step-like in price and understate demand
# loss when prices rise, so 03_price_optimization.py uses
# per-product log-log elasticity instead.
# ============================================================

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# ---------- 1. LOAD DATA ----------
sales = pd.read_csv("../1_DATA/sales_data.csv")
print("Sales data loaded successfully!")

# ---------- 2. BUILD FEATURES ----------
sales["month"] = pd.to_datetime(sales["date"]).dt.month
sales["price_ratio"] = sales["unit_price"] / sales["competitor_price"]

features = ["unit_price", "competitor_price", "price_ratio",
            "promotion_flag", "month"]

X = pd.get_dummies(sales[features + ["category"]], columns=["category"])
y = sales["quantity_sold"]

# ---------- 3. SPLIT DATA ----------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------- 4. TRAIN MODEL ----------
model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# ---------- 5. EVALUATE ----------
pred = model.predict(X_test)
print("\nDemand prediction results")
print("-------------------------")
print("MAE:", round(mean_absolute_error(y_test, pred), 2))
print("R2: ", round(r2_score(y_test, pred), 2))

# ---------- 6. FEATURE IMPORTANCE ----------
importance = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_
}).sort_values("importance", ascending=False)

print("\nFeature importance:")
print(importance.head(10))

# ---------- 7. WHY THIS MODEL IS NOT USED FOR PRICING ----------
# Raise price on a typical row and watch predicted demand.
# Tree models often show flat, step-like responses.
row = X.median().to_frame().T
print("\nPredicted units at different prices (typical product):")
for change in [-0.10, -0.05, 0, 0.05, 0.10]:
    r = row.copy()
    r["unit_price"] = row["unit_price"] * (1 + change)
    r["price_ratio"] = r["unit_price"] / r["competitor_price"]
    print(f"  price {change:+.0%}: {model.predict(r)[0]:.2f} units")

# ---------- 8. SAVE ----------
importance.to_csv("../1_DATA/demand_feature_importance.csv", index=False)
print("\nDemand prediction completed successfully!")
