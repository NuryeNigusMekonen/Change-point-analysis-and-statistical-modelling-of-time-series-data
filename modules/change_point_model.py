import pymc as pm
import numpy as np
import logging
import arviz as az

logger = logging.getLogger(__name__)


def build_change_point_model(data: np.ndarray) -> pm.Model:
    """
    Build a Bayesian change point model using PyMC with separate means and stds before and after τ.

    Args:
        data (np.ndarray): 1D array of time series data (e.g., log returns or other metric).

    Returns:
        pm.Model: A compiled PyMC model object.
    """
    n = len(data)
    if n < 10:
        raise ValueError("Data too short to estimate a change point reliably.")

    idx = np.arange(n)

    with pm.Model() as model:
        # Define the switch point (change point τ)
        tau = pm.DiscreteUniform("tau", lower=5, upper=n - 5)

        # Prior distributions for means
        mu_1 = pm.Normal("mu_1", mu=np.mean(data), sigma=2 * np.std(data))
        mu_2 = pm.Normal("mu_2", mu=np.mean(data), sigma=2 * np.std(data))

        # Prior distributions for standard deviations
        sigma_1 = pm.HalfNormal("sigma_1", sigma=np.std(data))
        sigma_2 = pm.HalfNormal("sigma_2", sigma=np.std(data))

        # Mean and standard deviation based on the change point
        mu = pm.Deterministic("mu", pm.math.switch(idx < tau, mu_1, mu_2))
        sigma = pm.Deterministic("sigma", pm.math.switch(idx < tau, sigma_1, sigma_2))

        # Likelihood function
        pm.Normal("obs", mu=mu, sigma=sigma, observed=data)

    logger.info("PyMC change point model successfully built.")
    return model


def sample_model(
    model: pm.Model,
    draws: int = 3000,
    tune: int = 1500,
    target_accept: float = 0.95,
    chains: int = 4,
    cores: int = 4,
    random_seed: int = 42
) -> az.InferenceData:
    """
    Sample from the posterior distribution using NUTS.

    Args:
        model (pm.Model): The PyMC model.
        draws (int): Number of posterior samples.
        tune (int): Number of tuning steps.
        target_accept (float): Target acceptance probability.
        chains (int): Number of MCMC chains.
        cores (int): Number of parallel CPU cores to use.
        random_seed (int): Random seed for reproducibility.

    Returns:
        az.InferenceData: Inference results from sampling.
    """
    try:
        with model:
            trace = pm.sample(
                draws=draws,
                tune=tune,
                target_accept=target_accept,
                chains=chains,
                cores=cores,
                return_inferencedata=True,
                random_seed=random_seed
            )

        logger.info("Sampling completed successfully.")
        return trace
    except Exception as e:
        logger.error(f"Sampling failed: {e}")
        raise
