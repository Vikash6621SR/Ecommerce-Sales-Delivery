from pathlib import Path
import pandas as pd
import mysql.connector
from mysql.connector import Error

PROJECT = Path(
    r"C:\Users\SR\OneDrive\Desktop\Personal Projects\Data Analyst\Ecommerce-Sales-Delivery"
)
DATA_DIR = PROJECT / "data" / "processed"

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3307,
    "user": "root",
    "password": "",  # Update if your MariaDB root account has a password
    "database": "ecommerce_sales_db",
}

TABLES = {
    "customers_clean.csv": "customers",
    "sellers_clean.csv": "sellers",
    "products_clean.csv": "products",
    "orders_clean.csv": "orders",
    "order_items_clean.csv": "order_items",
    "payments_clean.csv": "payments",
}

def clean_value(value):
    if pd.isna(value):
        return None
    if hasattr(value, "to_pydatetime"):
        return value.to_pydatetime()
    if hasattr(value, "item"):
        return value.item()
    return value

def main():
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        print("Connected to ecommerce_sales_db.")

        for filename, table in TABLES.items():
            path = DATA_DIR / filename
            if not path.exists():
                raise FileNotFoundError(f"Missing file: {path}")

            df = pd.read_csv(path, low_memory=False)
            columns = list(df.columns)

            column_sql = ", ".join(f"`{c}`" for c in columns)
            placeholders = ", ".join(["%s"] * len(columns))

            insert_sql = (
                f"INSERT INTO `{table}` ({column_sql}) "
                f"VALUES ({placeholders})"
            )

            print(f"\nImporting {filename} into {table}...")
            cursor.execute(f"DELETE FROM `{table}`")
            connection.commit()

            batch_size = 1000
            inserted = 0

            for start in range(0, len(df), batch_size):
                batch = df.iloc[start:start + batch_size]
                records = [
                    tuple(clean_value(v) for v in row)
                    for row in batch.itertuples(index=False, name=None)
                ]

                cursor.executemany(insert_sql, records)
                connection.commit()
                inserted += len(records)

            print(f"Imported {inserted:,} rows into {table}.")

        print("\nAll six CSV files imported successfully.")

    except (Error, Exception) as exc:
        if connection and connection.is_connected():
            connection.rollback()
        print(f"\nIMPORT FAILED: {exc}")
        print("Check the error before attempting another import.")

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    main()
