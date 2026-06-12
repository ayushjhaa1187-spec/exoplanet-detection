import os
import sys
import logging
import argparse
import multiprocessing as mp
import pandas as pd
import json
import numpy as np

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pipeline import ExoAstroPipeline

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(processName)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

def process_target(target_id):
    """Worker function to process a single target."""
    try:
        pipeline = ExoAstroPipeline()
        # Ensure we fetch TESS data. We can specify author='SPOC' and exptime=120 for 2-min cadence TESS data
        results = pipeline.run(target_id, author='SPOC', exptime=120)
        
        if results is None:
            return {"target_id": target_id, "error": "No data or processing failed"}
        return results
    except Exception as e:
        log.error(f"Error processing {target_id}: {e}")
        return {"target_id": target_id, "error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="Run TESS batch processing.")
    parser.add_argument("--targets_file", type=str, help="CSV file containing 'TIC_ID' column of targets to process.")
    parser.add_argument("--targets", type=str, nargs="+", help="List of TIC IDs to process.")
    parser.add_argument("--outdir", default="outputs/batch_results", help="Directory to save batch results")
    parser.add_argument("--workers", type=int, default=mp.cpu_count() - 1, help="Number of parallel workers")
    args = parser.parse_args()

    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    target_list = []
    if args.targets_file:
        df = pd.read_csv(args.targets_file)
        if 'TIC_ID' in df.columns:
            target_list = df['TIC_ID'].astype(str).tolist()
            # Ensure TIC prefix if not present
            target_list = [t if t.startswith("TIC ") else f"TIC {t}" for t in target_list]
        else:
            log.error("targets_file must contain a 'TIC_ID' column")
            return
    elif args.targets:
        target_list = [t if t.startswith("TIC ") else f"TIC {t}" for t in args.targets]
    else:
        log.warning("No targets provided. Running a sample list.")
        target_list = ["TIC 270810595", "TIC 25155310"] # Example TICs
        
    log.info(f"Loaded {len(target_list)} targets. Starting pool with {args.workers} workers...")

    all_results = []
    with mp.Pool(processes=args.workers) as pool:
        for i, result in enumerate(pool.imap_unordered(process_target, target_list)):
            log.info(f"Completed {i+1}/{len(target_list)}")
            all_results.append(result)
            
            # Save individual JSON
            target_id_safe = str(result['target_id']).replace(' ', '_')
            with open(os.path.join(args.outdir, f"{target_id_safe}.json"), 'w') as f:
                # Convert any numpy types to python types for json serialization
                clean_result = {}
                for k, v in result.items():
                    if isinstance(v, (np.float32, np.float64)):
                        clean_result[k] = float(v)
                    elif isinstance(v, (np.int32, np.int64)):
                        clean_result[k] = int(v)
                    else:
                        clean_result[k] = v
                json.dump(clean_result, f, indent=4)

    # Save summary CSV
    df_results = pd.DataFrame(all_results)
    df_results.to_csv(os.path.join(args.outdir, "batch_summary.csv"), index=False)
    log.info(f"Batch processing complete. Summary saved to {os.path.join(args.outdir, 'batch_summary.csv')}")

if __name__ == "__main__":
    main()
