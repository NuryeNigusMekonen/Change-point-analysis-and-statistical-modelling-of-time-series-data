import pandas as pd
import os

def load_key_events(csv_path="data/key_events.csv") -> pd.DataFrame:
    """
    Load and preprocess key geopolitical/economic events from a CSV file.

    Args:
        csv_path (str): Path to the key events CSV file.

    Returns:
        pd.DataFrame: Cleaned and sorted events DataFrame with datetime columns.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Key events file not found at path: {csv_path}")

    df = pd.read_csv(csv_path)

    # Basic cleanup
    required_cols = {"Event", "Start_Date", "Region", "Type", "Notes"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"CSV is missing one or more required columns: {required_cols}")

    # Convert date columns
    df["Start_Date"] = pd.to_datetime(df["Start_Date"], errors="coerce")
    df = df.dropna(subset=["Start_Date"])  # Remove rows with invalid dates

    # Sort chronologically
    df = df.sort_values("Start_Date").reset_index(drop=True)
    # print the event is imported 
    print(f"Loaded {len(df)} key events from {csv_path}")
    
    return df
