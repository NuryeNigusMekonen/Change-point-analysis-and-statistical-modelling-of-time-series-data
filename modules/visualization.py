import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import arviz as az
import pandas as pd


def plot_price_and_log_returns(df: pd.DataFrame):
    """
    Plot Brent Oil Price and its Log Returns.

    Args:
        df (pd.DataFrame): Must contain 'Date', 'Price', and 'Log_Return' columns.
    """
    fig, axs = plt.subplots(2, 1, figsize=(14, 6))

    axs[0].plot(df["Date"], df["Price"], color='navy')
    axs[0].set_title("Brent Oil Price")
    axs[0].set_ylabel("Price (USD)")
    axs[0].grid(True)

    axs[1].plot(df["Date"], df["Log_Return"], color='darkgreen')
    axs[1].set_title("Log Returns")
    axs[1].set_ylabel("Log Return")
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()


def plot_trace_summary(trace: az.InferenceData):
    """
    Plot trace and posterior summaries for key parameters.

    Args:
        trace (az.InferenceData): MCMC samples from PyMC.
    
    Returns:
        az.Summary: Posterior summary statistics.
    """
    if not isinstance(trace, az.InferenceData):
        raise TypeError("Expected ArviZ InferenceData. Use `return_inferencedata=True` in pm.sample().")

    available_vars = list(trace.posterior.data_vars)
    expected_vars = ["tau", "mu_1", "mu_2", "sigma_1", "sigma_2"]
    present_vars = [v for v in expected_vars if v in available_vars]

    if not present_vars:
        raise ValueError(f"No expected variables found in trace: {expected_vars}")

    # Optional: Thin the trace to speed up plotting (uncomment if needed)
    # trace = trace.sel(draw=slice(None, None, 5))

    az.plot_trace(trace, var_names=present_vars)
    plt.tight_layout()
    plt.show()

    summary = az.summary(trace, var_names=present_vars)
    print(summary)
    return summary


def plot_tau_posterior(trace: az.InferenceData, dates: pd.Series) -> pd.Timestamp:
    """
    Plot the posterior distribution of τ (change point) and return most likely date.

    Args:
        trace (az.InferenceData): Posterior samples from PyMC.
        dates (pd.Series): Date series corresponding to the time series index.
    
    Returns:
        pd.Timestamp: The most probable change point date.
    """
    tau_samples = trace.posterior["tau"].values.flatten()

    plt.figure(figsize=(10, 4))
    plt.hist(tau_samples, bins=50, color='skyblue', edgecolor='k')

    # Find the mode of tau samples using scipy.stats.mode
    mode_tau = stats.mode(tau_samples, keepdims=True).mode[0]

    plt.axvline(mode_tau, color='red', linestyle='--', label=f"Most Likely τ (Index {mode_tau})")
    plt.legend()
    plt.title("Posterior Distribution of Change Point τ")
    plt.xlabel("Index")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()

    return dates.iloc[int(mode_tau)]
