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

def quantify_impact(trace):
    """
    Quantify change in mean parameters before and after the change point.

    Args:
        trace (arviz.InferenceData): Posterior samples from PyMC v4.

    Returns:
        tuple: (mean_before, mean_after, percent_change)
    """
    mu_1_samples = trace.posterior["mu_1"].values.flatten()
    mu_2_samples = trace.posterior["mu_2"].values.flatten()
    mean_before = np.mean(mu_1_samples)
    mean_after = np.mean(mu_2_samples)
    pct_change = ((mean_after - mean_before) / abs(mean_before)) * 100 if mean_before != 0 else np.nan
    return mean_before, mean_after, pct_change
