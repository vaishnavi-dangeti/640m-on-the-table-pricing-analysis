# 💰 Dynamic Pricing: Profit Optimization

**A tool that tells a shop which prices to change, by how much, and how much extra profit it will earn.**



![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)




![MySQL](https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=white)




![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?logo=powerbi&logoColor=black)



---

## 🤔 The problem

Every shop has to decide: **what price should I put on each product?**

- Price too high → customers leave and you sell less.
- Price too low → you sell more, but leave money on the table.

Most shops just guess, or copy their competitors. With hundreds of products, guessing costs real money.

## 💡 A simple example

A shop sells a phone cover. It costs the shop **₹600** to buy, and it sells it for **₹1,000**.

| | Today | After a 5% price rise |
|---|---:|---:|
| Price | ₹1,000 | ₹1,050 |
| Covers sold per month | 100 | 95 |
| Revenue | ₹1,00,000 | ₹99,750 |
| **Profit** | **₹40,000** | **₹42,750** ✅ |

The shop sells 5 fewer covers, but earns ₹450 on each sale instead of ₹400. **Profit goes up by ₹2,750 even though revenue goes down slightly.**

The hard part is knowing *how many customers you will lose* for each product. That is what this project works out. Now imagine doing this correctly for **500 products at once**.

## ✅ What this project does

1. **Measures how sensitive customers are** to price changes, for each product separately (called *price elasticity*).
2. **Tests many possible prices** for every product, from 5% lower to 8% higher.
3. **Picks the price that earns the most profit**, while staying within safe limits: never above the product's normal price range, and never more than 10% above the competitor.

The output is a ready-to-use file, `pricing_recommendations.csv`, with a recommended price for every product.

## 📊 Result

| | |
|---|---:|
| Profit before | ₹5.32B |
| **Extra profit found** | **+₹270.4M (+5.1%)** |
| Average price change | +4.99% |
| Revenue change | −3.1% |

The charts, category breakdown and top products are in the **Power BI dashboard** (`4_DASHBOARD` folder).

## 🚀 Why it is useful

- 🎯 **Product-by-product decisions.** Some products can take a price rise and others cannot. It does not apply one rule to everything.
- 💰 **Focuses on profit, not just sales.** A high-selling product can still earn little.
- 🛡️ **Safe by design.** Prices stay close to competitors and inside historical limits.
- ⚡ **Saves time.** Instead of pricing 500 products by hand, a team gets a ready list in minutes.
- 🔁 **Works for any shop** with sales history: just replace the data files.

## 🗂️ Project structure

```
1_DATA        sales and product data + final recommendations
2_SQL         database tables and business queries (MySQL)
3_PYTHON      the 4 scripts that do the analysis (run in order 01 → 04)
4_DASHBOARD   tables used by the Power BI dashboard
```

## ▶️ How to run

```bash
pip install -r requirements.txt
cd 3_PYTHON
python 01_data_analysis.py
python 02_demand_prediction.py
python 03_price_optimization.py
python 04_dashboard_tables.py
```

New to Python? Follow [SETUP.md](SETUP.md).

## ⚠️ Limitations

- 🧪 **The data is synthetic (made up for practice)**, so the ₹270M shows what the method can do, not a real company's results.
- 🏪 **It assumes competitors do not react** to price changes and that customers respond the same way at every price.
