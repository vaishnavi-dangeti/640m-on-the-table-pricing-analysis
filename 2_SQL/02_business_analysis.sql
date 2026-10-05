-- ============================================================
-- DYNAMIC PRICING & PROFIT OPTIMIZATION ENGINE
-- 02 - BUSINESS ANALYSIS USING SQL (MySQL, synthetic dataset)
-- ============================================================

USE dynamic_pricing;

-- ------------------------------------------------------------
-- A. DATA QUALITY CHECKS
-- ------------------------------------------------------------

-- A1. Duplicate transactions (should return no rows)
SELECT transaction_id, COUNT(*) AS copies
FROM sales
GROUP BY transaction_id
HAVING COUNT(*) > 1;

-- A2. Missing or impossible values (all counts should be 0)
SELECT
    SUM(unit_price <= 0)          AS bad_prices,
    SUM(quantity_sold <= 0)       AS bad_quantities,
    SUM(competitor_price IS NULL) AS missing_competitor_price,
    SUM(gross_profit IS NULL)     AS missing_profit
FROM sales;

-- A3. Sales priced outside the product's allowed range
SELECT COUNT(*) AS outside_price_limits
FROM sales s
JOIN products p ON s.product_id = p.product_id
WHERE s.unit_price < p.min_price OR s.unit_price > p.max_price;


-- ------------------------------------------------------------
-- B. BUSINESS PERFORMANCE
-- ------------------------------------------------------------

-- B1. Overall performance
SELECT
    COUNT(DISTINCT transaction_id)                  AS total_transactions,
    SUM(quantity_sold)                              AS total_units_sold,
    ROUND(SUM(revenue), 2)                          AS total_revenue,
    ROUND(SUM(gross_profit), 2)                     AS total_profit,
    ROUND(SUM(gross_profit) / SUM(revenue) * 100, 2) AS margin_pct
FROM sales;

-- B2. Monthly revenue and profit
SELECT
    MONTH(date)                  AS month,
    ROUND(SUM(reven
    
