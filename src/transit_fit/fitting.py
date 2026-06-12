import numpy as np
from pytransit import RoadRunnerModel
from scipy.optimize import minimize
import logging

log = logging.getLogger(__name__)

class ExoplanetFitter:
    def __init__(self, model_type='quadratic'):
        self.model = RoadRunnerModel(model_type)

    def transit_model(self, params, times):
        """
        params: [k, t0, p, a, i]
        k: radius ratio (Rp/Rs)
        t0: transit center
        p: period
        a: semi-major axis / Rs
        i: inclination in radians
        """
        k, t0, p, a, i = params
        self.model.set_data(times)
        # Using default limb darkening coefficients [0.1, 0.1]
        flux = self.model.evaluate(k=k, ldc=[0.1, 0.1], t0=t0, p=p, a=a, i=i)
        return flux

    def objective(self, params, times, flux, flux_err):
        model_flux = self.transit_model(params, times)
        return np.sum(((flux - model_flux) / flux_err)**2)

    def fit(self, times, flux, initial_params):
        log.info("Fitting transit model using PyTransit...")
        
        flux_err = np.ones_like(flux) * 0.0001 # Assume small error if not provided
        
        # initial_params order: [k, t0, p, a, i]
        res = minimize(self.objective, initial_params, args=(times, flux, flux_err), 
                       method='Nelder-Mead', tol=1e-6)
        
        if res.success:
            return res.x
        else:
            log.warning("Fit failed.")
            return initial_params

    def fit_with_uncertainty(self, times, flux, initial_params, n_bootstraps=50):
        log.info(f"Running residual bootstrap with {n_bootstraps} iterations...")
        best_fit_params = self.fit(times, flux, initial_params)
        model_flux = self.transit_model(best_fit_params, times)
        residuals = flux - model_flux
        
        bootstrap_params = []
        for _ in range(n_bootstraps):
            # Resample residuals with replacement
            resampled_residuals = np.random.choice(residuals, size=len(residuals), replace=True)
            synthetic_flux = model_flux + resampled_residuals
            
            fit_p = self.fit(times, synthetic_flux, best_fit_params)
            bootstrap_params.append(fit_p)
            
        bootstrap_params = np.array(bootstrap_params)
        
        # Calculate 1-sigma bounds (16th and 84th percentiles)
        lower_bound = np.percentile(bootstrap_params, 16, axis=0)
        upper_bound = np.percentile(bootstrap_params, 84, axis=0)
        
        err_minus = best_fit_params - lower_bound
        err_plus = upper_bound - best_fit_params
        
        return {
            'best_fit': best_fit_params,
            'err_minus': err_minus,
            'err_plus': err_plus
        }
