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

    az.plot_trace(trace, var_names=present_vars)
    plt.tight_layout()
    plt.show()

    summary = az.summary(trace, var_names=present_vars)
    print(summary)
    return summary

def plot_tau_posterior(trace: az.InferenceData, dates: pd.Series, var_name="tau") -> pd.Timestamp:
    """
    Plot the posterior distribution of change point variable and return most likely date.

    Args:
        trace (az.InferenceData): Posterior samples from PyMC.
        dates (pd.Series): Date series corresponding to the time series index.
        var_name (str): Name of the change point variable in the trace (default 'tau').

    Returns:
        pd.Timestamp: The most probable change point date.
    """
    if var_name not in trace.posterior.data_vars:
        raise ValueError(f"Variable '{var_name}' not found in trace.posterior")

    cp_samples = trace.posterior[var_name].values.flatten()

    plt.figure(figsize=(10, 4))
    plt.hist(cp_samples, bins=50, color='skyblue', edgecolor='k')

    mode_cp = stats.mode(cp_samples, keepdims=True).mode[0]
    plt.axvline(mode_cp, color='red', linestyle='--', label=f"Most Likely {var_name} (Index {mode_cp})")

    plt.legend()
    plt.title(f"Posterior Distribution of Change Point '{var_name}'")
    plt.xlabel("Index")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()

    return dates.iloc[int(mode_cp)]


def plot_multiple_change_points(trace: az.InferenceData, dates: pd.Series, param="tau"):
    """
    Visualize posterior distributions of multiple change points.

    Args:
        trace (az.InferenceData): Posterior samples.
        dates (pd.Series): Date index for time series.
        param (str): Change point parameter, e.g. 'tau', 'tau_0', 'tau_1', etc.
    """
    tau_vars = [v for v in trace.posterior.data_vars if "tau" in v]

    if not tau_vars:
        raise ValueError("No τ (change point) variables found in trace.")

    plt.figure(figsize=(12, 6))

    for i, var in enumerate(tau_vars):
        tau_values = trace.posterior[var].values.flatten()
        mode_index = stats.mode(tau_values, keepdims=True).mode[0]
        mode_date = dates.iloc[int(mode_index)]

        plt.hist(tau_values, bins=50, alpha=0.5, label=f"{var}: {mode_date.date()}")
        plt.axvline(mode_index, color='black', linestyle='--')

    plt.title("Posterior Distributions of Change Points")
    plt.xlabel("Index")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
