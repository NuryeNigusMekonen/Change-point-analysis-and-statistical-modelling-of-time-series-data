import pandas as pd
from modules.logger import get_logger
logger = get_logger()

def load_event_data(filepath):
    try:
        df = pd.read_csv(filepath)
        assert {"Event", "Start_Date"}.issubset(df.columns)
        df["Start_Date"] = pd.to_datetime(df["Start_Date"], errors='coerce')
        df.dropna(subset=["Start_Date"], inplace=True)
        logger.info(f"Loaded event data: {df.shape[0]} rows.")
        return df
    except Exception as e:
        logger.error(f"Failed to load event data: {e}")
        raise
