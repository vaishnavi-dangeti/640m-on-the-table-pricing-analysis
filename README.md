# Dynamic Pricing & Profit Optimization Engine

Estimates how sensitive demand is to price for each of 500 products, then tests prices to find the most profitable one. **The dataset is synthetic**, so results illustrate the method and are not a forecast of real business performance.

## Result
- **₹270M simulated gross profit uplift**
- **5.0% average price change** across 500 products
- Price elasticity ranges from **-4.55 to -0.24**
- Profit rises even though some units are lost, because each sale earns more
- [FILL AFTER STEP 4: largest category and its share of uplift]
- [FILL AFTER STEP 4: % of products priced below competitors]

## Data (synthetic)
500 products across 5 categories, 100,000 sales records, competitor prices, inventory, promotions and a calendar table, covering 365 days.

## Method
1. **SQL** (`2_SQL`): schema, data quality checks and business KPIs.
2. **Elasticity** (`03_price_optimization.py`): a log-log regression per product of units sold on price, controlling for promotions. Unreliable estimates fall back to the category median.
3. **Cost**: unit cost is taken from gross profit per unit sold.
4. **Optimisation**: for each product, prices from -5% to +8% are tested. The price with the highest gross profit is chosen, within the product's price limits and at most 10% above the competitor price.
5. **Demand model** (`02_demand_prediction.py`): a Random Forest was tested as an exploratory model. It is not used for final prices, because tree models are step-like in price and understate demand loss when prices rise.
6. **Dashboard** (`4_DASHBOARD`): Power BI report built from the output tables.

## Limitations
- Constant elasticity is assumed for each product.
- Top products hit the +8% cap, so the true optimum may be higher.
- Competitor reactions and brand effects are not modelled.
- Monthly values are estimated by applying each product's modelled-to-current ratio to its monthly sales.
- With real data, estimates would need validation, ideally through price tests.

## Run it
See `SETUP.md`.

## Tools
Python (pandas, statsmodels, scikit-learn), SQL (MySQL), Power BI.
