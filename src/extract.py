"""
extract.py
-----------
Responsible for downloading or loading raw Olympic datasets.
Outputs: raw/athlete_events.csv, raw/noc_regions.csv
"""

import os
import pandas as pd

# Folder where raw files will be stored
RAW_DIR = "raw"

def ensure_raw_dir():
    """
    Creates the raw data directory if it doesn't exist.
    Prevents errors when saving files.
    """
    os.makedirs(RAW_DIR, exist_ok=True)


def load_local_csv(file_path: str) -> pd.DataFrame:
    """
    Loads a CSV from disk and returns it as a Pandas DataFrame.
    Includes a simple error check for missing files.

    Parameters:
        file_path (str): Path to a CSV file.

    Returns:
        pd.DataFrame: Loaded dataset.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    return pd.read_csv(file_path)


def extract_data():
    """
    Main extraction function:
    - Ensures raw folder exists
    - Loads athlete_events and NOC data locally
    - Saves cleaned raw copies into /raw folder
    """

    ensure_raw_dir()

    # Load raw CSVs (assumes the user downloaded them into /input)
    athlete_events = load_local_csv("input/athlete_events.csv")
    noc_regions = load_local_csv("input/noc_regions.csv")

    # Save into raw directory for consistency in the pipeline
    athlete_events.to_csv(f"{RAW_DIR}/athlete_events.csv", index=False)
    noc_regions.to_csv(f"{RAW_DIR}/noc_regions.csv", index=False)

    print("Raw Olympic datasets extracted successfully.")


if __name__ == "__main__":
    extract_data()