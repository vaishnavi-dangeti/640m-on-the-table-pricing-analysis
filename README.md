# 💰 Dynamic Pricing: Profit Optimization

**Which product prices should change, by how much, and what does it earn?**



![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)




![MySQL](https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=white)




![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?logo=powerbi&logoColor=black)




![Data](https://img.shields.io/badge/data-synthetic-lightgrey)



---

## 🎯 Problem
A retailer sets prices by habit. This project finds the price for each of **500 products** that **maximizes gross profit**, using each product's own price sensitivity (elasticity).

## 📊 Result

| Metric | Value |
|---|---:|
| Baseline gross profit | ₹5.32B |
| **Profit uplift** | **+₹270.4M (+5.1%)** |
| Revenue change | −₹458.8M (−3.1%) |
| Avg price change | +4.99% |

💡 **Why profit rises while revenue falls:** most products are price-elastic, but current margins (36%) are below the profit-maximizing level. A small price rise loses some sales but earns more on every unit sold.

📈 Full charts, category breakdown and top products are in the **Power BI dashboard** (`4_DASHBOARD`).

## 🧠 Method
1. **Elasticity:** for each product, fit `ln(quantity) = a + b·ln(price) + c·promo`. The coefficient `b` is the elasticity.
2. **Cost:** `unit cost = gross profit ÷ quantity sold`.
3. **Search:** test price changes from −5% to +8% in 0.5% steps and keep the one with the highest profit.
4. **Guardrails:** stay within the product's historical price range and never above 110% of the competitor price.

**Example (illustrative):** cost ₹100, price ₹150, 100 units, elasticity −2.
A 5% price rise gives price ₹157.5 and 90.7 units. Revenue falls from ₹15,000 to ₹14,285, but profit rises from ₹5,000 to ₹5,215.

## 🌲 Why not use the Random Forest for pricing?
I trained one (R² ≈ 0.69) but kept it out of the pricing step. When price rose from +5% to +10%, it predicted demand going **up** (10.3 → 11.2 units), which is not realistic. Per-product elasticity gives a smooth, explainable demand curve, so it is used for pricing and the forest is exploratory only.

## 🗂️ Structure
```
1_DATA        source CSVs + pricing_recommendations.csv (final output)
2_SQL         schema and business analysis queries (MySQL)
3_PYTHON      01 explore → 02 demand model → 03 optimize → 04 dashboard tables
4_DASHBOARD   tables used by Power BI
```

## 🚀 Run it
```bash
pip install -r requirements.txt
cd 3_PYTHON
python 01_data_analysis.py
python 02_demand_prediction.py
python 03_price_optimization.py
python 04_dashboard_tables.py
```
Step-by-step guide for beginners: [SETUP.md](SETUP.md)

## ⚠️ Limitations
- 🧪 **Data is synthetic**, so the ₹270M is a simulation of the method, not a real forecast.
- 📐 Elasticity is assumed constant across prices.
- 🧱 The top products hit the +8% price cap, so their true optimum may be higher.
- 🏪 Competitor reactions and inventory limits are not modelled.

## 🔄 Version note
An earlier version claimed "₹640M revenue uplift". It was flawed: the recommended price just copied the competitor's price, and elasticity was calculated incorrectly. I rebuilt it to optimize profit with proper elasticity, which is why the headline is smaller and more honest.
