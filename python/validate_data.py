
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(
    r"C:\Users\SR\OneDrive\Desktop\Personal Projects\Data Analyst\Ecommerce-Sales-Delivery"
)
RAW_DIR = PROJECT_DIR / "data" / "raw"
REPORT_DIR = PROJECT_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

if not RAW_DIR.exists():
    raise FileNotFoundError(f"Folder not found: {RAW_DIR}")

files = sorted(RAW_DIR.glob("*.csv"))
if not files:
    raise FileNotFoundError(f"No CSV files found in {RAW_DIR}")

summary = []
missing_details = []

for file in files:
    print(f"\nChecking: {file.name}")
    df = pd.read_csv(file, low_memory=False)

    summary.append({
        "file": file.name,
        "rows": len(df),
        "columns": len(df.columns),
        "duplicate_full_rows": int(df.duplicated().sum()),
        "missing_cells": int(df.isna().sum().sum()),
        "missing_columns": int(df.isna().any(axis=0).sum()),
    })

    for column in df.columns:
        missing = int(df[column].isna().sum())
        if missing:
            missing_details.append({
                "file": file.name,
                "column": column,
                "missing_count": missing,
                "missing_percent": round(missing / len(df) * 100, 2),
            })

    print(f"Rows: {len(df):,} | Columns: {len(df.columns)}")
    print(f"Duplicate full rows: {df.duplicated().sum():,}")
    print(f"Missing cells: {df.isna().sum().sum():,}")

summary_path = REPORT_DIR / "validation_summary.csv"
missing_path = REPORT_DIR / "missing_values.csv"

pd.DataFrame(summary).to_csv(summary_path, index=False)
pd.DataFrame(
    missing_details,
    columns=["file", "column", "missing_count", "missing_percent"]
).to_csv(missing_path, index=False)

print("\nVALIDATION COMPLETED")
print(f"Summary saved to: {summary_path}")
print(f"Missing-value report saved to: {missing_path}")
