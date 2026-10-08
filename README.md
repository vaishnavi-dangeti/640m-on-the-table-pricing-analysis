# 🏷️ Do Discounts Pay?

**More sales ≠ more profit.**

 I analyzed **14,016 real discount weeks** from a Walmart store to answer one question:
> **Are discounts actually paying for themselves?**



![Python](https://img.shields.io/badge/Python-pandas%20%7C%20statsmodels-3776AB?logo=python&logoColor=white)




![Power BI](https://img.shields.io/badge/Power%20BI-dashboard-F2C811?logo=powerbi&logoColor=black)




![Data](https://img.shields.io/badge/Real%20Walmart%20Sales-2ea44f)



<!-- 

![Dashboard](4_DASHBOARD/dashboard.png)

 -->

---

## 🚨 The answer surprised me

Across 14,016 discount weeks, discounts produced an estimated:

### −$69.6K in profit*

And the bigger surprise? **Customers weren't very price-sensitive.**

A 10% food discount was associated with only about **6–7% more units sold**.

Meanwhile, in full SNAP benefit weeks, sales in two major food departments jumped **without any discount**:

| Department | Sales lift |
|---|---:|
| FOODS_2 | **+18.6%** |
| FOODS_3 | **+13.5%** |
| FOODS_1 | +0.8% |

<sub>*Based on a 35% assumed margin; sensitivity-tested at 25% (−$73.8K) and 45% (−$65.4K).</sub>

---

## 💡 The business insight

Retailers often celebrate a promotion because units sold go up. But the real question is:

> **Did the extra sales generate enough profit to cover the discount?**

For this store, discounting wasn't the best way to create demand. **Timing mattered.**

---

## 📊 What I found

| Question | Finding |
|---|---|
| Do food shoppers respond strongly to discounts? | No: elasticity ≈ **−0.59** |
| What does a 10% discount generate? | About **6–7% more units** |
| How far from breaking even? | Food shoppers would need to be **4–8× more price-sensitive** for a 10% discount to pay off |
| Did Hobbies & Household show meaningful lift? | **No measurable lift** |
| What happens in full SNAP benefit weeks? | **+13.5% to +18.6%** sales in FOODS_2 and FOODS_3 |
| How large was the discount impact? | **−$69.6K** profit |

---

## 🎯 What I'd tell the business

**01 — Rethink routine food discounts**
If a 10% discount generates only 6–7% more units, the margin given away outweighs the extra demand.

**02 — Stop treating every high-sales week the same**
SNAP benefit weeks already generate strong demand in major food departments. Test moving some promotions to pre-benefit or lower-demand weeks instead.

**03 — Test before discounting**
For Hobbies and Household, the analysis found no measurable sales lift. Don't discount first and ask questions later.

---

## 🔬 How I analyzed it

```
5.9M daily sales records
        ↓
683K product-week observations
        ↓
14,016 discount weeks identified
        ↓
Department-level price elasticity
        ↓
Normal-price comparison for every discount week
        ↓
Profit impact + business recommendations
```

Discounts were identified when weekly prices were at least 3% below the product's recent 8-week price baseline. Regression models controlled for SNAP timing, events, seasonality and trends.

---

## 🧠 One important lesson

My first model produced a **564% error** on unseen weeks.

The problem? It was confusing long-term price increases with short-term price effects.

I rebuilt the analysis around recent product-level price changes and department-level estimation, which produced a much more stable estimate of price sensitivity.

**The model didn't just give me an answer: debugging it changed the answer.**

---

## 📈 Dashboard

The Power BI dashboard turns the analysis into a business decision tool:

**Discount impact → Price sensitivity → SNAP effect → Profit impact → Recommendations**

## 📊 Power BI Dashboard

[🔗 View the Power BI Dashboard](https://github.com/vaishnavi-dangeti/Do-Discounts-Pay/blob/main/4_DASHBOARD/MY%20PORTFOLIO%20PROJECT.pbix)

Download the `.pbix` file and open it in Power BI Desktop to explore the dashboard yourself.

<!-- 

![Dashboard](4_DASHBOARD/dashboard.png)

 -->

---

## 🛠️ Built with

- **Python**: data preparation and statistical analysis
- **pandas**: transformation and aggregation
- **statsmodels**: regression and elasticity
- **Power BI**: interactive dashboard

---





Raw Walmart data is not included because of its size and Kaggle's competition rules.




---

## 💭 The takeaway

Don't ask: *"How much did the promotion sell?"*

Ask: ***"Did the promotion create enough extra profit to be worth it?"***

That is the question this project was built to answer.

---

**👩‍💻 Vaishnavi Dangeti**
Pricing Analytics • Business Intelligence • Statistical Analysis
