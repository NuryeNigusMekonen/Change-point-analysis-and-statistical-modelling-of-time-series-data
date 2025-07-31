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

def associate_multiple_events(change_dates, events_df):
    """
    Map a list of change point dates to their closest events.

    Args:
        change_dates (List[pd.Timestamp]): List of change point dates.
        events_df (pd.DataFrame): Event dataframe.

    Returns:
        List[dict]: List of event dicts.
    """
    return [associate_event(cd, events_df) for cd in change_dates]

def extract_multiple_change_points(trace, date_index, num_changes=2):
    """
    Extract multiple change points from posterior.

    Args:
        trace (arviz.InferenceData): PyMC trace.
        date_index (pd.Series): Timestamps for each observation.
        num_changes (int): Number of change points used in model.

    Returns:
        List[pd.Timestamp]: Most probable change point dates.
    """
    taus = trace.posterior["taus"].values  # shape: (chains, draws, num_changes)
    taus_mean = taus.mean(axis=(0, 1))  # Average over chains and draws
    tau_indices = np.round(taus_mean).astype(int)
    change_dates = [date_index[idx] for idx in tau_indices]
    return change_dates

def quantify_impact(trace):
    """
    Quantify change in mean parameters before and after the change points.

    Args:
        trace (arviz.InferenceData): Posterior samples from PyMC v4.

    Returns:
        list of tuples: Each tuple contains (mean_before, mean_after, percent_change)
    """
    mu_samples = trace.posterior["mus"].values  # shape: (chains, draws, segments)
    means = mu_samples.mean(axis=(0, 1))  # segment means
    impacts = []
    for i in range(len(means) - 1):
        before = means[i]
        after = means[i + 1]
        pct_change = ((after - before) / abs(before)) * 100 if before != 0 else np.nan
        impacts.append((before, after, pct_change))
    return impacts
