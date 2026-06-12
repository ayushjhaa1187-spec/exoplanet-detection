import os
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

def main():
    outdir = "data/labels"
    os.makedirs(outdir, exist_ok=True)
    
    # In a real scenario, this merges TOI catalogs from ExoFOP
    # For now, we take our sample_10stars.csv and format it as master
    sample_path = "data/raw/sample_10stars.csv"
    
    if os.path.exists(sample_path):
        df = pd.read_csv(sample_path)
        # Assuming label mapping: 0: Transit, 1: EB, 2: Blend, 3: Noise
        class_map = {0: 'planet_transit', 1: 'eclipsing_binary', 2: 'blend_or_contamination', 3: 'noise_no_signal'}
        df['Label_Name'] = df['Label'].map(class_map)
        
        out_csv = os.path.join(outdir, "master_labels.csv")
        df.to_csv(out_csv, index=False)
        log.info(f"Built master label catalog at {out_csv} with {len(df)} records.")
    else:
        log.error(f"Sample data not found at {sample_path}")

if __name__ == "__main__":
    main()
