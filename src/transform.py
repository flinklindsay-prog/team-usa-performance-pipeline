"""
transform.py
-------------
Cleans and transforms the raw Olympic datasets.
Outputs: processed/olympics_cleaned.csv
"""

import os
import pandas as pd

RAW_DIR = "raw"
PROCESSED_DIR = "processed"


def ensure_processed_dir():
    """
    Creates the processed data directory if it doesn't exist.
    """
    os.makedirs(PROCESSED_DIR, exist_ok=True)


def load_raw_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Loads the raw Olympic datasets from the /raw directory.

    Returns:
        (pd.DataFrame, pd.DataFrame): athlete_events, noc_regions
    """

    athlete_events = pd.read_csv(f"{RAW_DIR}/athlete_events.csv")
    noc_regions = pd.read_csv(f"{RAW_DIR}/noc_regions.csv")

    return athlete_events, noc_regions


def clean_athlete_events(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies cleaning steps to athlete_events.csv:
    - Standardizes missing values
    - Converts data types
    - Handles inconsistent text fields

    Parameters:
        df (pd.DataFrame): Raw athlete events dataset

    Returns:
        pd.DataFrame: Cleaned dataset
    """

    # Replace known missing markers
    df.replace({"NA": None, "N/A": None, "": None}, inplace=True)

    # Convert numeric columns safely
    numeric_cols = ["Age", "Height", "Weight", "Year"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Standardize string columns
    df["Name"] = df["Name"].str.strip()
    df["Sex"] = df["Sex"].str.upper()
    df["Season"] = df["Season"].str.title()  # Summer/Winter
    df["City"] = df["City"].str.title()

    return df


def merge_noc_regions(athletes: pd.DataFrame, noc: pd.DataFrame) -> pd.DataFrame:
    """
    Merges athlete data with NOC region information.
    Adds a 'Region' column for each athlete.

    Parameters:
        athletes (pd.DataFrame): Clean athlete events data
        noc (pd.DataFrame): NOC region mappings

    Returns:
        pd.DataFrame: Merged dataset
    """

    merged = athletes.merge(
        noc,
        how="left",
        left_on="NOC",
        right_on="NOC"  # ensures NOC codes match
    )

    return merged


def transform_data():
    """
    Main transformation function:
    - Loads raw data
    - Cleans athlete events dataset
    - Joins NOC region info
    - Saves final processed file
    """

    ensure_processed_dir()

    # Load source datasets
    athlete_events, noc_regions = load_raw_data()

    # Clean main table
    athlete_clean = clean_athlete_events(athlete_events)

    # Merge NOC data
    final_df = merge_noc_regions(athlete_clean, noc_regions)

    # Save processed version
    final_df.to_csv(f"{PROCESSED_DIR}/olympics_cleaned.csv", index=False)

    print("Olympic dataset transformed and saved successfully.")


if __name__ == "__main__":
    transform_data()