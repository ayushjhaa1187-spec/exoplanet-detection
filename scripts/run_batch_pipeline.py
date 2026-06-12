import os
import sys
import json
import logging
import numpy as np
import lightkurve as lk

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pipeline import ExoAstroPipeline
from src.models.model import AdvancedAstroNetModel

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

def main():
    targets = [
        {"id": "kepler-22b", "name": "Kepler-22b", "type": "CP"},
        {"id": "kepler-10b", "name": "Kepler-10b", "type": "CP"},
        {"id": "kepler-452b", "name": "Kepler-452b", "type": "CP"},
        {"id": "kepler-1b", "name": "Kepler-1b", "type": "CP"},
        {"id": "kepler-62f", "name": "Kepler-62f", "type": "CP"},
        {"id": "kic-3642335", "name": "KIC 3642335", "type": "CP"},
        {"id": "kic-757450", "name": "KIC 757450", "type": "FP"},
        {"id": "kepler-7b", "name": "Kepler-7b", "type": "CP"},
        {"id": "kepler-11b", "name": "Kepler-11b", "type": "CP"},
        {"id": "kepler-16b", "name": "Kepler-16b", "type": "CP"}
    ]
    
    pipeline = ExoAstroPipeline()
    # Load advanced trained model
    pipeline.model = AdvancedAstroNetModel()
    pipeline.model.load("models/astronet_best.h5")
    
    os.makedirs("web/public/plots", exist_ok=True)
    os.makedirs("web/public/data", exist_ok=True)
    
    candidates = []
    
    for t in targets:
        target_name = t["name"]
        target_id = t["id"]
        category = t["type"]
        
        log.info(f"==========================================")
        log.info(f"Processing target: {target_name}...")
        
        # Try loading local FITS first to avoid network requests
        filename = target_name.replace(" ", "_") + ".fits"
        local_path = os.path.join("data/raw", category, filename)
        
        lc_clean = None
        if os.path.exists(local_path):
            log.info(f"Loading local FITS from {local_path}...")
            try:
                lc = lk.read(local_path)
                # Stitch and clean or clean directly if single LightCurve
                if isinstance(lc, lk.LightCurveCollection):
                    lc_clean = pipeline.fetcher.stitch_and_clean(lc)
                else:
                    lc = lc.remove_nans().remove_outliers()
                    lc_clean = lc.flatten(window_length=401)
            except Exception as e:
                log.error(f"Error loading local FITS: {e}")
        
        if lc_clean is None:
            log.info(f"Local FITS not found or failed. Fetching over network for {target_name}...")
            try:
                lc_collection = pipeline.fetcher.fetch_lightcurve(target_name, quarter=2)
                lc_clean = pipeline.fetcher.stitch_and_clean(lc_collection)
            except Exception as e:
                log.error(f"Error fetching/processing over network: {e}")
                continue
                
        # Run BLS
        search_results = pipeline.fetcher.find_transit_parameters(lc_clean)
        period = search_results['period']
        t0 = search_results['t0']
        duration = search_results['duration']
        
        # Preprocessing for CNN
        global_view, local_view = pipeline.preprocessor.process(lc_clean, period, t0, duration)
        
        # AstroNet classification
        score = float(pipeline.model.predict(global_view, local_view)[0][0])
        log.info(f"Prediction score: {score:.4f}")
        
        # Transit fitting
        folded = lc_clean.fold(period=period, epoch_time=t0)
        folded.sort('time')
        mask = (folded.time.value > -2*duration) & (folded.time.value < 2*duration)
        times_fit = folded.time.value[mask]
        flux_fit = folded.flux.value[mask]
        
        # Safely fit parameters
        fitted_k = 0.1
        if len(times_fit) > 5:
            try:
                initial_guess = [0.1, 0.0, period, 10.0, 1.57]
                fit_params = pipeline.fitter.fit(times_fit, flux_fit, initial_guess)
                fitted_k = float(fit_params[0])
            except Exception as e:
                log.warning(f"PyTransit fitting failed for {target_name}: {e}. Using default k=0.1")
        
        # Vetting
        snr = float(pipeline.vetter.calculate_snr(lc_clean, period, t0, duration))
        odd_even = pipeline.vetter.odd_even_test(lc_clean, period, t0, duration)
        secondary = float(pipeline.vetter.secondary_eclipse_test(lc_clean, period, t0, duration))
        
        # Save plots
        folded_plot_rel = f"/plots/{target_id}_folded.png"
        folded_plot_abs = os.path.join("web/public", "plots", f"{target_id}_folded.png")
        pipeline.vetter.plot_folded_transit(lc_clean, period, t0, duration, folded_plot_abs)
        
        # Generate diagnostic plot (zoomed in view)
        diagnostic_plot_rel = f"/plots/{target_id}_diagnostic.png"
        diagnostic_plot_abs = os.path.join("web/public", "plots", f"{target_id}_diagnostic.png")
        pipeline.vetter.plot_folded_transit(lc_clean, period, t0, duration / 2, diagnostic_plot_abs)
        
        # Labeling: threshold at 0.5
        label = "PLANET CANDIDATE" if score >= 0.5 else "FALSE POSITIVE"
        
        # Create summary
        short_summary = f"Transit signal at {period:.2f}d. Trained advanced CNN score: {score:.4f}. SNR {snr:.1f}. PyTransit Rp/Rs = {fitted_k:.4f}."
        
        candidate_data = {
            "id": target_id,
            "targetName": target_name,
            "astronet_score": round(score, 4),
            "label": label,
            "bls_period": round(period, 4),
            "bls_t0": round(t0, 4),
            "bls_duration": round(duration, 4),
            "snr": round(snr, 2),
            "fitted_k": round(fitted_k, 4),
            "odd_even_suspicious": bool(odd_even['is_suspicious']),
            "secondary_eclipse_depth": round(secondary, 4),
            "status": "trained_advanced",
            "shortSummary": short_summary,
            "foldedPlot": folded_plot_rel,
            "diagnosticPlot": diagnostic_plot_rel
        }
        
        candidates.append(candidate_data)
        log.info(f"Finished {target_name} successfully!")

    # Write to web/public/data/candidates.json
    with open("web/public/data/candidates.json", "w") as f:
        json.dump(candidates, f, indent=2)
    log.info("Successfully wrote web/public/data/candidates.json!")

if __name__ == "__main__":
    main()
