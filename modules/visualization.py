import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import arviz as az

def plot_price_and_log_returns(df):
    """
    Plot Brent Oil Price and its Log Returns over time.
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

def plot_trace_summary(trace):
    """
    Plot trace and summary statistics using ArviZ from a PyMC v4 model.
    """
    if not isinstance(trace, az.InferenceData):
        raise TypeError("Expected ArviZ InferenceData. Use `return_inferencedata=True` in pm.sample().")

    # Check which variables are present
    available_vars = list(trace.posterior.data_vars)
    expected_vars = ["tau", "mu_1", "mu_2", "sigma"]
    present_vars = [v for v in expected_vars if v in available_vars]

    if not present_vars:
        raise ValueError(f"None of the expected vars {expected_vars} found in trace.")

    az.plot_trace(trace, var_names=present_vars)
    plt.tight_layout()
    plt.show()

    summary = az.summary(trace, var_names=present_vars)
    print(summary)
    return summary


def plot_tau_posterior(trace, dates):
    """
    Plot the posterior distribution of the change point τ.

    Args:
        trace (arviz.InferenceData): Posterior samples
        dates (pd.Series): Corresponding dates to index

    Returns:
        pd.Timestamp: Date corresponding to the most probable change point
    """
    if not isinstance(trace, az.InferenceData):
        raise TypeError("Expected ArviZ InferenceData.")

    tau_samples = trace.posterior["tau"].values.flatten()
    
    plt.figure(figsize=(10, 4))
    plt.hist(tau_samples, bins=50, color='skyblue', edgecolor='k')
    mode_tau = stats.mode(tau_samples, keepdims=True)[0][0]

    plt.axvline(mode_tau, color='red', linestyle='--', label=f"Most Likely τ (Index {mode_tau})")
    plt.legend()
    plt.title("Posterior Distribution of Change Point τ")
    plt.xlabel("Index (Days)")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()

    return dates[int(mode_tau)]

