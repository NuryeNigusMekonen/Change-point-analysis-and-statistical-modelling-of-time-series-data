import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller

def compute_log_returns(df):
    df = df.copy()
    df["Log_Return"] = np.log(df["Price"]) - np.log(df["Price"].shift(1))
    return df.dropna()

def check_stationarity(series):
    result = adfuller(series.dropna())
    return {
        "ADF Statistic": result[0],
        "p-value": result[1],
        "Used Lag": result[2],
        "Number of Observations": result[3],
        "Critical Values": result[4],
        "Conclusion": "Stationary" if result[1] < 0.05 else "Non-stationary"
    }
