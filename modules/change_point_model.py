import pymc as pm
import numpy as np
import logging
import arviz as az

logger = logging.getLogger(__name__)

def build_change_point_model(data: np.ndarray) -> pm.Model:
    """
    Build a Bayesian change point model using PyMC with separate means and stds before and after τ.
    
    Args:
        data (np.ndarray): 1D array of time series data (e.g., log returns).
    
    Returns:
        pm.Model: The PyMC model object.
    """
    n = len(data)
    idx = np.arange(n)

    with pm.Model() as model:
        # Discrete change point τ
        tau = pm.DiscreteUniform("tau", lower=5, upper=n - 5)

        # Priors for means
        mu_1 = pm.Normal("mu_1", mu=np.mean(data), sigma=2 * np.std(data))
        mu_2 = pm.Normal("mu_2", mu=np.mean(data), sigma=2 * np.std(data))

        # Priors for standard deviations
        sigma_1 = pm.HalfNormal("sigma_1", sigma=np.std(data))
        sigma_2 = pm.HalfNormal("sigma_2", sigma=np.std(data))

        # Switch mean and sigma based on τ
        mu = pm.Deterministic("mu", pm.math.switch(idx < tau, mu_1, mu_2))
        sigma = pm.Deterministic("sigma", pm.math.switch(idx < tau, sigma_1, sigma_2))

        # Likelihood
        pm.Normal("obs", mu=mu, sigma=sigma, observed=data)

    logger.info("PyMC change point model built.")
    return model


def sample_model(
    model: pm.Model,
    draws: int = 3000,
    tune: int = 1500,
    target_accept: float = 0.95
) -> az.InferenceData:
    """
    Run MCMC sampling for the given model.
    
    Args:
        model (pm.Model): PyMC model to sample.
        draws (int): Number of samples to draw.
        tune (int): Number of tuning steps.
        target_accept (float): Target acceptance rate.
    
    Returns:
        az.InferenceData: Posterior samples.
    """
    try:
        with model:
            trace = pm.sample(draws=1000, tune=500, cores=4, target_accept=0.9, return_inferencedata=True)

        logger.info("Sampling completed.")
        return trace
    except Exception as e:
        logger.error(f"Sampling failed: {e}")
        raise
