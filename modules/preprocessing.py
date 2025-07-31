import numpy as np
import pandas as pd

def compute_log_returns(df, price_col="Price"):
    """
    Compute log returns from price data.
    
    Args:
        df (pd.DataFrame): DataFrame with a price column.
        price_col (str): Name of the column with price/time-series values.
        
    Returns:
        pd.DataFrame: DataFrame with added 'Log_Return' column and dropped NA rows.
    """
    df = df.copy()
    df["Log_Return"] = np.log(df[price_col] / df[price_col].shift(1))
    return df.dropna()

def preprocess_time_series(df, value_col="sentiment_score", date_col="date"):
    """
    Basic preprocessing for time series data.
    
    Args:
        df (pd.DataFrame): Raw time series data with date and value columns.
        value_col (str): Column name for values (e.g. sentiment_score).
        date_col (str): Column name for the datetime column.
    
    Returns:
        pd.DataFrame: Preprocessed time series with datetime index and sorted.
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df = df[[date_col, value_col]].dropna()
    df = df.sort_values(date_col)
    df.set_index(date_col, inplace=True)
    df = df.asfreq("D")  # Ensure daily frequency (can be parameterized)
    df.fillna(method="ffill", inplace=True)
    return df
