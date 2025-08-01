import numpy as np
import pandas as pd
import arviz as az


def associate_event(change_date, events_df):
    """
    Match the closest global event to a given change point date.
    """
    events_df = events_df.copy()
    events_df["Start_Date"] = pd.to_datetime(events_df["Start_Date"])
    events_df["Delta"] = (events_df["Start_Date"] - change_date).abs()
    closest = events_df.loc[events_df["Delta"].idxmin()]
    return closest.to_dict()


def extract_multiple_change_points(trace: az.InferenceData, date_index: pd.Series):
    """
    Extract multiple change points from posterior samples in a PyMC trace.
    Supports 'tau', 'tau_pos', and 'cp' depending on model type.
    """
    # Dynamically find the change point key
    possible_keys = ["tau", "tau_pos", "cp"]
    cp_key = next((k for k in possible_keys if k in trace.posterior), None)

    if cp_key is None:
        raise KeyError("No change point variable found in trace. Expected one of: 'tau', 'tau_pos', or 'cp'.")

    tau_samples = trace.posterior[cp_key].values  # shape: (chains, draws) or (chains, draws, max_cp)

    # Ensure shape is always (chains, draws, N) for consistency
    if tau_samples.ndim == 2:
        tau_samples = tau_samples[:, :, np.newaxis]  # for models with one cp

    max_cp = tau_samples.shape[-1]
    tau_means = tau_samples.mean(axis=(0, 1))  # average over chains and draws
    tau_indices = sorted(set([int(round(t)) for t in tau_means if 0 <= int(round(t)) < len(date_index)]))
    
    return [date_index.iloc[i] for i in tau_indices]


def generate_insights(change_dates, events_df):
    """
    For each change date, associate the most relevant global event and package insight.
    """
    insights = []
    for change_date in change_dates:
        event = associate_event(change_date, events_df)
        insights.append({
            "Change_Point": change_date,
            "Event": event["Event"],
            "Event_Date": event["Start_Date"],
            "Days_Offset": abs((event["Start_Date"] - change_date).days),
            "Notes": event.get("Notes", ""),
            "Type": event.get("Type", ""),
            "Region": event.get("Region", "")
        })
    return insights


def quantify_impact_mean_shift(trace):
    """
    Quantify impact for Bayesian mean shift model.
    Returns mean before change, mean after last change, and percent change.
    """
    mu_samples = trace.posterior["mu"].values  # shape: (chains, draws, segments)
    mu_means = mu_samples.mean(axis=(0, 1))     # average across chains and draws

    mean_before = mu_means[0]
    mean_after = mu_means[-1]

    pct_change = 100 * (mean_after - mean_before) / abs(mean_before) if mean_before != 0 else np.nan
    return mean_before, mean_after, pct_change


def quantify_impact_trend(trace, data_length):
    """
    Quantify impact for Bayesian trend change model.
    Returns slope before and after change point and their difference.
    """
    a1_samples = trace.posterior["a1"].values.flatten()
    a2_samples = trace.posterior["a2"].values.flatten()
    cp_samples = trace.posterior["cp"].values.flatten()

    cp_median = int(np.median(cp_samples))

    slope_before = np.mean(a1_samples)
    slope_after = np.mean(a2_samples)
    slope_diff = slope_after - slope_before

    return slope_before, slope_after, slope_diff, cp_median


def quantify_impact_variance_shift(trace):
    """
    Quantify impact for Bayesian variance shift model.
    Returns variance before and after change point, and percent change.
    """
    sigma1_samples = trace.posterior["sigma1"].values.flatten()
    sigma2_samples = trace.posterior["sigma2"].values.flatten()

    var_before = np.mean(sigma1_samples ** 2)
    var_after = np.mean(sigma2_samples ** 2)

    pct_change = 100 * (var_after - var_before) / var_before if var_before != 0 else np.nan
    return var_before, var_after, pct_change
