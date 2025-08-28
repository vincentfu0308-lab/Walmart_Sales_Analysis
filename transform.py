import pandas as pd

def to_date(df: pd.DataFrame, col: str):
    """
    Convert a column in a DataFrame to datetime.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    col : str
        Column name to be converted to datetime.

    Returns
    -------
    pd.DataFrame
        DataFrame with the specified column converted to datetime.
    """
    df[col] = pd.to_datetime(df[col], errors="coerce")
    return df

def transform(stores: pd.DataFrame, train: pd.DataFrame, features: pd.DataFrame) -> pd.DataFrame:
    """
    Transform raw Walmart datasets into a clean, analysis-ready DataFrame.

    Steps:
    1. Convert date columns to datetime.
    2. Merge train (sales) data with features (economic indicators, holidays).
    3. Merge with store-level metadata.
    4. Filter out invalid sales (nulls or negatives).
    5. Add derived fields: year, month, week, holiday_flag, sales_per_size.
    6. Reorder and select final columns.

    Parameters
    ----------
    stores : pd.DataFrame
        Store metadata (store type, size).
    train : pd.DataFrame
        Sales data (store, dept, date, weekly_sales).
    features : pd.DataFrame
        External features (fuel_price, cpi, unemployment, isholiday).

    Returns
    -------
    pd.DataFrame
        Cleaned and merged dataset ready for loading/analysis.
    """

    # 1. Ensure date columns are proper datetime
    train = to_date(train, "date")
    features = to_date(features, "date")

    # 2. Merge sales data with features (per store-date)
    tf = train.merge(
        features.drop_duplicates(subset=["store", "date"]),
        on=["store", "date"],
        how="left",
        suffixes=("", "_feat")
    )

    # 3. Merge with store metadata
    full = tf.merge(
        stores.drop_duplicates(subset=["store"]),
        on="store",
        how="left"
    )

    # 4. Filter invalid rows (remove null or negative sales)
    full = full[full["weekly_sales"].notna()]
    full = full[full["weekly_sales"] >= 0]

    # 5. Add derived features
    full["year"] = full["date"].dt.year
    full["month"] = full["date"].dt.month
    full["week"] = full["date"].dt.isocalendar().week.astype(int)
    full["holiday_flag"] = full.get("isholiday", False).astype(int)

    # Sales normalized by store size (per square foot/meter)
    if "size" in full.columns:
        full["sales_per_size"] = (full["weekly_sales"] / full["size"]).fillna(0)
    else:
        full["sales_per_size"] = None

    # 6. Final selected columns
    cols = [
        "store","dept","date","weekly_sales","isholiday","temperature",
        "fuel_price","cpi","unemployment","type","size",
        "year","month","week","holiday_flag","sales_per_size"
    ]
    cols = [c for c in cols if c in full.columns]

    # Sort for consistency
    return full[cols].sort_values(["store","dept","date"]).reset_index(drop=True)