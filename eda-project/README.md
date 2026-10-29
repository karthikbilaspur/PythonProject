# E-Commerce EDA - Demo Project

> End-to-end Exploratory Data Analysis on 1000 orders, 500 customers, 50 products

## Problem

Analyze an e-commerce store to find what drives revenue, ratings, and delivery issues.

## Dataset (3 CSVs)

- `data/raw/demo_orders.csv` - 1000 orders (main)
- `data/raw/demo_customers.csv` - 500 customers
- `data/raw/demo_products.csv` - 50 products

## Key Insights (from notebook)

1. Premium customers = 20% users but ~35% revenue
2. Delivery days >4 drops rating from 4.2 to 3.1
3. UPI is most used, Card has highest AOV
4. Electronics has high margin but lower rating
5. Revenue peaks Oct-Dec (festive season)

## How to Run

```bash
pip install -r requirements.txt
jupyter notebook notebooks/01_eda.ipynb
```

## Tech Stack

Python, Pandas, Matplotlib, Seaborn

## Structure

- notebooks/01_eda.ipynb - full EDA
- data/raw - original data
- data/processed - cleaned_orders.csv
- visuals/ - exported charts
