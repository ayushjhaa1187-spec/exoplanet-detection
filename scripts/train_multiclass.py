import os
import sys
import numpy as np
import pandas as pd
import logging
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.models.multiclass_model import HybridMulticlassModel

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

def load_data(labels_csv, views_dir, tabular_npy):
    df = pd.read_csv(labels_csv)
    tab = np.load(tabular_npy)
    
    globals_list = []
    locals_list = []
    y_list = []
    tab_list = []
    
    for idx, row in df.iterrows():
        tic = row['TIC_ID']
        label = row['Label_Idx']
        g_path = os.path.join(views_dir, tic, 'global.npy')
        l_path = os.path.join(views_dir, tic, 'local.npy')
        
        if os.path.exists(g_path) and os.path.exists(l_path):
            globals_list.append(np.load(g_path))
            locals_list.append(np.load(l_path))
            tab_list.append(tab[idx])
            
            # One-hot encoding for 5 classes
            y_one_hot = np.zeros(5)
            y_one_hot[label] = 1.0
            y_list.append(y_one_hot)
            
    X_global = np.array(globals_list)
    X_local = np.array(locals_list)
    X_tab = np.array(tab_list)
    Y = np.array(y_list)
    
    # Add channel dimension
    X_global = np.expand_dims(X_global, axis=-1)
    X_local = np.expand_dims(X_local, axis=-1)
    
    return X_global, X_local, X_tab, Y

def main():
    log.info("Loading synthetic multi-class data...")
    X_g, X_l, X_t, Y = load_data(
        "data/labels/synthetic_master_labels.csv", 
        "data/features/views", 
        "data/features/tabular_features.npy"
    )
    
    log.info(f"Loaded {len(Y)} samples.")
    
    # Split: Train 70%, Val 15%, Test 15%
    X_g_train, X_g_tmp, X_l_train, X_l_tmp, X_t_train, X_t_tmp, Y_train, Y_tmp = train_test_split(
        X_g, X_l, X_t, Y, test_size=0.3, random_state=42, stratify=np.argmax(Y, axis=1)
    )
    
    X_g_val, X_g_test, X_l_val, X_l_test, X_t_val, X_t_test, Y_val, Y_test = train_test_split(
        X_g_tmp, X_l_tmp, X_t_tmp, Y_tmp, test_size=0.5, random_state=42, stratify=np.argmax(Y_tmp, axis=1)
    )
    
    log.info(f"Train: {len(Y_train)}, Val: {len(Y_val)}, Test: {len(Y_test)}")
    
    model = HybridMulticlassModel()
    
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    ]
    
    log.info("Training Hybrid Multiclass Model...")
    model.model.fit(
        [X_g_train, X_l_train, X_t_train], Y_train,
        validation_data=([X_g_val, X_l_val, X_t_val], Y_val),
        epochs=20,
        batch_size=32,
        callbacks=callbacks,
        verbose=1
    )
    
    os.makedirs("models", exist_ok=True)
    model.model.save("models/multiclass_astronet.keras")
    log.info("Saved models/multiclass_astronet.keras")
    
    # Save test set for evaluate_model.py
    os.makedirs("data/interim", exist_ok=True)
    np.savez("data/interim/test_set.npz", 
             X_g_test=X_g_test, X_l_test=X_l_test, X_t_test=X_t_test, Y_test=Y_test)

if __name__ == "__main__":
    main()
