# src/extract.py
import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/athlete_events.csv")

def load_raw_data(filepath: Path = RAW_PATH):
    """
    Load the raw Olympic dataset into a pandas DataFrame.
    Returns DataFrame or raises FileNotFoundError.
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Raw data not found at {filepath.resolve()}")
    df = pd.read_csv(filepath)
    print(f"[extract] Loaded {len(df):,} rows from {filepath}")
    return df

if __name__ == "__main__":
    df = load_raw_data()
    print(df.columns.tolist())
    print(df.head(3))
