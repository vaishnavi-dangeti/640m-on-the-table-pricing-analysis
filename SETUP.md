# Setup

## 1. Install
```
pip install -r requirements.txt
```

## 2. Run the pipeline (from inside the 3_PYTHON folder)
```
cd 3_PYTHON
python 01_data_analysis.py
python 02_demand_prediction.py
python 03_price_optimization.py
python 04_dashboard_tables.py
```
Run them in this order. 03 saves `1_DATA/pricing_recommendations.csv`, and 04 reads it.

## 3. SQL (optional, MySQL 8.0+)
1. Run `2_SQL/01_schema.sql`.
2. Import the CSV files from `1_DATA` into the matching tables.
3. Run `2_SQL/02_business_analysis.sql`.

## 4. Dashboard
Open the Power BI file in `4_DASHBOARD` and refresh from the CSV files in that folder.
