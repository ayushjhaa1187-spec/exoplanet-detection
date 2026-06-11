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
    parser = argparse.ArgumentParser(description="Evaluate AstroNet model.")
    parser.add_argument("--data_dir", default="data/processed", help="Directory containing processed numpy views")
    parser.add_argument("--model_path", default="models/astronet_baseline.h5", help="Path to the trained model")
    args = parser.parse_args()

    if not os.path.exists(args.model_path):
        log.error(f"Model not found at {args.model_path}")
        return

    log.info("Loading model for evaluation...")
    astronet = AstroNetModel()
    astronet.load(args.model_path)
    
    # Simple evaluation loop
    # In a real scenario, this would compute Precision/Recall/F1 on a test set
    log.info("Evaluation complete (Placeholder for full metrics).")

if __name__ == "__main__":
    main()
