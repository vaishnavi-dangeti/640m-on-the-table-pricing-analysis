-- ============================================================
-- DYNAMIC PRICING & PROFIT OPTIMIZATION ENGINE
-- 01 - DATABASE SCHEMA (MySQL, synthetic dataset)
-- ============================================================

CREATE DATABASE IF NOT EXISTS dynamic_pricing;
USE dynamic_pricing;

-- 1. PRODUCTS
CREATE TABLE IF NOT EXISTS products (
    product_id   VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category     VARCHAR(50)  NOT NULL,
    base_cost    DECIMAL(10,2) NOT NULL,
    base_price   DECIMAL(10,2) NOT NULL,
    min_price    DECIMAL(10,2) NOT NULL,
    max_price    DECIMAL(10,2) NOT NULL
);

-- 2. SALES TRANSACTIONS
CREATE TABLE IF NOT EXISTS sales (
    transaction_id   VARCHAR(30) PRIMARY KEY,
    date             DATE NOT NULL,
    product_id       VARCHAR(20) NOT NULL,
    category         VARCHAR(50),
    unit_price       DECIMAL(10,2) NOT NULL,
    discount_pct     DECIMAL(6,2),
    competitor_price DECIMAL(10,2),
    promotion_flag   TINYINT,
    quantity_sold    INT NOT NULL,
    revenue          DECIMAL(14,2),
    gross_profit     DECIMAL(14,2),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
CREATE INDEX idx_sales_product ON sales(product_id);
CREATE INDEX idx_sales_date    ON sales(date);

-- 3. COMPETITOR PRICES
CREATE TABLE IF NOT EXISTS competitor_prices (
    product_id           VARCHAR(20) NOT NULL,
    date                 DATE NOT NULL,
    competitor_a_price   DECIMAL(10,2),
    competitor_b_price   DECIMAL(10,2),
    competitor_c_price   DECIMAL(10,2),
    competitor_avg_price DECIMAL(10,2),
    PRIMARY KEY (product_id, date),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- 4. INVENTORY
CREATE TABLE IF NOT EXISTS inventory (
    product_id          VARCHAR(20) NOT NULL,
    date                DATE NOT NULL,
    opening_inventory   INT,
    units_sold_estimate INT,
    closing_inventory   INT,
    reorder_point       INT,
    inventory_status    VARCHAR(30),
    PRIMARY KEY (product_id, date),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- 5. PROMOTIONS
CREATE TABLE IF NOT EXISTS promotions (
    promotion_id           VARCHAR(30) PRIMARY KEY,
    date                   DATE NOT NULL,
    promotion_type         VARCHAR(50),
    promotion_discount_pct DECIMAL(6,2)
);

-- 6. CALENDAR
CREATE TABLE IF NOT EXISTS calendar (
    date        DATE PRIMARY KEY,
    day_of_week VARCHAR(20),
    month       INT,
    quarter     INT,
    is_weekend  TINYINT,
    season      VARCHAR(30)
);

-- 7. PRICING RECOMMENDATIONS (output of 3_PYTHON/03_price_optimization.py)
CREATE TABLE IF NOT EXISTS pricing_recommendations (
    product_id         VARCHAR(20) PRIMARY KEY,
    current_price      DECIMAL(12,2),
    competitor_price   DECIMAL(12,2),
    unit_cost          DECIMAL(12,2),
    units_sold         INT,
    product_name       VARCHAR(150),
    min_price          DECIMAL(12,2),
    max_price          DECIMAL(12,2),
    category           VARCHAR(50),
    price_elasticity   DECIMAL(8,4),
    recommended_price  DECIMAL(12,2),
    volume_change_pct  DECIMAL(8,3),
    revenue_current    DECIMAL(16,2),
    revenue_modelled   DECIMAL(16,2),
    revenue_uplift     DECIMAL(16,2),
    profit_current     DECIMAL(16,2),
    profit_modelled    DECIMAL(16,2),
    profit_uplift      DECIMAL(16,2),
    price_change_pct   DECIMAL(8,3),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- ============================================================
-- SCHEMA COMPLETE
-- ============================================================
