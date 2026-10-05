# 💰 Dynamic Pricing: Profit Optimization

**A data-driven pricing system that recommends the best price for each product in an online retail catalog, to maximize gross profit.**



![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)




![MySQL](https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=white)




![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?logo=powerbi&logoColor=black)



---

## 🎯 The Business Problem

An online retailer sells hundreds of products across categories such as Electronics, Fashion and Home & Kitchen. For each product, someone has to decide the price. This is hard because:

- **Raise the price too much** and customers buy less or switch to a competitor.
- **Keep it too low** and the business earns less than it could on every sale.
- Different products react differently. A small price rise may barely affect one product and hurt another badly.

In practice, prices are often set by habit or by copying competitors. Across a large catalog, that leaves money on the table.

## ✅ The Solution

This project analyses historical sales to answer three questions for **each of the 500 products**:

1. **How sensitive are customers to this product's price?** (called *price elasticity*)
2. **What would happen to sales and profit at different prices?**
3. **Which price earns the highest profit, while staying safe?**

The result is a ready-to-use price list (`pricing_recommendations.csv`) and a Power BI dashboard.

## 💡 Example From the Results

**Product P0251 (Home & Kitchen)**

| | Current | Recommended |
|---|---:|---:|
| Price | ₹21,106 | ₹22,794 (+8%) |
| Competitor price | ₹22,679 | |
| Expected sales volume | | −7.3% |
| **Extra profit for this product** | | **+₹3.84M** |

**Why this works:** the product is currently priced about 7% *below* its competitor. The model finds that customers would only buy about 7% fewer units after a price rise, but each unit now earns noticeably more. The new price stays within 1% of the competitor, so the product remains competitive.

The model makes this kind of decision for every product, not just one.

## 📊 Overall Impact

| Metric | Value |
|---|---:|
| Gross profit before | ₹5.32B |
| **Extra gross profit found** | **+₹270.4M (+5.1%)** |
| Average recommended price change | +4.99% |
| Revenue change | −3.1% |

**Note:** revenue goes slightly down but profit goes up. Selling a bit less at a better margin earns more than selling more at a thin margin. That is why the project optimizes **profit, not revenue**.

📈 Category breakdown, top products and trends are in the **Power BI dashboard** (`4_DASHBOARD` folder).

## 🛠️ How It Works

1. **Measure price sensitivity:** a regression model is fitted to each product's own sales history.
2. **Calculate cost:** unit cost is derived from the sales data, so profit can be measured.
3. **Test prices:** every price from 5% below to 8% above the current price is tested.
4. **Choose the best price:** the highest-profit option wins, within safe limits. It stays inside the product's historical price range and never exceeds 110% of the competitor price.

## 🗂️ Project Structure

```
1_DATA        sales and product data, plus the final recommendations
2_SQL         database tables and business queries (MySQL)
3_PYTHON      analysis scripts, run in order 01 → 04
4_DASHBOARD   tables used by the Power BI dashboard
```

## ▶️ How to Run

```bash
pip install -r requirements.txt
cd 3_PYTHON
python 01_data_analysis.py
python 02_demand_prediction.py
python 03_price_optimization.py
python 04_dashboard_tables.py
```

New to Python? Follow the steps in [SETUP.md](SETUP.md).

## ⚠️ Limitations

- 🧪 **The data is synthetic (generated for practice)**, so the ₹270M shows what the method can achieve, not a real company's results.
- 🏪 **Competitors are assumed not to react** to price changes, and customer sensitivity is assumed to stay constant across prices.
