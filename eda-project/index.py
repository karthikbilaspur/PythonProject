import pandas as pd
import os

# --- Config ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else "."
CUSTOMERS_FILE = os.path.join(BASE_DIR, "demo_customers.csv")
ORDERS_FILE = os.path.join(BASE_DIR, "demo_orders.csv")
PRODUCTS_FILE = os.path.join(BASE_DIR, "demo_products.csv")

def load_data():
    """Load all 3 CSVs with correct date parsing."""
    customers = pd.read_csv(CUSTOMERS_FILE, parse_dates=["signup_date"])
    orders = pd.read_csv(ORDERS_FILE, parse_dates=["order_date"])
    products = pd.read_csv(PRODUCTS_FILE)
    return customers, orders, products

def clean_data(
    customers: pd.DataFrame,
    orders: pd.DataFrame,
    products: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Basic cleaning - returns cleaned copies."""
    customers = customers.copy()
    orders = orders.copy()
    products = products.copy()

    # Strip whitespace from text columns
    for df in [customers, orders, products]:
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].astype(str).str.strip()

    # Fix types
    customers["age"] = pd.to_numeric(customers["age"], errors="coerce")
    orders["quantity"] = pd.to_numeric(orders["quantity"], errors="coerce")
    orders["delivery_days"] = pd.to_numeric(orders["delivery_days"], errors="coerce")
    orders["rating"] = pd.to_numeric(orders["rating"], errors="coerce")

    # Fill missing values (report them, don't silently drop)
    print(f"Missing rating: {orders['rating'].isna().sum()} rows")
    print(f"Missing delivery_days: {orders['delivery_days'].isna().sum()} rows")
    orders["rating_filled"] = orders["rating"].fillna(orders["rating"].median())
    orders["delivery_days_filled"] = orders["delivery_days"].fillna(orders["delivery_days"].median())

    return customers, orders, products

def merge_data(
    customers: pd.DataFrame,
    orders: pd.DataFrame,
    products: pd.DataFrame,
) -> pd.DataFrame:
    """Join orders -> customers -> products into one enriched dataframe."""
    prod = products.rename(columns={"price": "product_price"})
    df = orders.merge(customers, on="customer_id", how="left")
    df = df.merge(prod, on="product_id", how="left")
    # orders.price = price at order time, product_price = catalogue price
    df["profit"] = (df["price"] - df["cost"]) * df["quantity"]
    df["revenue"] = df["total_amount"]
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    return df

def print_section(title: str):
    print("\n" + "="*60)
    print(title)
    print("="*60)

def analyze(
    customers: pd.DataFrame,
    orders: pd.DataFrame,
    products: pd.DataFrame,
    df: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    print_section("1. DATASET OVERVIEW")
    print(f"Customers: {len(customers):,} rows, {len(customers.columns)} cols -> {list(customers.columns)}")
    print(f"Products : {len(products):,} rows, {len(products.columns)} cols -> {list(products.columns)}")
    print(f"Orders   : {len(orders):,} rows, {len(orders.columns)} cols -> {list(orders.columns)}")
    print(f"Customers who ordered: {orders['customer_id'].nunique()} / {len(customers)}")
    print(f"Customers with NO orders: {len(set(customers['customer_id']) - set(orders['customer_id']))}")

    print_section("2. CUSTOMERS")
    print("\nBy City:\n", customers["city"].value_counts().to_string())
    print("\nBy Segment:\n", customers["segment"].value_counts().to_string())
    print("\nBy Gender:\n", customers["gender"].value_counts().to_string())
    print(f"\nAge: min {customers['age'].min()}, max {customers['age'].max()}, mean {customers['age'].mean():.1f}, median {customers['age'].median():.0f}")
    print(f"Signup range: {customers['signup_date'].min().date()} to {customers['signup_date'].max().date()}")

    print_section("3. PRODUCTS")
    print("\nBy Category:\n", products["category"].value_counts().to_string())
    print(f"\nPrice: min Rs.{products['price'].min():,.2f}, max Rs.{products['price'].max():,.2f}, mean Rs.{products['price'].mean():,.2f}")
    print(f"Cost : min Rs.{products['cost'].min():,.2f}, max Rs.{products['cost'].max():,.2f}, mean Rs.{products['cost'].mean():,.2f}")

    print_section("4. ORDERS - REVENUE")
    total_revenue = orders["total_amount"].sum()
    print(f"Total Revenue      : Rs.{total_revenue:,.2f}")
    print(f"Average Order Value: Rs.{orders['total_amount'].mean():,.2f}")
    print(f"Median Order Value : Rs.{orders['total_amount'].median():,.2f}")
    print(f"Total Profit (est.): Rs.{df['profit'].sum():,.2f}")
    print(f"Order date range   : {orders['order_date'].min().date()} to {orders['order_date'].max().date()}")
    print("\nBy Payment Method:\n", orders["payment_method"].value_counts().to_string())
    print("\nBy Quantity:\n", orders["quantity"].value_counts().sort_index().to_string())
    print(f"\nDelivery days: mean {orders['delivery_days'].mean():.2f}, median {orders['delivery_days'].median():.0f}")
    print(f"Rating: mean {orders['rating'].mean():.2f}, median {orders['rating'].median():.0f}")
    print("\nRating distribution:\n", orders["rating"].value_counts(dropna=False).sort_index().to_string())

    print_section("5. REVENUE BY CATEGORY")
    cat = df.groupby("category").agg(orders=("order_id","count"), revenue=("total_amount","sum"), avg_rating=("rating","mean"), profit=("profit","sum")).sort_values("revenue", ascending=False)
    print(cat.to_string(float_format=lambda x: f"{x:,.2f}"))

    print_section("6. REVENUE BY CUSTOMER SEGMENT")
    seg = df.groupby("segment").agg(customers=("customer_id","nunique"), orders=("order_id","count"), revenue=("total_amount","sum"), avg_order=("total_amount","mean")).sort_values("revenue", ascending=False)
    print(seg.to_string(float_format=lambda x: f"{x:,.2f}"))

    print_section("7. REVENUE BY CITY")
    city = df.groupby("city").agg(customers=("customer_id","nunique"), orders=("order_id","count"), revenue=("total_amount","sum")).sort_values("revenue", ascending=False)
    print(city.to_string(float_format=lambda x: f"{x:,.2f}"))

    print_section("8. REVENUE BY MONTH")
    monthly = df.groupby("month").agg(orders=("order_id","count"), revenue=("total_amount","sum")).sort_index()
    print(monthly.to_string(float_format=lambda x: f"{x:,.2f}"))

    print_section("9. TOP 10 CUSTOMERS BY REVENUE")
    top_cust = df.groupby(["customer_id","city","segment"]).agg(orders=("order_id","count"), revenue=("total_amount","sum"), avg_rating=("rating","mean")).sort_values("revenue", ascending=False).head(10)
    print(top_cust.to_string(float_format=lambda x: f"{x:,.2f}"))

    print_section("10. TOP 10 PRODUCTS BY REVENUE")
    top_prod = df.groupby(["product_id","category"]).agg(orders=("order_id","count"), qty=("quantity","sum"), revenue=("total_amount","sum"), profit=("profit","sum")).sort_values("revenue", ascending=False).head(10)
    print(top_prod.to_string(float_format=lambda x: f"{x:,.2f}"))

    print_section("11. DATA QUALITY CHECKS")
    print(f"Price mismatch (orders vs products): {(abs(df['price'] - df['product_price']) > 0.01).sum()}")
    print(f"Total_amount mismatch (qty*price): {(abs(df['total_amount'] - df['quantity']*df['price']) > 0.01).sum()}")
    print(f"Orphan customer_ids in orders: {len(set(orders['customer_id']) - set(customers['customer_id']))}")
    print(f"Orphan product_ids in orders: {len(set(orders['product_id']) - set(products['product_id']))}")

    return {"monthly": monthly, "category": cat, "segment": seg, "city": city, "top_customers": top_cust, "top_products": top_prod}

def save_outputs(results: dict[str, pd.DataFrame], df: pd.DataFrame):
    """Save enriched + summary files next to the script."""
    df.to_csv(os.path.join(BASE_DIR, "enriched_orders.csv"), index=False)
    print(f"\nSaved: enriched_orders.csv ({len(df)} rows)")
    for name, table in results.items():
        path = os.path.join(BASE_DIR, f"summary_{name}.csv")
        table.to_csv(path)
        print(f"Saved: {path}")

def main():
    customers, orders, products = load_data()
    customers, orders, products = clean_data(customers, orders, products)
    df = merge_data(customers, orders, products)
    results = analyze(customers, orders, products, df)
    save_outputs(results, df)
    print("\nDone!")

if __name__ == "__main__":
    main()