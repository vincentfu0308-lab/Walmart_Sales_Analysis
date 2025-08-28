import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.types import Integer, Float, String, SmallInteger, Date, DECIMAL
from dotenv import load_dotenv

# Directory for processed CSV outputs
PROCESSED_DIR = "./data/processed"

def to_csv(df: pd.DataFrame, filename: str):
    """
    Save a DataFrame to CSV in the processed data directory.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to save.
    filename : str
        File name for the CSV file.

    Returns
    -------
    str
        Full path of the saved file.
    """

    os.makedirs(PROCESSED_DIR, exist_ok=True)
    path = os.path.join(PROCESSED_DIR, filename)
    df.to_csv(path, index=False)
    return path

# Load environment variables (e.g., DB_URL from .env)
load_dotenv()
DB_URL = os.getenv("DB_URL") or "mysql+pymysql://root:1243284120Qq@127.0.0.1:3306/walmart_sales"

def to_mysql(df: pd.DataFrame, table: str = "walmart_sales_clean") -> None:
    engine = create_engine(DB_URL, pool_pre_ping=True)

    with engine.begin() as conn:
        # Current DB info
        curr_db = conn.execute(text("SELECT DATABASE();")).scalar()
        print("→ Current DB:", curr_db)
        print("→ Writing rows:", len(df))

        # Define column types explicitly
        dtype_map = {
            "store": Integer(), "dept": Integer(), "date": Date(),
            "weekly_sales": DECIMAL(12, 2), "isholiday": SmallInteger(),
            "temperature": Float(), "fuel_price": Float(),
            "cpi": Float(), "unemployment": Float(),
            "type": String(5), "size": Integer(),
            "year": Integer(), "month": Integer(), "week": Integer(),
            "holiday_flag": SmallInteger(), "sales_per_size": Float(),
        }

        # Write DataFrame to MySQL
        df.to_sql(table, con=conn, if_exists="replace", index=False,
                  chunksize=50000, method="multi", dtype=dtype_map)

        # Validate row count
        cnt = conn.execute(text(f"SELECT COUNT(*) FROM {table};")).scalar()
        print(f"✅ MySQL rows in {table}: {cnt}")

        # Define helper inside the connection block
        def create_index_if_absent(conn, table: str, index_name: str, columns: str):
            schema = conn.execute(text("SELECT DATABASE();")).scalar()
            exists = conn.execute(text("""
                SELECT COUNT(*)
                FROM information_schema.statistics
                WHERE table_schema = :schema
                  AND table_name   = :table
                  AND index_name   = :index
            """), {"schema": schema, "table": table, "index": index_name}).scalar()
            if exists == 0:
                conn.execute(text(f"CREATE INDEX {index_name} ON {table}({columns});"))
                print(f"→ Created index {index_name} on {table}({columns})")
            else:
                print(f"→ Index {index_name} already exists")

        # ✅ Create indexes (inside with-block)
        create_index_if_absent(conn, table, f"idx_{table}_store_date", "store, date")
        create_index_if_absent(conn, table, f"idx_{table}_date", "date")