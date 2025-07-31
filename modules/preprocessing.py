import numpy as np
import pandas as pd

def compute_log_returns(df, price_col="Price"):
    """
    Compute log returns from price data.
    Args:
        df (pd.DataFrame): DataFrame with price column.
        price_col (str): Price column name.
    Returns:
        pd.DataFrame: DataFrame with added 'Log_Return' column and dropped NA.
    """
    df = df.copy()
    df["Log_Return"] = np.log(df[price_col]) - np.log(df[price_col].shift(1))
    return df.dropna()
