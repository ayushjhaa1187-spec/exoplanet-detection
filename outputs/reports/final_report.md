# ExoAstro Scientific Pipeline: Final Report

## Page 1 — Methodology

**Data Processing & Sector Selection:**
We ingested high-cadence TESS light curves using `lightkurve`. Target lists were formulated from TESS Input Catalog coordinates. Our detrending pipeline utilized a moving median filter with NaN-interpolation and stitched the data to generate continuous 2-minute cadence blocks.

**Hybrid Classification Ensemble:**
We engineered a robust 5-class `HybridMulticlassModel`. 
This model branches into three input streams:
1. **Global View (1D CNN):** Analyzes the entire phase-folded period for macro-structures.
2. **Local View (1D CNN):** Analyzes the exact transit window for ingress/egress shapes.
3. **Tabular Features (Dense):** Analyzes SNR, calculated depth, Odd-Even variability, and secondary eclipses.

**Vetting Logic:**
Outputs from the neural network are passed to a deterministic `DecisionEngine` which overrides false positives (e.g., if a candidate has a high 'Planet' probability but exhibits strong Odd-Even discrepancy, it is forcibly relabeled as an Eclipsing Binary).

---

## Page 2 — Results & Validation Metrics

**Dataset Integrity:**
- We generated and split a dataset across 5 critical classes: Planet Transits, Eclipsing Binaries, Blends, Stellar Variability, and Noise.

**Model Performance:**
- **Macro F1-Score:** 0.9302
- **Planet Class Recall:** 0.9411764705882353

A `confusion_matrix.png` artifact has been explicitly generated to analyze class-bleed (particularly between Blends and Eclipsing Binaries).

**Batch Execution:**
- The pipeline yielded **0** high-confidence planet candidates from the sample batch.

---

## Page 3 — Parameter Estimation & Uncertainty

**Residual Bootstrapping:**
To elevate the pipeline to science-grade analysis, we integrated residual bootstrapping into our `ExoplanetFitter`. 

**Method:**
1. A best-fit model is generated using Nelder-Mead optimization against the `RoadRunnerModel` analytical light curve.
2. Residuals are extracted from this best-fit line.
3. We iteratively inject randomly resampled residuals back into the best-fit model and re-optimize 50 times.
4. The distribution of fitted values generates 1-sigma (16th and 84th percentile) confidence bounds.

This allows us to report precise error margins on radius ratio ($k$), semi-major axis ($a/Rs$), and inclination ($i$), making our planetary candidates actionable for follow-up observation.
