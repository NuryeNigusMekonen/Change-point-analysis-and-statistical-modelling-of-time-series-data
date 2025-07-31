import pandas as pd
from modules.logger import get_logger
logger = get_logger()

def load_brent_data(filepath):
    try:
        df = pd.read_csv(filepath)
        assert "Date" in df.columns and "Price" in df.columns
        df["Date"] = pd.to_datetime(df["Date"], format="%d-%b-%y", errors='coerce')
        df.dropna(subset=["Date", "Price"], inplace=True)
        df.sort_values("Date", inplace=True)
        logger.info(f"Loaded Brent data: {df.shape[0]} rows.")
        return df
    except Exception as e:
        logger.error(f"Failed to load Brent data: {e}")
        raise
