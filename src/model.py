# src/model.py
"""
MODEL STEP
This script takes the cleaned USA-only Olympic dataset (produced in the transform step)
and builds an aggregated, analysis-ready dataset with metrics grouped by:

    • year
    • sport

The output is used for Tableau visualizations and downstream analytics.
"""

import pandas as pd
from pathlib import Path

# -----------------------------
# File paths used in the model
# -----------------------------

# Input file produced by transform.py
INPUT_PATH = Path("data/processed/clean_athletes.csv")

# Ensure processed directory exists for writing output
OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Final modeling output file
OUTPUT_PATH = OUTPUT_DIR / "team_usa_model.csv"


# ------------------------------------------------------
# Load the cleaned dataset created in the transform step
# ------------------------------------------------------
def load_clean_data(path: Path = INPUT_PATH) -> pd.DataFrame:
    """
    Load the cleaned USA-only athletes dataset.
    Raises an error if the file is missing so failures are obvious.
    """
    if not path.exists():
        raise FileNotFoundError(
            f"Clean dataset not found. Expected at: {path.resolve()}"
        )

    df = pd.read_csv(path)
    print(f"[model] Loaded {len(df):,} rows from {path}")
    return df


# ----------------------------------------------------------------------
# Core transformation logic: aggregate metrics by year + sport
# ----------------------------------------------------------------------
def compute_aggregations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes athlete-level data and computes aggregated metrics
    for each combination of (year, sport).
    """

    # Ensure year is numeric — invalid values become NaN
    # Then cast to Pandas' nullable Int64 type (supports missing values)
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")

    # Group rows into year/sport buckets and compute metrics inside each group
    grouped = (
        df.groupby(["year", "sport"], dropna=True)
        .agg(
            # Number of unique athletes participating in that sport/year
            total_athletes=("name", "nunique"),

            # Count medals by type (Gold, Silver, Bronze)
            gold_count=("medal", lambda x: (x == "Gold").sum()),
            silver_count=("medal", lambda x: (x == "Silver").sum()),
            bronze_count=("medal", lambda x: (x == "Bronze").sum()),

            # Count any medal type
            medal_count=("medal", lambda x: x.isin(["Gold", "Silver", "Bronze"]).sum()),

            # Average athlete age for the sport/year grouping
            avg_age=("age", "mean"),
        )
        .reset_index()                 # Convert grouping index back to regular columns
        .sort_values(["year", "sport"])  # Sort for readability and consistency
    )

    return grouped


# ------------------------------------
# Save the output aggregated dataset
# ------------------------------------
def save_output(df: pd.DataFrame, path: Path = OUTPUT_PATH):
    """
    Write model output to CSV.
    """
    df.to_csv(path, index=False)
    print(f"[model] Wrote {len(df):,} aggregated rows → {path}")


# ---------------------------------------------------
# Orchestration function: run the entire model step
# ---------------------------------------------------
def run_model():
    """
    High-level function that:
      1. Loads clean data
      2. Computes aggregations
      3. Saves the final model output
    """
    df_clean = load_clean_data()
    df_model = compute_aggregations(df_clean)
    save_output(df_model)

    # Print first 10 rows for a quick sanity check
    print(df_model.head(10))
    return df_model


# ---------------------------------------------------
# Script entry point
# Allows running:  python src/model.py
# ---------------------------------------------------
if __name__ == "__main__":
    run_model()