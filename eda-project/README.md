# A simple Python script that loads, cleans, joins, and analyzes 3 demo CSV files

— customers, orders, and products — and prints a full business summary.

Files in this project
File Description
demo_analysis.py Main analysis script. Run this.
demo_customers.csv 500 customers — id, city, age, gender, signup_date, segment
demo_orders.csv 1,000 orders — order, customer, product, date, quantity, payment, delivery, rating, price, total
demo_products.csv 50 products — id, category, price, cost
enriched_orders.csv (Generated) All 3 files joined into one table
summary_*.csv (Generated) Summary tables — monthly, category, segment, city, top customers, top products

Requirements
Python 3.9+
pandas
pip install pandas
How to run
Put all files in the same folder:
your-folder/
├── index.py
├── demo_customers.csv
├── demo_orders.csv
└── demo_products.csv

Run the script:
python index.py
That's it. No arguments needed — the script finds the CSVs next to itself.

What it does
Loads all 3 CSVs, parsing signup_date and order_date as dates.

Cleans the data:
Trims whitespace from text columns
Converts age, quantity, delivery_days, rating to numbers
Reports missing values instead of silently dropping them
rating: 107 missing
delivery_days: 21 missing

Joins everything into one enriched table:
orders.customer_id → customers
orders.product_id → products
Calculates new columns:
profit = (price - cost) *quantity
revenue = total_amount
month = YYYY-MM from order_date
Prints 11 sections to the terminal (see below).
Saves enriched_orders.csv + 6 summary_*.csv files in the same folder.

What it prints

Section What you get

1 Dataset Overview Row counts, columns, customers who ordered vs. never ordered (68)

2 Customers By city, segment, gender, age stats, signup range

3 Products By category, price / cost stats

4 Orders — Revenue Total revenue (Rs. 2,46,15,389.25), AOV, profit, payment method, quantity, delivery, rating

5 Revenue by Category Orders, revenue, avg rating, profit per category

6 Revenue by Segment Customers, orders, revenue, AOV per Regular / New / Premium

7 Revenue by City Customers, orders, revenue per city

8 Revenue by Month Orders + revenue per month

9 Top 10 Customers By revenue, with city, segment, order count, avg rating

10 Top 10 Products By revenue, with category, quantity, profit

11 Data Quality Checks Price mismatches, total_amount mismatches, orphan customer / product IDs
Example output

4 ORDERS - REVENUE

Total Revenue      : Rs. 2,46,15,389.25
Average Order Value: Rs. 24,615.39
Median Order Value : Rs. 18,180.36
Order date range   : 2023-01-01 to 2024-08-23
Output files
After a run, you'll see these new files next to the script:

enriched_orders.csv        # 1,000 rows, orders + customer + product columns
summary_monthly.csv
summary_category.csv
summary_segment.csv
summary_city.csv
summary_top_customers.csv
summary_top_products.csv
Open any of them in Excel / Google Sheets.

Want only one section: Comment out the other print_section(...) blocks in analyze().
Notes
Prices in the demo data are in INR.
This is demo data — no real customer data.
The script does not modify your original CSVs. It only reads them and writes new enriched_ / summary_ files.
