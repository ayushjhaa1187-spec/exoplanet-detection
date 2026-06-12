import os
import sys
import logging
import argparse
import numpy as np
import tensorflow as tf
from tensorflow.keras import callbacks

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.model import AstroNetModel, AdvancedAstroNetModel

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

def load_dataset(data_dir, target_samples=1000):
    """Load global and local views, and augment/synthesize data to balance and expand the dataset."""
    real_cp_global = []
    real_cp_local = []
    real_fp_global = []
    real_fp_local = []
    
    # Assume directory structure data/processed/[CP|FP]/target_id/
    for category in ['CP', 'FP']:
        cat_dir = os.path.join(data_dir, category)
        if not os.path.exists(cat_dir):
            continue
            
        for target_dir in os.listdir(cat_dir):
            path = os.path.join(cat_dir, target_dir)
            if os.path.isdir(path):
                try:
                    g_view = np.load(os.path.join(path, "global_view.npy"))
                    l_view = np.load(os.path.join(path, "local_view.npy"))
                    
                    # Clean NaNs immediately
                    g_view = np.nan_to_num(g_view, nan=0.0)
                    l_view = np.nan_to_num(l_view, nan=0.0)
                    
                    # Center and handle unnormalized views
                    med_g = np.median(g_view)
                    if med_g > 0.5:
                        g_view = g_view.copy()
                        g_view[g_view == 0.0] = med_g
                        g_view = g_view - med_g
                    else:
                        g_view = g_view - med_g
                        
                    med_l = np.median(l_view)
                    if med_l > 0.5:
                        l_view = l_view.copy()
                        l_view[l_view == 0.0] = med_l
                        l_view = l_view - med_l
                    else:
                        l_view = l_view - med_l

                    # Scale to standard deviation 1.0
                    std_g = np.std(g_view)
                    if std_g > 0.0:
                        g_view = g_view / std_g
                    std_l = np.std(l_view)
                    if std_l > 0.0:
                        l_view = l_view / std_l
                    
                    # Treat KIC_3642335 as FP (label 0) instead of CP
                    if category == 'CP' and target_dir != 'KIC_3642335':
                        real_cp_global.append(g_view)
                        real_cp_local.append(l_view)
                    else:
                        real_fp_global.append(g_view)
                        real_fp_local.append(l_view)
                except Exception as e:
                    log.warning(f"Failed to load data for {target_dir}: {e}")
                    
    num_cp = len(real_cp_global)
    num_fp = len(real_fp_global)
    
    if num_cp == 0 or num_fp == 0:
        log.error(f"Cannot load dataset. Found CP: {num_cp}, FP: {num_fp}")
        return np.array([]), np.array([]), np.array([])
        
    log.info(f"Loaded {num_cp} real CP and {num_fp} real FP samples. Synthesizing up to {target_samples} samples...")
    
    global_views = []
    local_views = []
    labels = []
    
    half_samples = target_samples // 2
    
    # 1. Generate CP Samples
    for i in range(half_samples):
        # Pick a random real CP target
        idx = np.random.randint(num_cp)
        g = real_cp_global[idx].copy()
        l = real_cp_local[idx].copy()
        
        # Apply random cyclic shifts (mimics T0 uncertainty)
        shift = np.random.randint(-10, 11)
        g_aug = np.roll(g, shift)
        # Shift local view proportionally
        l_shift = int(shift * (len(l) / len(g)))
        l_aug = np.roll(l, l_shift)
        
        # Apply random depth scaling (mimics varying planet sizes)
        scale = np.random.uniform(0.5, 1.5)
        g_aug = g_aug * scale
        l_aug = l_aug * scale
        
        # Add random Gaussian noise proportional to target std
        std_g = np.std(g) if np.std(g) > 0 else 1e-5
        std_l = np.std(l) if np.std(l) > 0 else 1e-5
        
        noise_std_g = std_g * np.random.uniform(0.01, 0.05)
        noise_std_l = std_l * np.random.uniform(0.01, 0.05)
        
        g_aug += np.random.normal(0, noise_std_g, g_aug.shape)
        l_aug += np.random.normal(0, noise_std_l, l_aug.shape)
        
        # Add a small random baseline offset proportional to std
        offset_g = np.random.uniform(-0.05, 0.05) * std_g
        offset_l = np.random.uniform(-0.05, 0.05) * std_l
        g_aug += offset_g
        l_aug += offset_l

        # Normalize final augmented views to unit standard deviation
        std_aug_g = np.std(g_aug)
        if std_aug_g > 0.0:
            g_aug = g_aug / std_aug_g
        std_aug_l = np.std(l_aug)
        if std_aug_l > 0.0:
            l_aug = l_aug / std_aug_l
        
        global_views.append(g_aug)
        local_views.append(l_aug)
        labels.append(1)
        
    # 2. Generate FP Samples
    for i in range(half_samples):
        # Synthesize FP in one of four ways:
        # A: Augment existing real FP
        # B: Deform a CP to have NO transit (flat noise)
        # C: Deform a CP to have an OFF-CENTER transit (mimicking incorrect period/T0)
        # D: Deform a CP to have a secondary eclipse (eclipsing binary)
        fp_type = np.random.choice(['real_fp', 'no_transit', 'off_center', 'secondary_eclipse'])
        
        if fp_type == 'real_fp':
            idx = np.random.randint(num_fp)
            g = real_fp_global[idx].copy()
            l = real_fp_local[idx].copy()
            
            # Apply shift
            shift = np.random.randint(-10, 11)
            g_aug = np.roll(g, shift)
            l_shift = int(shift * (len(l) / len(g)))
            l_aug = np.roll(l, l_shift)
            
            scale = np.random.uniform(0.5, 1.5)
            g_aug = g_aug * scale
            l_aug = l_aug * scale
        
        elif fp_type == 'no_transit':
            # Take a CP, but replace the transit region with pure noise (so there is no dip)
            idx = np.random.randint(num_cp)
            g = real_cp_global[idx].copy()
            l = real_cp_local[idx].copy()
            
            # Zero out the transit region (bins 75 to 125 of local view)
            l[75:125] = 0.0
            # Zero out global view as well
            g[:] = 0.0
            
            g_aug = g
            l_aug = l
            
        elif fp_type == 'off_center':
            # Shift the transit so far that it is not centered (CNN learns center alignment is crucial)
            idx = np.random.randint(num_cp)
            g = real_cp_global[idx].copy()
            l = real_cp_local[idx].copy()
            
            # Roll by a large shift (35 to 70 bins)
            large_shift = np.random.choice([np.random.randint(-70, -35), np.random.randint(35, 70)])
            l_aug = np.roll(l, large_shift)
            g_aug = np.roll(g, large_shift * 10)
            
        elif fp_type == 'secondary_eclipse':
            # Create a secondary eclipse: a primary dip plus a secondary smaller dip at a different phase
            idx = np.random.randint(num_cp)
            g = real_cp_global[idx].copy()
            l = real_cp_local[idx].copy()
            
            # Duplicate and shift the dip in global view (e.g., secondary eclipse at phase 0.5)
            g_sec = np.roll(g, len(g) // 2) * np.random.uniform(0.2, 0.5)
            g_aug = g + g_sec
            
            # Local view remains centered on primary, but we might add a small depth asymmetry or keep it
            l_aug = l
            
        # Add random noise, offset, and scale on top
        std_g = np.std(g) if np.std(g) > 0 else 1e-5
        std_l = np.std(l) if np.std(l) > 0 else 1e-5
        
        noise_std_g = std_g * np.random.uniform(0.01, 0.05)
        noise_std_l = std_l * np.random.uniform(0.01, 0.05)
        
        g_aug += np.random.normal(0, noise_std_g, g_aug.shape)
        l_aug += np.random.normal(0, noise_std_l, l_aug.shape)
        
        offset_g = np.random.uniform(-0.05, 0.05) * std_g
        offset_l = np.random.uniform(-0.05, 0.05) * std_l
        g_aug += offset_g
        l_aug += offset_l

        # Normalize final augmented views to unit standard deviation
        std_aug_g = np.std(g_aug)
        if std_aug_g > 0.0:
            g_aug = g_aug / std_aug_g
        std_aug_l = np.std(l_aug)
        if std_aug_l > 0.0:
            l_aug = l_aug / std_aug_l
        
        global_views.append(g_aug)
        local_views.append(l_aug)
        labels.append(0)
        
    return np.array(global_views), np.array(local_views), np.array(labels)


def main():
    parser = argparse.ArgumentParser(description="Deep training experiment for AstroNet.")
    parser.add_argument("--data_dir", default="data/processed", help="Directory containing processed numpy views")
    parser.add_argument("--model_type", choices=['baseline', 'advanced'], default='baseline')
    parser.add_argument("--model_path", default="models/astronet_best.h5", help="Path to save the best model")
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--val_split", type=float, default=0.2)
    args = parser.parse_args()

    if not os.path.exists("models"):
        os.makedirs("models")

    log.info("Loading dataset...")
    g_data, l_data, y_data = load_dataset(args.data_dir)

    if len(g_data) == 0:
        log.warning("No data found. Please run fetch_lightcurves and preprocess scripts first.")
        return

    # Shuffle and Reshape
    indices = np.random.permutation(len(g_data))
    g_data = g_data[indices].reshape(g_data.shape + (1,))
    l_data = l_data[indices].reshape(l_data.shape + (1,))
    y_data = y_data[indices]

    log.info(f"Loaded {len(g_data)} samples. Split: {1-args.val_split:.1f}/{args.val_split:.1f}")

    # Initialize model
    if args.model_type == 'advanced':
        astronet = AdvancedAstroNetModel()
    else:
        astronet = AstroNetModel()

    # Callbacks
    my_callbacks = [
        callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
        callbacks.ModelCheckpoint(args.model_path, monitor='val_accuracy', save_best_only=True),
        callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5),
        callbacks.CSVLogger(os.path.join("outputs", f"training_log_{args.model_type}.csv"))
    ]

    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    log.info(f"Starting {args.model_type} training for {args.epochs} epochs...")
    history = astronet.model.fit(
        {'global_input': g_data, 'local_input': l_data},
        y_data,
        epochs=args.epochs,
        batch_size=args.batch_size,
        validation_split=args.val_split,
        callbacks=my_callbacks,
        verbose=1
    )

    log.info("Training complete.")
    log.info(f"Best validation accuracy: {max(history.history['val_accuracy']):.4f}")
    
    # Explicitly save final weights
    final_model_path = args.model_path.replace('.h5', '_final.keras')
    astronet.save(final_model_path)
    log.info(f"Final model saved to {final_model_path}")

if __name__ == "__main__":
    main()
