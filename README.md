{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "35e9bfd7-2078-498f-a073-a523a20969a5",
   "metadata": {},
   "source": [
    "Walmart Sales Analysis – ETL & Insights"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "8456d2df-7184-4d04-a1b1-c0aa864cac6a",
   "metadata": {},
   "source": [
    "1. Project Background"
   ]
  },
  {
   "cell_type": "raw",
   "id": "af8868e8-379d-41a0-b871-303b29eebc10",
   "metadata": {},
   "source": [
    "Walmart is the world’s largest retailer. Analyzing its sales data can help us:\n",
    "\n",
    "Understand how holidays, store types, and economic factors affect sales\n",
    "\n",
    "Build forecasting models to optimize inventory and marketing strategies\n",
    "\n",
    "Demonstrate a full ETL → Data Warehouse → Analysis → Visualization workflow\n",
    "\n",
    "Dataset: Kaggle – Walmart Store Sales Forecasting"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "fac8b9f4-3bab-4f59-bde1-a8460fcb1599",
   "metadata": {},
   "source": [
    "2. Project Structure"
   ]
  },
  {
   "cell_type": "raw",
   "id": "4333ce4b-a0cb-4587-8758-5e57dff26b97",
   "metadata": {},
   "source": [
    "walmart_project\n",
    "    data\n",
    "        raw            # Raw datasets (stores.csv, train.csv, features.csv)\n",
    "        processed      # Cleaned data (walmart_sales_clean.csv)\n",
    "    etl\n",
    "        extract.py     # Data extraction\n",
    "        transform.py   # Data cleaning & merging\n",
    "        load.py        # Export to CSV & MySQL\n",
    "        pipeline.py    # Run ETL pipeline\n",
    "        analysis.py    # Visualization & advanced analysis\n",
    "    sql\n",
    "        create_views.sql   # SQL views\n",
    "        validate.sql       # SQL data validation\n",
    "    README.md"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "85cbb19c-37dc-460a-99f6-88284aeecf17",
   "metadata": {},
   "source": [
    "3. Tech Stack"
   ]
  },
  {
   "cell_type": "raw",
   "id": "7d4bbc70-c2f5-44f2-a7a0-bea34a8b42df",
   "metadata": {},
   "source": [
    "Language: Python (pandas, matplotlib, SQLAlchemy), SQL\n",
    "\n",
    "Database: MySQL\n",
    "\n",
    "Tools: PyCharm, MySQL Workbench, Jupyter Notebook\n",
    "\n",
    "Env Management: .env file for DB connection (DB_URL, paths, etc.)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "1c107dac-b772-47cc-9b3b-5e47ba9d41dd",
   "metadata": {},
   "source": [
    "4. ETL Workflow"
   ]
  },
  {
   "cell_type": "raw",
   "id": "cd479024-e543-4d46-866f-d0653d8f1566",
   "metadata": {},
   "source": [
    "1. Extract: Read raw CSVs (stores.csv, train.csv, features.csv)\n",
    "\n",
    "2. Transform:\n",
    "\n",
    "Merge datasets\n",
    "\n",
    "Standardize column names and parse dates\n",
    "\n",
    "Derived fields: year, month, week, holiday_flag, sales_per_size\n",
    "\n",
    "Filter negative sales and handle missing values\n",
    "\n",
    "3. Load:\n",
    "\n",
    "Save cleaned data to data/processed/walmart_sales_clean.csv\n",
    "\n",
    "Load into MySQL table walmart_sales_clean\n",
    "\n",
    "4. Validate:\n",
    "\n",
    "Check primary key uniqueness (store, dept, date)\n",
    "\n",
    "Check for negative values, missing values, and date range\n",
    "\n",
    "Ensure row counts match"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "7892552a-cbfd-4cf2-80ce-5202f2f1702b",
   "metadata": {},
   "source": [
    "5. Database Views"
   ]
  },
  {
   "cell_type": "raw",
   "id": "362271a1-c4fa-4588-b349-658f61f951a2",
   "metadata": {},
   "source": [
    "Defined in sql/create_views.sql:\n",
    "\n",
    "vw_sales_daily → daily aggregated sales trend\n",
    "\n",
    "vw_store_rank → store-level total sales ranking\n",
    "\n",
    "vw_type_sales → store type performance"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "a6ad19c6-8d30-4a9b-a17c-2338e62ca387",
   "metadata": {},
   "source": [
    "6. Key Insights"
   ]
  },
  {
   "cell_type": "raw",
   "id": "5adfa8f6-af03-40fc-94f7-5d0570135188",
   "metadata": {},
   "source": [
    "A. Top 10 Stores\n",
    "\n",
    "Store 20 recorded the highest total sales (~40M+)\n",
    "\n",
    "Top 10 stores contributed 35%+ of overall sales\n",
    "\n",
    "B. Holiday vs Non-Holiday\n",
    "\n",
    "Average weekly sales during holidays ≈ 11,000\n",
    "\n",
    "~15% higher compared to non-holiday weeks\n",
    "\n",
    "C. Overall Trend\n",
    "\n",
    "Strong seasonality observed\n",
    "\n",
    "Peaks in November–December, dips in January–February\n",
    "\n",
    "D. Store Types\n",
    "\n",
    "Type A stores (large stores) lead in total sales\n",
    "\n",
    "Type B stores follow\n",
    "\n",
    "Type C stores have limited contribution"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "9fb03e46-b9af-4f2b-93f8-13be89928dfb",
   "metadata": {},
   "source": [
    "7. Data Quality Checks"
   ]
  },
  {
   "cell_type": "raw",
   "id": "14b742d1-d286-4456-93e6-1922135a23ea",
   "metadata": {},
   "source": [
    "Validation (sql/validate.sql or etl/validate.py):\n",
    "\n",
    "Primary key (store, dept, date) is unique\n",
    "\n",
    "No negative sales values\n",
    "\n",
    "Date range: 2010-02-05 ~ 2012-10-26\n",
    "\n",
    "No critical missing values"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
