import logging
from .data.data_loader import ExoplanetDataFetcher
from .features.preprocessing import ExoplanetPreprocessor
from .models.model import AstroNetModel
from .transit_fit.fitting import ExoplanetFitter
from .vetting.vetting import ExoplanetVetter

log = logging.getLogger(__name__)

class ExoAstroPipeline:
    def __init__(self):
        self.fetcher = ExoplanetDataFetcher()
        self.preprocessor = ExoplanetPreprocessor()
        self.model = AstroNetModel()
        self.fitter = ExoplanetFitter()
        self.vetter = ExoplanetVetter()

    def run(self, target_id, author='Kepler', **fetch_kwargs):
        log.info(f"Starting pipeline for target: {target_id}")
        
        # 1. Fetch Data
        try:
            lc_collection = self.fetcher.fetch_lightcurve(target_id, author=author, **fetch_kwargs)
        except Exception as e:
            log.error(f"Error fetching data: {e}")
            return None
        
        # 2. Clean Data
        lc_clean = self.fetcher.stitch_and_clean(lc_collection)
        
        # 3. Initial Search (BLS)
        search_results = self.fetcher.find_transit_parameters(lc_clean)
        period = search_results['period']
        t0 = search_results['t0']
        duration = search_results['duration']
        
        log.info(f"Initial parameters found: Period={period:.4f}, T0={t0:.4f}, Duration={duration:.4f}")
        
        # 4. Preprocessing for CNN
        global_view, local_view = self.preprocessor.process(lc_clean, period, t0, duration)
        
        # 5. AstroNet Classification
        score = self.model.predict(global_view, local_view)
        log.info(f"AstroNet classification score: {score[0][0]:.4f}")
        
        # 6. Scientific Refinement (Optional - using folded data for speed)
        folded = lc_clean.fold(period=period, epoch_time=t0)
        folded.sort('time')
        # Filter for local region to fit
        mask = (folded.time.value > -2*duration) & (folded.time.value < 2*duration)
        times_fit = folded.time.value[mask]
        flux_fit = folded.flux.value[mask]
        
        # Initial guess for fit: [k, t0_offset, p, a, i]
        # Note: t0 in folded is 0.
        initial_guess = [0.1, 0.0, period, 10.0, 1.57]
        fit_params = self.fitter.fit(times_fit, flux_fit, initial_guess)
        
        # 7. Vetting Tests
        snr = self.vetter.calculate_snr(lc_clean, period, t0, duration)
        odd_even = self.vetter.odd_even_test(lc_clean, period, t0, duration)
        secondary = self.vetter.secondary_eclipse_test(lc_clean, period, t0, duration)
        
        results = {
            'target_id': target_id,
            'astronet_score': float(score[0][0]),
            'snr': snr,
            'odd_even_suspicious': odd_even['is_suspicious'],
            'secondary_eclipse_depth': secondary,
            'bls_period': period,
            'bls_t0': t0,
            'bls_duration': duration,
            'fitted_k': fit_params[0]
        }
        
        log.info("Pipeline completed successfully.")
        return results
