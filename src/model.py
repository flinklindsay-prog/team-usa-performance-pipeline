# model.py
import pandas as pd

def aggregate_medals(df):
    """
    Create a summary table: year, sport, total athletes, medal counts.
    """
    df_summary = df.groupby(["year", "sport"]).agg(
        total_athletes=("name", "nunique"),
        gold_count=("medal", lambda x: sum(x=="Gold")),
        silver_count=("medal", lambda x: sum(x=="Silver")),
        bronze_count=("medal", lambda x: sum(x=="Bronze")),
        avg_age=("age", "mean")
    ).reset_index()
    return df_summary

if __name__ == "__main__":
    from transform import filter_usa, clean_columns
    from extract import load_raw_data

    df = load_raw_data()
    if df is not None:
        df = filter_usa(df)
        df = clean_columns(df)
        df_summary = aggregate_medals(df)
        print(df_summary.head())
        df_summary.to_csv("data/processed/team_usa_model.csv", index=False)
