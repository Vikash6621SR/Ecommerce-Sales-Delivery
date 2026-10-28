from pathlib import Path
import pandas as pd

PROJECT = Path(
    r"C:\Users\SR\OneDrive\Desktop\Personal Projects\Data Analyst\Ecommerce-Sales-Delivery"
)

RAW = PROJECT / "data" / "raw"
OUT = PROJECT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

def load_csv(filename):
    path = RAW / filename
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")
    return pd.read_csv(path, low_memory=False)

def save_csv(df, filename):
    path = OUT / filename
    df.to_csv(path, index=False, encoding="utf-8")
    print(f"Saved {filename}: {len(df):,} rows, {len(df.columns)} columns")

# 1. Orders: preserve all statuses and missing dates.
orders = load_csv("olist_orders_dataset.csv")

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

for col in date_columns:
    orders[col] = pd.to_datetime(orders[col], errors="coerce")

# Flag delivered orders that arrived after their estimated date.
actual = orders["order_delivered_customer_date"]
estimated = orders["order_estimated_delivery_date"]

orders["delivery_days"] = (
    actual - orders["order_purchase_timestamp"]
).dt.total_seconds() / 86400

orders["delivery_delay_days"] = (
    actual - estimated
).dt.total_seconds() / 86400

orders["delivery_performance"] = "Not delivered"

delivered = orders["order_status"].eq("delivered") & actual.notna()
orders.loc[delivered, "delivery_performance"] = "On time"
orders.loc[
    delivered & (orders["delivery_delay_days"] > 0),
    "delivery_performance",
] = "Late"

orders.loc[
    delivered & (orders["delivery_delay_days"] <= 0),
    "delivery_performance",
] = "On time"

save_csv(orders, "orders_clean.csv")

# 2. Order items: preserve line items and amounts.
items = load_csv("olist_order_items_dataset.csv")
items["shipping_limit_date"] = pd.to_datetime(
    items["shipping_limit_date"], errors="coerce"
)
save_csv(items, "order_items_clean.csv")

# 3. Products: translate category names where possible.
products = load_csv("olist_products_dataset.csv")
translation_file = RAW / "product_category_name_translation.csv"

if translation_file.exists():
    translations = pd.read_csv(translation_file)
    products = products.merge(
        translations,
        on="product_category_name",
        how="left",
        validate="many_to_one",
    )
    products["product_category_english"] = (
        products["product_category_name_english"]
        .fillna(products["product_category_name"])
        .fillna("Unknown")
    )
    products = products.drop(
        columns=["product_category_name_english"]
    )
else:
    products["product_category_english"] = (
        products["product_category_name"].fillna("Unknown")
    )

save_csv(products, "products_clean.csv")

# 4. Customers.
customers = load_csv("olist_customers_dataset.csv")
save_csv(customers, "customers_clean.csv")

# 5. Payments.
payments = load_csv("olist_order_payments_dataset.csv")
save_csv(payments, "payments_clean.csv")

# 6. Sellers.
sellers = load_csv("olist_sellers_dataset.csv")
save_csv(sellers, "sellers_clean.csv")

print("\nCleaning completed.")
print("Original raw CSV files were not modified.")
print(f"Output folder: {OUT}")
