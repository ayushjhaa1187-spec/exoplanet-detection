import os
import sys
import logging
import argparse

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data.data_loader import ExoplanetDataFetcher

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Fetch exoplanet lightcurves.")
    parser.add_argument("--targets", nargs="+", default=["Kepler-10b", "Kepler-90i"], help="List of target IDs")
    parser.add_argument("--outdir", default="data/raw", help="Directory to save FITS files")
    parser.add_argument("--quarter", type=int, help="Specific quarter to fetch")
    args = parser.parse_args()

    fetcher = ExoplanetDataFetcher()
    
    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    for target in args.targets:
        try:
            log.info(f"Processing {target}...")
            lc_collection = fetcher.fetch_lightcurve(target, quarter=args.quarter)
            lc = lc_collection.stitch()
            
            # Sanitize filename
            filename = target.replace(" ", "_") + ".fits"
            path = os.path.join(args.outdir, filename)
            
            fetcher.save_lightcurve(lc, path)
            log.info(f"Successfully saved {target} to {path}")
        except Exception as e:
            log.error(f"Failed to fetch {target}: {e}")

if __name__ == "__main__":
    main()
