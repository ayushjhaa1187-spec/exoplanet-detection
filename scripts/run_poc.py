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
    target_id = 'Kepler-10b'
    
    pipeline = ExoAstroPipeline()
    results = pipeline.run(target_id, quarter=2)
    
    if results:
        print("\n--- Pipeline Results ---")
        for key, value in results.items():
            print(f"{key}: {value}")
    else:
        print("Pipeline failed to produce results.")

if __name__ == "__main__":
    main()
