# extract.py
import pandas as pd

def load_raw_data(filepath="data/raw/athlete_events.csv"):
    """
    Load the raw Olympic dataset into a DataFrame.
    """
    try:
        df = pd.read_csv(filepath)
        print(f"Loaded {len(df)} rows from {filepath}")
        return df
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None

if __name__ == "__main__":
    df = load_raw_data()
    print(df.head())
