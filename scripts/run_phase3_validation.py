import os
import yaml
import json
import logging
import pandas as pd
import numpy as np

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data.data_loader import ExoplanetDataFetcher
from src.features.preprocessing import ExoplanetPreprocessor
from src.features.tabular_features import TabularFeatureExtractor
from src.models.multiclass_model import HybridMulticlassModel
from src.vetting.vetting import ExoplanetVetter
from src.vetting.decision_engine import DecisionEngine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

def main():
    config_path = "configs/sector.yaml"
    if not os.path.exists(config_path):
        log.error("configs/sector.yaml not found.")
        return
        
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
        
    sector = config.get('sector', 27)
    author = config.get('author', 'SPOC')
    outdir = config.get('output_dir', f"outputs/sector_{sector}")
    os.makedirs(outdir, exist_ok=True)
    
    catalog_path = f"data/catalog/sector_{sector}_targets.csv"
    if not os.path.exists(catalog_path):
        log.error(f"Catalog {catalog_path} not found. Please run scripts/download_tess_sector.py first.")
        return
        
    df_catalog = pd.read_csv(catalog_path)
    targets = df_catalog['TIC_ID'].tolist()
    
    fetcher = ExoplanetDataFetcher()
    preprocessor = ExoplanetPreprocessor()
    tab_extractor = TabularFeatureExtractor()
    model = HybridMulticlassModel()
    vetter = ExoplanetVetter()
    decision_engine = DecisionEngine()
    
    results = []
    
    for tic in targets:
        log.info(f"Processing {tic}...")
        try:
            lc_collection = fetcher.fetch_lightcurve(tic, author=author, mission="TESS", sector=sector)
            lc_clean = fetcher.stitch_and_clean(lc_collection)
            
            bls_results = fetcher.find_transit_parameters(lc_clean)
            period = bls_results['period']
            t0 = bls_results['t0']
            duration = bls_results['duration']
            
            # Extract features
            global_view, local_view = preprocessor.process(lc_clean, period, t0, duration)
            
            snr = vetter.calculate_snr(lc_clean, period, t0, duration)
            odd_even = vetter.odd_even_test(lc_clean, period, t0, duration)
            sec_depth = vetter.secondary_eclipse_test(lc_clean, period, t0, duration)
            
            tabular_feat = tab_extractor.extract(lc_clean, bls_results, snr, odd_even, sec_depth)
            
            # Predict
            global_batch = np.expand_dims(global_view, axis=0)
            local_batch = np.expand_dims(local_view, axis=0)
            tab_batch = np.expand_dims(tabular_feat, axis=0)
            
            probs = model.model.predict([global_batch, local_batch, tab_batch], verbose=0)[0]
            
            # Decide
            decision = decision_engine.evaluate(probs, snr, odd_even, sec_depth)
            
            record = {
                "TIC_ID": tic,
                "Period": period,
                "Depth": tabular_feat[2],
                "Duration": duration,
                "SNR": snr,
                "Base_Class": decision_engine.CLASSES[np.argmax(probs)],
                "Final_Class": decision['final_class'],
                "Confidence": decision['confidence'],
                "Explanation": decision['explanation']
            }
            results.append(record)
            
        except Exception as e:
            log.error(f"Failed on {tic}: {e}")
            results.append({"TIC_ID": tic, "Final_Class": "processing_error", "Explanation": str(e)})
            
    df_results = pd.DataFrame(results)
    
    # Generate candidate rankings
    df_candidates = df_results[df_results['Final_Class'] != 'processing_error'].copy()
    if not df_candidates.empty:
        # Rank by confidence * SNR
        df_candidates['Ranking_Score'] = df_candidates['Confidence'].fillna(0) * df_candidates['SNR'].fillna(0)
        df_candidates = df_candidates.sort_values('Ranking_Score', ascending=False)
        
    out_csv = os.path.join(outdir, "candidate_rankings.csv")
    df_candidates.to_csv(out_csv, index=False)
    log.info(f"Saved rankings to {out_csv}")

if __name__ == "__main__":
    main()
