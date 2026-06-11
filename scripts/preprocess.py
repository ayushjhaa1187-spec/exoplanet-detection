import os
import sys
import logging
import argparse
import lightkurve as lk
import numpy as np

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data.data_loader import ExoplanetDataFetcher
from src.features.preprocessing import ExoplanetPreprocessor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Preprocess exoplanet lightcurves.")
    parser.add_argument("--indir", default="data/raw", help="Directory containing FITS files")
    parser.add_argument("--outdir", default="data/processed", help="Directory to save numpy views")
    args = parser.parse_args()

    fetcher = ExoplanetDataFetcher()
    preprocessor = ExoplanetPreprocessor()
    
    if not os.path.exists(args.indir):
        log.error(f"Input directory {args.indir} does not exist.")
        return

    fits_files = [f for f in os.listdir(args.indir) if f.endswith(".fits")]
    
    for filename in fits_files:
        try:
            target_id = filename.replace(".fits", "").replace("_", " ")
            log.info(f"Processing {target_id}...")
            
            path = os.path.join(args.indir, filename)
            lc = lk.read(path)
            
            # Find parameters using BLS (usually you'd have these from a table)
            params = fetcher.find_transit_parameters(lc)
            
            global_view, local_view = preprocessor.process(
                lc, params['period'], params['t0'], params['duration']
            )
            
            preprocessor.save_views(target_id, global_view, local_view, args.outdir)
            
        except Exception as e:
            log.error(f"Failed to process {filename}: {e}")

if __name__ == "__main__":
    main()
