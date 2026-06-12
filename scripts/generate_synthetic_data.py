import os
import numpy as np
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

CLASSES = [
    "planet_transit",
    "eclipsing_binary",
    "blend_or_contamination",
    "stellar_variability",
    "noise_no_signal"
]

def synthesize_target(class_idx):
    """Generate synthetic global, local, and tabular views for a given class."""
    # Global: 2001, Local: 201, Tabular: 8
    g = np.random.normal(0, 0.1, 2001)
    l = np.random.normal(0, 0.1, 201)
    
    # [period, duration, depth, snr, odd_depth, even_depth, odd_even_sig, sec_depth]
    t = np.array([3.14, 0.1, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0])
    
    if class_idx == 0: # Planet
        g[990:1010] -= 0.5
        l[90:110] -= 0.5
        t = np.array([3.14, 0.1, 0.005, 15.0, 0.005, 0.005, 0.1, 0.0001])
    elif class_idx == 1: # EB
        g[990:1010] -= 5.0
        g[490:510] -= 1.0 # Secondary
        l[90:110] -= 5.0
        t = np.array([3.14, 0.2, 0.05, 50.0, 0.05, 0.02, 10.0, 0.01])
    elif class_idx == 2: # Blend
        # V-shape
        for i in range(20):
            g[990+i] -= (20-i)*0.01
            l[90+i] -= (20-i)*0.01
        t = np.array([3.14, 0.15, 0.01, 12.0, 0.01, 0.01, 1.0, 0.002])
    elif class_idx == 3: # Variability
        g = np.sin(np.linspace(0, 20, 2001)) * 0.5 + np.random.normal(0, 0.1, 2001)
        l = np.sin(np.linspace(0, 2, 201)) * 0.5 + np.random.normal(0, 0.1, 201)
        t = np.array([1.5, 0.5, 0.01, 8.0, 0.01, 0.01, 0.5, 0.01])
    else: # Noise
        t = np.array([0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0])
        
    return g, l, t

def main():
    num_samples = 500
    outdir = "data/features/views"
    os.makedirs(outdir, exist_ok=True)
    
    records = []
    
    log.info(f"Generating {num_samples} synthetic targets...")
    tabular_data = []
    
    for i in range(num_samples):
        tic = f"TIC_SYNTH_{i}"
        class_idx = np.random.randint(0, 5)
        label_name = CLASSES[class_idx]
        
        g, l, t = synthesize_target(class_idx)
        
        target_dir = os.path.join(outdir, tic)
        os.makedirs(target_dir, exist_ok=True)
        
        np.save(os.path.join(target_dir, "global.npy"), g)
        np.save(os.path.join(target_dir, "local.npy"), l)
        
        tabular_data.append(t)
        
        records.append({
            "TIC_ID": tic,
            "Label_Name": label_name,
            "Label_Idx": class_idx
        })
        
    # Save labels
    df_labels = pd.DataFrame(records)
    df_labels.to_csv("data/labels/synthetic_master_labels.csv", index=False)
    
    # Save tabular array
    np.save("data/features/tabular_features.npy", np.array(tabular_data))
    
    log.info("Synthetic generation complete.")
    
if __name__ == "__main__":
    main()
