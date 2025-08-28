import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Default raw data directory (can be overridden by .env)
RAW_DIR = os.getenv("RAW_DIR", "./data/raw")

def load_csv_safe(filename: str, **kwargs) -> pd.DataFrame:
    """
    Load a CSV file from the raw data directory with safe defaults.
    Parameters:
        filename (str): Name of the CSV file (e.g., "stores.csv")
        kwargs: Additional arguments for pandas.read_csv
    Returns:
        pd.DataFrame: Loaded dataframe
    """
    path = os.path.join(RAW_DIR, filename)
    df = pd.read_csv(path, low_memory=False, **kwargs)
    return df

def extract():
    """
    Extract raw datasets:
    - stores.csv
    - train.csv
    - features.csv
    Also standardize column names to lowercase for consistency.
    Returns:
        Tuple of (stores, train, features) DataFrames
    """
    stores = load_csv_safe("stores.csv")
    train = load_csv_safe("train.csv")
    features = load_csv_safe("features.csv")

    # Normalize column names to lowercase
    stores.columns = [c.strip().lower() for c in stores.columns]
    train.columns = [c.strip().lower() for c in train.columns]
    features.columns = [c.strip().lower() for c in features.columns]
    return stores, train, features

if __name__ == "__main__":
    # Run extraction and print dataset sizes
    s, t, f = extract()
    print(len(s), len(t), len(f))