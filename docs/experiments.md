# Experiments Log

## Exp 001: Advanced AstroNet with Attention
- **Date**: 2026-06-11
- **Model**: `AdvancedAstroNetModel` (5-layer Global CNN, 2-layer Local CNN + Multi-head Attention)
- **Dataset**: 6 samples (4 CP, 2 FP)
- **Epochs**: 20 (Early Stopped at 11)
- **Results**:
  - Training Accuracy: 75%
  - Validation Accuracy: 50%
- **Observations**: The dataset is extremely small, but the infrastructure (logging, checkpointing, early stopping) is working perfectly. The model started to overfit early, as expected.
- **Artifacts**: `models/astronet_best.h5`, `outputs/training_log_advanced.csv`
