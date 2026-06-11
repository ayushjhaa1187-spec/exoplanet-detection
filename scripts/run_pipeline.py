import os
import sys
import logging

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pipeline import ExoAstroPipeline

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

def main():
    target_id = 'Kepler-22b'
    
    pipeline = ExoAstroPipeline()
    
    # Try to load trained weights if available
    weights_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'astronet_weights.h5')
    if os.path.exists(weights_path):
        log.info(f"Loading weights from {weights_path}")
        pipeline.model.load(weights_path)
    else:
        log.info("No saved weights found. Running with default (untrained) model.")
        
    results = pipeline.run(target_id, quarter=2)
    
    if results:
        print("\n--- Pipeline Results ---")
        for key, value in results.items():
            print(f"{key}: {value}")
    else:
        print("Pipeline failed to produce results.")

if __name__ == "__main__":
    main()
