from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", palette="crest")

# Load Python EDA outputs
monthly = pd.read_csv(REPORTS_DIR / "monthly_sales.csv")
categories = pd.read_csv(REPORTS_DIR / "sales_by_category.csv")
states = pd.read_csv(REPORTS_DIR / "sales_by_state.csv")
payments = pd.read_csv(REPORTS_DIR / "payment_analysis.csv")
delivery = pd.read_csv(REPORTS_DIR / "delivery_analysis.csv")

# 1. Monthly sales trend
monthly = monthly.dropna(subset=["month", "total_sales"])
monthly = monthly.sort_values("month")

plt.figure(figsize=(12, 6))
sns.lineplot(
    data=monthly,
    x="month",
    y="total_sales",
    marker="o",
    linewidth=2.5,
)
plt.title("Monthly E-commerce Sales Trend", fontsize=16, weight="bold")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(REPORTS_DIR / "monthly_sales_trend.png", dpi=300)
plt.close()

# 2. Top 10 product categories
top_categories = categories.nlargest(10, "total_sales").sort_values("total_sales")

plt.figure(figsize=(12, 7))
sns.barplot(
    data=top_categories,
    x="total_sales",
    y="product_category_name",
)
plt.title("Top 10 Product Categories by Sales", fontsize=16, weight="bold")
plt.xlabel("Sales")
plt.ylabel("Product Category")
plt.tight_layout()
plt.savefig(REPORTS_DIR / "top_product_categories.png", dpi=300)
plt.close()

# 3. Top 10 states
top_states = states.nlargest(10, "total_sales").sort_values("total_sales")

plt.figure(figsize=(10, 6))
sns.barplot(data=top_states, x="total_sales", y="customer_state")
plt.title("Top 10 States by Sales", fontsize=16, weight="bold")
plt.xlabel("Sales")
plt.ylabel("Customer State")
plt.tight_layout()
plt.savefig(REPORTS_DIR / "top_states_by_sales.png", dpi=300)
plt.close()

# 4. Payment methods
payments = payments.sort_values("total_payments", ascending=False)

plt.figure(figsize=(9, 6))
sns.barplot(data=payments, x="payment_type", y="total_payments")
plt.title("Payments by Payment Method", fontsize=16, weight="bold")
plt.xlabel("Payment Method")
plt.ylabel("Total Payments")
plt.xticks(rotation=25, ha="right")
plt.tight_layout()
plt.savefig(REPORTS_DIR / "payment_methods.png", dpi=300)
plt.close()

# 5. Average delivery time by status
plt.figure(figsize=(8, 5))
sns.barplot(
    data=delivery,
    x="delivery_performance",
    y="average_delivery_days",
)
plt.title("Average Delivery Time by Performance", fontsize=15, weight="bold")
plt.xlabel("Delivery Performance")
plt.ylabel("Average Delivery Days")
plt.tight_layout()
plt.savefig(REPORTS_DIR / "delivery_performance.png", dpi=300)
plt.close()

print("Python visualizations completed!")
print(f"Charts saved in: {REPORTS_DIR}")
