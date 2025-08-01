import numpy as np
import pymc as pm
import pytensor.tensor as pt
from aesara.tensor import alloc
import arviz as az
import pytensor.tensor as pt
import pymc as pm
import numpy as np
import aesara.tensor as at
import numpy as np
import pymc as pm
import aesara.tensor as at
from aesara.tensor import alloc
import arviz as az

def bayesian_mean_shift_flexible(data, max_cp=10, min_dist=5):
    """
    Bayesian model to detect up to max_cp mean change points,
    with minimum distance between change points to avoid clustering.
    """
    n = len(data)
    x = np.arange(n)

    with pm.Model() as model:
        delta_tau = pm.Exponential("delta_tau", lam=1.0, shape=max_cp)
        tau_unscaled = pm.Deterministic("tau_unscaled", pt.cumsum(delta_tau))

        scale_factor = (n - max_cp * min_dist) / tau_unscaled[-1]
        min_dist_tensor = pt.constant(min_dist)
        tau_pos = pm.Deterministic(
            "tau_pos",
            pt.clip(
                pt.round(tau_unscaled * scale_factor + pt.arange(max_cp) * min_dist_tensor),
                min_dist,
                n - min_dist,
            ),
        )

        mu = pm.Normal("mu", mu=0, sigma=10, shape=max_cp + 1)
        sigma = pm.HalfNormal("sigma", sigma=5)

        mu_obs = pt.alloc(mu[0], n)
        for i in range(max_cp):
            mu_obs = pt.switch(x > tau_pos[i], mu[i + 1], mu_obs)

        y_obs = pm.Normal("y_obs", mu=mu_obs, sigma=sigma, observed=data)

        trace = pm.sample(1000, tune=1000, target_accept=0.95, chains=4, return_inferencedata=True)

    return trace, model

def bayesian_trend_change_model(data):
    """
    Detect a single trend (slope) change point using Bayesian piecewise linear regression.

    Args:
        data (array-like): 1D time series data.

    Returns:
        trace: Posterior samples.
        model: The PyMC model.
    """
    x = np.arange(len(data))
    y = np.array(data)

    with pm.Model() as model:
        cp = pm.DiscreteUniform("cp", lower=10, upper=len(data) - 10)

        a1 = pm.Normal("a1", mu=0, sigma=1)
        b1 = pm.Normal("b1", mu=0, sigma=1)
        a2 = pm.Normal("a2", mu=0, sigma=1)
        b2 = pm.Normal("b2", mu=0, sigma=1)

        mu = pm.math.switch(x < cp, a1 * x + b1, a2 * x + b2)

        sigma = pm.HalfNormal("sigma", sigma=1)
        y_obs = pm.Normal("y_obs", mu=mu, sigma=sigma, observed=y)

        trace = pm.sample(1000, tune=1000, chains=2, target_accept=0.95)

    return trace, model


def bayesian_variance_shift_model(data):
    """
    Detect a single variance change point using a Bayesian model.

    Args:
        data (array-like): 1D time series data.

    Returns:
        trace: Posterior samples.
        model: The PyMC model.
    """
    x = np.arange(len(data))
    y = np.array(data)

    with pm.Model() as model:
        cp = pm.DiscreteUniform("cp", lower=10, upper=len(data) - 10)

        mu = pm.Normal("mu", mu=0, sigma=10)
        sigma1 = pm.HalfNormal("sigma1", sigma=5)
        sigma2 = pm.HalfNormal("sigma2", sigma=5)

        sigma = pm.math.switch(x < cp, sigma1, sigma2)

        y_obs = pm.Normal("y_obs", mu=mu, sigma=sigma, observed=y)

        trace = pm.sample(1000, tune=1000, chains=2, target_accept=0.95)

    return trace, model

