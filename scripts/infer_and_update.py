import os
import sys
import json
import logging
import argparse
import numpy as np

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.model import AstroNetModel, AdvancedAstroNetModel

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Run inference and update web dashboard candidates.")
    parser.add_argument("--data_dir", default="data/processed", help="Directory containing processed numpy views")
    parser.add_argument("--model_path", default="models/astronet_best.h5", help="Path to the trained model (.h5 or .keras)")
    parser.add_argument("--model_type", choices=['baseline', 'advanced'], default='advanced', help="Model architecture type")
    parser.add_argument("--candidates_json", default="web/public/data/candidates.json", help="Path to candidates.json")
    args = parser.parse_args()

    if not os.path.exists(args.model_path):
        log.error(f"Model not found at {args.model_path}. Please make sure training completed successfully and you downloaded the model.")
        return

    if not os.path.exists(args.candidates_json):
        log.error(f"Candidates JSON not found at {args.candidates_json}")
        return

    log.info(f"Loading {args.model_type} model from {args.model_path}...")
    if args.model_type == 'advanced':
        astronet = AdvancedAstroNetModel()
    else:
        astronet = AstroNetModel()
        
    astronet.load(args.model_path)

    log.info(f"Loading candidates from {args.candidates_json}...")
    with open(args.candidates_json, 'r') as f:
        candidates = json.load(f)

    updated_count = 0

    for candidate in candidates:
        target_name = candidate['targetName']
        # Try both Kepler_10b and Kepler-10b folder styles
        dir_names = [target_name.replace(" ", "_"), target_name.replace(" ", "-")]
        
        g_view, l_view = None, None
        
        # Check in data_dir (either root or CP/FP subfolders)
        search_paths = [
            args.data_dir,
            os.path.join(args.data_dir, 'CP'),
            os.path.join(args.data_dir, 'FP')
        ]
        
        for base_path in search_paths:
            if not os.path.exists(base_path):
                continue
            for dir_name in dir_names:
                candidate_dir = os.path.join(base_path, dir_name)
                g_path = os.path.join(candidate_dir, "global_view.npy")
                l_path = os.path.join(candidate_dir, "local_view.npy")
                if os.path.exists(g_path) and os.path.exists(l_path):
                    g_view = np.load(g_path)
                    l_view = np.load(l_path)
                    break
            if g_view is not None:
                break
                
        if g_view is not None and l_view is not None:
            log.info(f"Running prediction for {target_name}...")
            score = float(astronet.predict(g_view, l_view)[0][0])
            
            # Update candidate data
            candidate['astronet_score'] = round(score, 4)
            candidate['status'] = f"trained_{args.model_type}"
            
            # Update label and summary based on prediction
            if score >= 0.50:
                candidate['label'] = "PLANET CANDIDATE"
            else:
                candidate['label'] = "FALSE POSITIVE"
                
            # Update summary
            summary = candidate.get('shortSummary', '')
            # Replace the untrained text with trained text
            if "Untrained CNN score" in summary or "baseline" in summary or "Awaiting" in summary:
                candidate['shortSummary'] = f"Transit signal at {candidate['bls_period']:.2f}d. Trained {args.model_type} CNN score: {score:.4f}. SNR {candidate['snr']:.1f}. PyTransit Rp/Rs = {candidate['fitted_k']:.4f}."
            
            log.info(f"Updated {target_name}: Score = {score:.4f}, Label = {candidate['label']}")
            updated_count += 1
        else:
            log.warning(f"Could not find processed numpy views for {target_name} in {args.data_dir}")

    # Save candidates back
    if updated_count > 0:
        with open(args.candidates_json, 'w') as f:
            json.dump(candidates, f, indent=2)
        log.info(f"Successfully updated {updated_count} candidates in {args.candidates_json}!")
    else:
        log.warning("No candidates were updated because no matching processed views were found.")

if __name__ == "__main__":
    main()
