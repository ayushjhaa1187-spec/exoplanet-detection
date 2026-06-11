# Astronet-Vetting Repo Notes
- **Purpose**: TESS adaptation of AstroNet with vetting-focused TFRecords.
- **Useful Folders**: `astronet/` (TESS models), `light_curve_util/`.
- **Setup Difficulty**: Medium. TESS data formats vary from Kepler.
- **What can be borrowed**: TESS-specific normalization and view adjustments, batch prediction flow.
- **What should be ignored**: Custom TFRecord generation scripts if using NumPy for simplicity.
- **How it fits the final system**: Secondary model reference specifically for TESS-mission data handling.
