# E-commerce Sales and Delivery Analysis

An end-to-end data analytics project exploring e-commerce sales, customer behavior, payment methods, product categories, and delivery performance using Python, MySQL, and Power BI.

## Project Overview

This project analyzes the Brazilian Olist e-commerce dataset to identify sales trends, high-performing product categories, state-level revenue patterns, payment preferences, and delivery performance.

## Tools and Technologies

- **Python:** Pandas, Matplotlib, Seaborn
- **SQL:** MySQL / MariaDB
- **Database Management:** XAMPP and phpMyAdmin
- **Dashboard:** Microsoft Power BI
- **Version Control:** Git and GitHub

## Project Structure

```text
Ecommerce-Sales-Delivery/
├── data/
│   └── processed/
├── dashboard/
├── docs/
├── python/
│   ├── validate_data.py
│   ├── clean_data.py
│   ├── import_to_mysql.py
│   ├── analyze_data.py
│   └── visualize_data.py
├── reports/
│   ├── monthly_sales.csv
│   ├── sales_by_category.csv
│   ├── sales_by_state.csv
│   ├── payment_analysis.csv
│   ├── delivery_analysis.csv
│   ├── monthly_sales_trend.png
│   ├── top_product_categories.png
│   ├── top_states_by_sales.png
│   ├── payment_methods.png
│   └── delivery_performance.png
├── sql/
├── requirements.txt
└── README.md
```

## Dataset

The project uses the Brazilian Olist e-commerce dataset. The cleaned data includes orders, order items, products, customers, payments, and sellers.

| Dataset     |    Rows |
| ----------- | ------: |
| Orders      |  99,441 |
| Order items | 112,650 |
| Products    |  32,951 |
| Customers   |  99,441 |
| Payments    | 103,886 |

## Analysis Performed

### Python

- Validated and cleaned source data.
- Analyzed monthly sales trends.
- Identified top product categories and customer states by sales.
- Compared payment methods and payment values.
- Evaluated average delivery time and delivery timeliness.
- Exported analysis tables and charts.

### SQL

- Imported cleaned datasets into MySQL.
- Explored sales, orders, customers, products, payments, and delivery data.
- Performed aggregation and business analysis queries.

### Power BI

The interactive dashboard includes:

- Total orders, customers, sales, and payments.
- Monthly sales trend.
- Sales by product category.
- Sales by customer state.
- Payment method analysis.
- Delivery performance analysis.

## Key Findings

- **Sales by state:** São Paulo (SP) recorded the highest sales in the analyzed data, at approximately 5.20 million.
- **Product categories:** `beleza_saude` was the top category by item sales, at approximately 1.26 million.
- **Payment methods:** Credit cards accounted for approximately 12.54 million in recorded payment value.
- **Delivery performance:** Among orders with both actual and estimated delivery dates, 88,649 were delivered on or before the estimated date, while 7,827 were delivered late.
- **Delivery duration:** Average purchase-to-delivery duration was approximately 10.88 days for on-time orders and 31.52 days for delayed orders.

_Figures are based on the current analysis outputs and may change with filters, data updates, or calculation definitions._

## How to Run the Python Analysis

1. Install Python.
2. Open a terminal in the project folder.
3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Run validation and cleaning as required by your local setup.
5. Run the analysis scripts from the project root:

   ```bash
   python python/analyze_data.py
   python python/visualize_data.py
   ```

The generated CSV summaries and PNG charts are saved in the `reports/` directory.

## Dashboard Preview

Add a screenshot of the completed Power BI dashboard here after saving it in the repository:

```markdown
![E-commerce Sales and Delivery Dashboard](docs/dashboard-preview.png)
```

## Notes

- Configure the local MySQL connection before running the database import script.
- Do not commit database passwords, API keys, or other secrets.
- Check dataset licensing and redistribution terms before uploading source or processed data.
- The `.pbix` report can be included if repository file-size limits and dataset permissions allow it.

## Author

**Vikash SR**

Data Analytics Portfolio Project
