import pymc as pm
import numpy as np
import logging

logger = logging.getLogger(__name__)

def build_change_point_model(data):
    """
    Build Bayesian change point model with separate means and variances before and after a change point.
    Args:
        data (np.array): 1D array of observations.
    Returns:
        pm.Model: PyMC model object.
    """
    n = len(data)
    idx = np.arange(n)

    with pm.Model() as model:
        # Discrete change point (tau)
        tau = pm.DiscreteUniform("tau", lower=5, upper=n - 5)

        # Separate means and stds before and after change
        mu_1 = pm.Normal("mu_1", mu=np.mean(data), sigma=np.std(data) * 2)
        mu_2 = pm.Normal("mu_2", mu=np.mean(data), sigma=np.std(data) * 2)

        sigma_1 = pm.HalfNormal("sigma_1", sigma=np.std(data))
        sigma_2 = pm.HalfNormal("sigma_2", sigma=np.std(data))

        # Piecewise parameters
        mu = pm.math.switch(tau >= idx, mu_1, mu_2)
        sigma = pm.math.switch(tau >= idx, sigma_1, sigma_2)

        # Likelihood
        obs = pm.Normal("obs", mu=mu, sigma=sigma, observed=data)

    logger.info("Enhanced Bayesian change point model built.")
    return model



def sample_model(model, draws=3000, tune=1500, target_accept=0.95):
    """
    Sample posterior using MCMC.
    Returns:
        arviz.InferenceData: Posterior samples and diagnostics.
    """
    try:
        with model:
            trace = pm.sample(draws=draws, tune=tune, target_accept=target_accept, return_inferencedata=True)
        logger.info("Sampling completed successfully.")
        return trace
    except Exception as e:
        logger.error(f"Sampling failed: {e}")
        raise
