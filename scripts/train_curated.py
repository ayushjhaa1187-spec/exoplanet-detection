import os
import sys
import logging
import argparse
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import callbacks

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.model import AstroNetModel, AdvancedAstroNetModel

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

def load_curated_dataset(data_dir, mapping_csv, num_classes=4):
    """
    Load curated dataset. 
    mapping_csv should have columns: target_id, label (0 to 3)
    """
    df = pd.read_csv(mapping_csv)
    
    global_views = []
    local_views = []
    labels = []
    
    missing = 0
    for idx, row in df.iterrows():
        target_id = str(row['target_id'])
        label = int(row['label'])
        
        # Determine paths
        # We assume the user has pre-generated the numpy views in data_dir / target_id
        path = os.path.join(data_dir, target_id)
        
        g_path = os.path.join(path, "global_view.npy")
        l_path = os.path.join(path, "local_view.npy")
        
        if not os.path.exists(g_path) or not os.path.exists(l_path):
            missing += 1
            continue
            
        try:
            g_view = np.load(g_path)
            l_view = np.load(l_path)
            
            g_view = np.nan_to_num(g_view, nan=0.0)
            l_view = np.nan_to_num(l_view, nan=0.0)
            
            # Normalization
            std_g = np.std(g_view)
            if std_g > 0.0:
                g_view = g_view / std_g
            std_l = np.std(l_view)
            if std_l > 0.0:
                l_view = l_view / std_l
                
            global_views.append(g_view)
            local_views.append(l_view)
            labels.append(label)
        except Exception as e:
            log.warning(f"Failed to load data for {target_id}: {e}")
            
    log.info(f"Loaded {len(labels)} targets successfully. {missing} targets missing views.")
    
    return np.array(global_views), np.array(local_views), np.array(labels)


def main():
    parser = argparse.ArgumentParser(description="Train multi-class AstroNet on curated dataset.")
    parser.add_argument("--data_dir", default="data/processed", help="Directory containing processed numpy views")
    parser.add_argument("--mapping_csv", required=True, help="Path to CSV file with target_id and label columns")
    parser.add_argument("--model_type", choices=['baseline', 'advanced'], default='advanced')
    parser.add_argument("--model_path", default="models/astronet_best.h5", help="Path to save the best model")
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--val_split", type=float, default=0.2)
    args = parser.parse_args()

    if not os.path.exists("models"):
        os.makedirs("models")

    log.info("Loading curated dataset...")
    g_data, l_data, y_data = load_curated_dataset(args.data_dir, args.mapping_csv)

    if len(g_data) == 0:
        log.error("No data loaded. Check mapping_csv and data_dir paths.")
        return

    # Convert labels to one-hot encoding for categorical_crossentropy
    num_classes = 4
    y_data_one_hot = tf.keras.utils.to_categorical(y_data, num_classes=num_classes)

    # Shuffle
    indices = np.random.permutation(len(g_data))
    g_data = g_data[indices].reshape(g_data.shape + (1,))
    l_data = l_data[indices].reshape(l_data.shape + (1,))
    y_data_one_hot = y_data_one_hot[indices]

    log.info(f"Loaded {len(g_data)} samples. Shape: {g_data.shape}")

    if args.model_type == 'advanced':
        astronet = AdvancedAstroNetModel()
    else:
        astronet = AstroNetModel()

    my_callbacks = [
        callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
        callbacks.ModelCheckpoint(args.model_path, monitor='val_accuracy', save_best_only=True),
        callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5),
        callbacks.CSVLogger(os.path.join("outputs", f"training_curated_log_{args.model_type}.csv"))
    ]

    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    log.info(f"Starting multi-class training for {args.epochs} epochs...")
    history = astronet.model.fit(
        {'global_input': g_data, 'local_input': l_data},
        y_data_one_hot,
        epochs=args.epochs,
        batch_size=args.batch_size,
        validation_split=args.val_split,
        callbacks=my_callbacks,
        verbose=1
    )

    log.info("Training complete.")

if __name__ == "__main__":
    main()
