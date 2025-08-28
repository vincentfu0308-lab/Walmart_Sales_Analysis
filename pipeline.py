from extract import extract
from transform import transform
from load import to_csv, to_mysql

if __name__ == "__main__":
    print("Running Walmart ETL pipeline")

    # 1. Extract
    stores, train, features = extract()

    # 2. Transform
    df = transform(stores, train, features)
    print("Rows after transform:", len(df))

    # 3a. Load → CSV
    out = to_csv(df, "walmart_sales_clean.csv")
    print(f"CSV saved: {out}")

    # 3b. Load → MySQL
    to_mysql(df, table="walmart_sales_clean")