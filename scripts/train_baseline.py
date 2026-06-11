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

def load_dataset(data_dir):
    """Load global and local views and determine labels from directory names."""
    global_views = []
    local_views = []
    labels = []
    
    # Assume directory structure data/processed/[CP|FP]/target_id/
    for category in ['CP', 'FP']:
        cat_dir = os.path.join(data_dir, category)
        if not os.path.exists(cat_dir):
            continue
            
        label = 1 if category == 'CP' else 0
        for target_dir in os.listdir(cat_dir):
            path = os.path.join(cat_dir, target_dir)
            if os.path.isdir(path):
                try:
                    g_view = np.load(os.path.join(path, "global_view.npy"))
                    l_view = np.load(os.path.join(path, "local_view.npy"))
                    global_views.append(g_view)
                    local_views.append(l_view)
                    labels.append(label)
                except Exception as e:
                    log.warning(f"Failed to load data for {target_dir}: {e}")
            
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

if __name__ == "__main__":
    main()
