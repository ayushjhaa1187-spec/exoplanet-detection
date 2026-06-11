import os
import sys
import logging
import argparse
import numpy as np
import lightkurve as lk

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data.data_loader import ExoplanetDataFetcher
from src.transit_fit.fitting import ExoplanetFitter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Fit transit model using PyTransit.")
    parser.add_argument("--target", default="Kepler-10b", help="Target ID")
    parser.add_argument("--fits_path", help="Path to raw FITS file")
    args = parser.parse_args()

    fetcher = ExoplanetDataFetcher()
    fitter = ExoplanetFitter()

    if args.fits_path:
        lc = lk.read(args.fits_path)
    else:
        # Default to fetching if path not provided
        lc_collection = fetcher.fetch_lightcurve(args.target, quarter=2)
        lc = fetcher.stitch_and_clean(lc_collection)

    params = fetcher.find_transit_parameters(lc)
    
    # Initial guess for fit: [k, t0_offset, p, a, i]
    initial_guess = [0.1, 0.0, params['period'], 10.0, 1.57]
    
    # Fold to get local region for faster fitting
    folded = lc.fold(period=params['period'], epoch_time=params['t0']).sort('time')
    mask = (folded.time.value > -2*params['duration']) & (folded.time.value < 2*params['duration'])
    
    fit_params = fitter.fit(folded.time.value[mask], folded.flux.value[mask], initial_guess)
    print(f"Fitted Parameters [k, t0_offset, p, a, i]: {fit_params}")

if __name__ == "__main__":
    main()
