# src/transform.py
import pandas as pd
from pathlib import Path
from extract import load_raw_data

PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = PROCESSED_DIR / "clean_athletes.csv"

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    # strip whitespace, lowercase, replace spaces with underscore
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df

def standardize_medal(df: pd.DataFrame) -> pd.DataFrame:
    # convert empty string / NaN to 'None' and capitalize
    df["medal"] = df["medal"].fillna("None")
    df["medal"] = df["medal"].replace("", "None")
    # ensure standardized capitalization
    df["medal"] = df["medal"].apply(lambda x: x.title() if isinstance(x, str) else x)
    return df

def coerce_types(df: pd.DataFrame) -> pd.DataFrame:
    # Year to int, Age to numeric (coerce)
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df["age"] = pd.to_numeric(df["age"], errors="coerce").astype("Float64")
    return df

def filter_team_usa(df: pd.DataFrame) -> pd.DataFrame:
    # Some datasets use 'team' or 'noc' columns; use NOC if present
    if "noc" in df.columns:
        df_usa = df[df["noc"] == "USA"].copy()
    else:
        # fallback: team column containing 'United States' or 'USA'
        df_usa = df[df["team"].astype(str).str.contains("United State|USA", na=False)].copy()
    return df_usa

def select_and_order_columns(df: pd.DataFrame) -> pd.DataFrame:
    # choose relevant columns for modeling/ad-hoc analysis
    cols = [
        "id", "name", "sex", "age", "height", "weight", "team", "noc",
        "games", "year", "season", "city", "sport", "event", "medal"
    ]
    available = [c for c in cols if c in df.columns]
    return df[available]

def run_transform_and_save(out_path=OUT_PATH):
    df = load_raw_data()
    df = normalize_columns(df)
    df = filter_team_usa(df)
    df = standardize_medal(df)
    df = coerce_types(df)
    df = select_and_order_columns(df)
    # optional: ensure medal values are exactly one of Gold/Silver/Bronze/None
    df["medal"] = df["medal"].where(df["medal"].isin(["Gold", "Silver", "Bronze", "None"]), "None")
    df.to_csv(out_path, index=False)
    print(f"[transform] Wrote {len(df):,} rows to {out_path}")
    return df

if __name__ == "__main__":
    df_clean = run_transform_and_save()
    print(df_clean.head())
    print(df_clean.dtypes)
