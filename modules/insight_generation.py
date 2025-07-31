import numpy as np
import pandas as pd
import arviz as az

def associate_event(change_date, events_df):
    """
    Find the closest event in time to the detected change point date.

    Args:
        change_date (pd.Timestamp): Detected change point date.
        events_df (pd.DataFrame): Events with 'Start_Date' column as datetime.

    Returns:
        dict: Closest event info.
    """
    events_df = events_df.copy()
    events_df["Start_Date"] = pd.to_datetime(events_df["Start_Date"])
    events_df["Delta"] = (events_df["Start_Date"] - change_date).abs()
    closest = events_df.loc[events_df["Delta"].idxmin()]
    return closest.to_dict()


def extract_single_change_point(trace: az.InferenceData, date_index: pd.Series) -> pd.Timestamp:
    """
    Extract the most probable single change point from the posterior.

    Args:
        trace (arviz.InferenceData): PyMC trace with 'tau' variable.
        date_index (pd.Series): Date/time index for the observations.

    Returns:
        pd.Timestamp: Most probable change point date.
    """
    tau_samples = trace.posterior["tau"].values  # shape: (chains, draws)
    tau_mean = tau_samples.mean(axis=(0, 1))     # average over chains and draws
    tau_idx = int(round(tau_mean))
    return date_index.iloc[tau_idx]


def quantify_impact(trace: az.InferenceData):
    """
    Quantify change in mean parameters before and after the single change point.

    Args:
        trace (arviz.InferenceData): Posterior samples from PyMC with 'mu_1' and 'mu_2'.

    Returns:
        tuple: (mean_before, mean_after, percent_change)
    """
    mu_1_samples = trace.posterior["mu_1"].values  # shape: (chains, draws)
    mu_2_samples = trace.posterior["mu_2"].values

    mean_before = mu_1_samples.mean()
    mean_after = mu_2_samples.mean()

    pct_change = ((mean_after - mean_before) / abs(mean_before)) * 100 if mean_before != 0 else float('nan')
    return mean_before, mean_after, pct_change
