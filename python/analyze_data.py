from pathlib import Path
import pandas as pd

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Load cleaned datasets
orders = pd.read_csv(DATA_DIR / "orders_clean.csv")
items = pd.read_csv(DATA_DIR / "order_items_clean.csv")
products = pd.read_csv(DATA_DIR / "products_clean.csv")
customers = pd.read_csv(DATA_DIR / "customers_clean.csv")
payments = pd.read_csv(DATA_DIR / "payments_clean.csv")

print("\n=== DATASET ROW COUNTS ===")
for name, df in {
    "Orders": orders,
    "Order Items": items,
    "Products": products,
    "Customers": customers,
    "Payments": payments,
}.items():
    print(f"{name}: {len(df):,} rows")

# Convert dates safely
for col in [
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]:
    if col in orders.columns:
        orders[col] = pd.to_datetime(orders[col], errors="coerce")

# Sales by month
items["price"] = pd.to_numeric(items["price"], errors="coerce")
monthly_sales = items.merge(
    orders[["order_id", "order_purchase_timestamp"]],
    on="order_id",
    how="left",
)
monthly_sales["month"] = (
    monthly_sales["order_purchase_timestamp"].dt.to_period("M").astype("string")
)
monthly_sales = (
    monthly_sales.groupby("month", dropna=False)["price"]
    .sum()
    .reset_index(name="total_sales")
)
monthly_sales.to_csv(REPORTS_DIR / "monthly_sales.csv", index=False)

# Sales by product category
category_sales = items.merge(
    products[["product_id", "product_category_name"]],
    on="product_id",
    how="left",
)
category_sales = (
    category_sales.groupby("product_category_name", dropna=False)["price"]
    .sum()
    .reset_index(name="total_sales")
    .sort_values("total_sales", ascending=False)
)
category_sales.to_csv(REPORTS_DIR / "sales_by_category.csv", index=False)

# Sales by customer state
state_sales = orders[["order_id", "customer_id"]].merge(
    customers[["customer_id", "customer_state"]],
    on="customer_id",
    how="left",
).merge(
    items[["order_id", "price"]],
    on="order_id",
    how="left",
)
state_sales = (
    state_sales.groupby("customer_state", dropna=False)["price"]
    .sum()
    .reset_index(name="total_sales")
    .sort_values("total_sales", ascending=False)
)
state_sales.to_csv(REPORTS_DIR / "sales_by_state.csv", index=False)

# Payment method analysis
payments["payment_value"] = pd.to_numeric(
    payments["payment_value"], errors="coerce"
)
payment_analysis = (
    payments.groupby("payment_type", dropna=False)["payment_value"]
    .agg(total_payments="sum", payment_records="count")
    .reset_index()
    .sort_values("total_payments", ascending=False)
)
payment_analysis.to_csv(REPORTS_DIR / "payment_analysis.csv", index=False)

# Delivery analysis
if (
    "order_delivered_customer_date" in orders.columns
    and "order_estimated_delivery_date" in orders.columns
):
    delivered = orders.dropna(
        subset=[
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ]
    ).copy()

    delivered["delivery_days"] = (
        delivered["order_delivered_customer_date"]
        - delivered["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400

    delivered["delivery_performance"] = (
        delivered["order_delivered_customer_date"]
        .le(delivered["order_estimated_delivery_date"])
        .map({True: "On Time", False: "Delayed"})
    )

    delivery_analysis = (
        delivered.groupby("delivery_performance")["delivery_days"]
        .agg(
            average_delivery_days="mean",
            order_count="count",
        )
        .reset_index()
    )
    delivery_analysis.to_csv(
        REPORTS_DIR / "delivery_analysis.csv", index=False
    )
    print("\n=== DELIVERY ANALYSIS ===")
    print(delivery_analysis.to_string(index=False))

print("\n=== MONTHLY SALES (LATEST 12 MONTHS) ===")
print(monthly_sales.tail(12).to_string(index=False))

print("\n=== TOP 10 PRODUCT CATEGORIES ===")
print(category_sales.head(10).to_string(index=False))

print("\n=== TOP STATES BY SALES ===")
print(state_sales.head(10).to_string(index=False))

print("\n=== PAYMENT ANALYSIS ===")
print(payment_analysis.to_string(index=False))

print(f"\nAnalysis complete. Reports saved to: {REPORTS_DIR}")
