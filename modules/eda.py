# modules/eda.py

import matplotlib.pyplot as plt
import numpy as np

def plot_price_trend(df):
    plt.figure(figsize=(14, 5))
    plt.plot(df["Date"], df["Price"], label="Brent Oil Price", color="darkblue")
    plt.title("Brent Oil Price Over Time")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_log_returns(df):
    df = df.copy()
    df["Log_Return"] = np.log(df["Price"]) - np.log(df["Price"].shift(1))
    plt.figure(figsize=(14, 4))
    plt.plot(df["Date"], df["Log_Return"], color="darkgreen")
    plt.title("Log Returns of Brent Oil Price")
    plt.xlabel("Date")
    plt.ylabel("Log Return")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
