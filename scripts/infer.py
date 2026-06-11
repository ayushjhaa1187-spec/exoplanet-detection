import os
import sys
import logging
import argparse
import numpy as np

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.model import AstroNetModel

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Inference using AstroNet.")
    parser.add_argument("--data_dir", default="data/processed", help="Directory containing processed numpy views")
    parser.add_argument("--model_path", default="models/astronet_baseline.h5", help="Path to the trained model")
    args = parser.parse_args()

    if not os.path.exists(args.model_path):
        log.error(f"Model not found at {args.model_path}")
        return

    log.info("Loading model...")
    astronet = AstroNetModel()
    astronet.load(args.model_path)

    for target_dir in os.listdir(args.data_dir):
        path = os.path.join(args.data_dir, target_dir)
        if os.path.isdir(path):
            try:
                g_view = np.load(os.path.join(path, "global_view.npy"))
                l_view = np.load(os.path.join(path, "local_view.npy"))
                
                score = astronet.predict(g_view, l_view)
                print(f"Target: {target_dir} | Score: {score[0][0]:.4f}")
            except Exception as e:
                log.error(f"Failed to predict for {target_dir}: {e}")

if __name__ == "__main__":
    main()
