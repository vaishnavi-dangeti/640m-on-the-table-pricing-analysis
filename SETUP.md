# ⚙️ Setup Guide

Follow these steps to run the project from scratch.

## 1. Install Python
Install Python 3.10 or newer. Anaconda is the easiest option on Windows, since it includes most libraries.

## 2. Install the libraries
Open a terminal in the project folder and run:
```bash
pip install -r requirements.txt
```

## 3. Get the data
1. On Kaggle, open the **M5 Forecasting – Accuracy** competition, go to the **Data** tab and accept the rules.
2. Download these 3 files:
   - `calendar.csv`
   - `sell_prices.csv`
   - `sales_train_evaluation.csv`
3. Put them in the `1_DATA/` folder.

⚠️ Don't open `sell_prices.csv` in Excel. It has about 6.8 million rows and Excel will cut it off.

## 4. Run the scripts in order
Run every script from inside the `3_PYTHON` folder:
```bash
cd 3_PYTHON
python 01_prepare_data.py
python 02_estimate_elasticity.py
python 03_discount_profit.py
python 04_dashboard_tables.py
```

## 5. Check your results
If everything worked, you should see:

| Script | What to check |
|---|---|
| `01_prepare_data.py` | 3,049 products · 683,167 product-weeks · 277 weeks |
| `02_estimate_elasticity.py` | Food elasticity: FOODS_1 −0.65, FOODS_2 −0.56, FOODS_3 −0.59 |
| `03_discount_profit.py` | 14,016 discount weeks · profit change −$69,585 at 35% margin |
| `04_dashboard_tables.py` | 5 tables saved to `4_DASHBOARD/` |

## 6. Open the dashboard
1. Open `4_DASHBOARD/PowerBI_Dashboard.pbix` in Power BI Desktop.
2. If it can't find the data: **Home → Transform data → Data source settings**, select each file, click **Change Source**, and point it to your own `4_DASHBOARD` folder.
3. Click **Refresh**.

## Troubleshooting

| Problem | Fix |
|---|---|
| `No such file or directory` | You're in the wrong folder. Run `cd 3_PYTHON` first. |
| Yellow `UserWarning` about numexpr | Harmless, you can ignore it. |
| Script is slow | Normal: script 01 reads large files and takes 1–3 minutes. |
