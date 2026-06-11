# Lightkurve Repo Notes
- **Purpose**: High-level data analysis library for Kepler and TESS.
- **Useful Folders**: `src/lightkurve/search.py`, `src/lightkurve/lightcurve.py`.
- **Setup Difficulty**: Low. Pip installable.
- **What can be borrowed**: MAST API search logic, BLS periodogram implementation, folding and stitching logic.
- **What should be ignored**: Low-level PRF (Pixel Response Function) modeling unless doing custom aperture photometry.
- **How it fits the final system**: Acts as the primary data acquisition and initial signal discovery layer.
