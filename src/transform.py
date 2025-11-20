# transform.py
import pandas as pd

def filter_usa(df):
    """
    Keep only USA athletes.
    """
    df_usa = df[df["NOC"] == "USA"].copy()
    return df_usa

def clean_columns(df):
    """
    Basic column cleanup (lowercase, strip spaces).
    """
    df.columns = df.columns.str.strip().str.lower()
    return df

if __name__ == "__main__":
    from extract import load_raw_data
    df = load_raw_data()
    if df is not None:
        df = filter_usa(df)
        df = clean_columns(df)
        print(df.head())
