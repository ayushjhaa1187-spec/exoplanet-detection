import os
import json
import numpy as np
import logging
from sklearn.metrics import classification_report, confusion_matrix, f1_score
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.models import load_model

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

CLASSES = [
    "planet_transit",
    "eclipsing_binary",
    "blend_or_contamination",
    "stellar_variability",
    "noise_no_signal"
]

def main():
    test_data_path = "data/interim/test_set.npz"
    model_path = "models/multiclass_astronet.keras"
    outdir = "outputs/evaluation"
    
    os.makedirs(outdir, exist_ok=True)
    
    if not os.path.exists(test_data_path) or not os.path.exists(model_path):
        log.error("Missing test set or model. Please run scripts/train_multiclass.py first.")
        return
        
    data = np.load(test_data_path)
    X_g = data['X_g_test']
    X_l = data['X_l_test']
    X_t = data['X_t_test']
    Y_true_one_hot = data['Y_test']
    
    Y_true = np.argmax(Y_true_one_hot, axis=1)
    
    log.info("Loading model...")
    model = load_model(model_path)
    
    log.info("Generating predictions...")
    probs = model.predict([X_g, X_l, X_t])
    Y_pred = np.argmax(probs, axis=1)
    
    # 1. Classification Report
    report = classification_report(Y_true, Y_pred, target_names=CLASSES, output_dict=True)
    with open(os.path.join(outdir, "classification_report.json"), "w") as f:
        json.dump(report, f, indent=4)
        
    macro_f1 = f1_score(Y_true, Y_pred, average='macro')
    log.info(f"Macro F1 Score: {macro_f1:.4f}")
    
    # 2. Confusion Matrix
    cm = confusion_matrix(Y_true, Y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=CLASSES, yticklabels=CLASSES)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix: Hybrid Multiclass Model')
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "confusion_matrix.png"))
    plt.close()
    
    log.info(f"Evaluation complete. Artifacts saved to {outdir}")

if __name__ == "__main__":
    main()
