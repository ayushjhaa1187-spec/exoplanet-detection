import lightkurve as lk
import numpy as np
import logging

log = logging.getLogger(__name__)

class ExoplanetDataFetcher:
    def __init__(self):
        pass

    def fetch_lightcurve(self, target_id, author='Kepler', quarter=None):
        """Fetch lightcurve for a given target."""
        log.info(f"Searching for lightcurve: {target_id}")
        search_result = lk.search_lightcurve(target_id, author=author, quarter=quarter)
        if len(search_result) == 0:
            raise ValueError(f"No lightcurve found for {target_id}")
        
        log.info(f"Downloading {len(search_result)} lightcurves...")
        lc_collection = search_result.download_all()
        return lc_collection

    def stitch_and_clean(self, lc_collection):
        """Stitch collection and perform basic cleaning."""
        lc = lc_collection.stitch()
        log.info("Cleaning lightcurve...")
        lc = lc.remove_nans().remove_outliers()
        # Flatten to remove long-term trends
        flattened_lc = lc.flatten(window_length=401)
        return flattened_lc

    def save_lightcurve(self, lc, path):
        """Save lightcurve to a FITS file."""
        log.info(f"Saving lightcurve to {path}")
        lc.to_fits(path, overwrite=True)

    def find_transit_parameters(self, lc, maximum_period=400):
        """Find transit parameters using Box Least Squares (BLS)."""
        log.info("Running BLS to find transit parameters...")
        
        # Limit the maximum period to half the observation baseline to ensure at least 2 transits can occur
        baseline = lc.time.value[-1] - lc.time.value[0]
        max_p = min(float(maximum_period), baseline / 2.0)
        
        # Scale the number of search points proportionally to search range, capped between 10k and 100k
        num_points = int(10000 * (max_p / 20.0))
        num_points = max(10000, min(num_points, 100000))
        
        periodogram = lc.to_periodogram(method='bls', period=np.linspace(0.5, max_p, num_points))
        
        best_fit = periodogram.period_at_max_power
        t0 = periodogram.transit_time_at_max_power
        duration = periodogram.duration_at_max_power
        
        return {
            'period': best_fit.value,
            't0': t0.value,
            'duration': duration.value,
            'periodogram': periodogram
        }
