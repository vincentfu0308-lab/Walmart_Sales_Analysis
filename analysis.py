import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

DB_URL = "mysql+pymysql://root:1243284120Qq@127.0.0.1:3306/walmart_sales"
engine = create_engine(DB_URL)

# Load data
df = pd.read_sql("SELECT * FROM walmart_sales_clean", engine, parse_dates=["date"])

# 1) Top 10 Stores
top10 = (df.groupby("store")["weekly_sales"].sum()
           .sort_values(ascending=False)
           .head(10))

top10.plot(kind="bar", figsize=(8,5))
plt.title("Top 10 Stores by Total Sales")
plt.xlabel("Store")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.show()

# 2) Holiday vs Non-Holiday Sales
avg = df.groupby("holiday_flag")["weekly_sales"].mean()
avg.index = ["Non-Holiday","Holiday"]

avg.plot(kind="bar", figsize=(6,4))
plt.title("Average Weekly Sales: Holiday vs Non-Holiday")
plt.ylabel("Average Sales")
plt.tight_layout()
plt.show()

# 3) Overall Weekly Sales Trend
trend = df.groupby("date")["weekly_sales"].sum().reset_index()

plt.figure(figsize=(10,5))
plt.plot(trend["date"], trend["weekly_sales"])
plt.title("Overall Weekly Sales Trend")
plt.xlabel("Date")
plt.ylabel("Total Weekly Sales")
plt.tight_layout()
plt.show()

# 4) Total Sales by Store Type
type_sales = df.groupby("type")["weekly_sales"].sum().sort_values(ascending=False)
type_sales.plot(kind="bar", figsize=(6,4))
plt.title("Total Sales by Store Type")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.show()