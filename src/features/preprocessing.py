import os
import numpy as np
import logging

log = logging.getLogger(__name__)

def bin_and_aggregate(x, y, num_bins, bin_width=None, x_min=None, x_max=None, aggr_fn=np.nanmedian):
    """Aggregates y-values in uniform intervals (bins) along the x-axis."""
    if num_bins < 2:
        raise ValueError("num_bins must be at least 2.")
    
    x_len = len(x)
    if x_len < 2:
        return np.zeros(num_bins), np.zeros(num_bins)
    
    x_min = x_min if x_min is not None else x[0]
    x_max = x_max if x_max is not None else x[-1]
    
    if x_min >= x_max:
        return np.zeros(num_bins), np.zeros(num_bins)
 
    bin_width = bin_width if bin_width is not None else (x_max - x_min) / num_bins
    bin_spacing = (x_max - x_min - bin_width) / (num_bins - 1) if num_bins > 1 else 0

    result = np.full(num_bins, np.nan)
    bin_counts = np.zeros(num_bins, dtype=int)

    # Simplified binning for efficiency
    for i in range(num_bins):
        b_min = x_min + i * bin_spacing
        b_max = b_min + bin_width
        mask = (x >= b_min) & (x < b_max)
        if np.any(mask):
            result[i] = aggr_fn(y[mask])
            bin_counts[i] = np.sum(mask)
    
    return result, bin_counts


class ExoplanetPreprocessor:
    def __init__(self, global_bins=2001, local_bins=201):
        self.global_bins = global_bins
        self.local_bins = local_bins

    def process(self, lc, period, t0, duration):
        """Generate global and local views of the lightcurve."""
        log.info("Generating global and local views...")
        
        # Fold the lightcurve
        folded_lc = lc.fold(period=period, epoch_time=t0)
        if folded_lc is None:
            log.error("Folded lightcurve is None!")
            return np.zeros(self.global_bins), np.zeros(self.local_bins)
        
        # Remove NaNs from the folded light curve flux
        flux_vals = folded_lc.flux.value
        clean_mask = ~np.isnan(flux_vals)
        folded_lc = folded_lc[clean_mask]
        
        folded_lc.sort('time')
        
        x = folded_lc.time.value
        y = folded_lc.flux.value
        
        # Global view: all data points folded
        global_view, _ = bin_and_aggregate(x, y, self.global_bins, x_min=-period/2, x_max=period/2)
        
        # Local view: zoom in on the transit
        local_view_width = 4 * duration
        local_view, _ = bin_and_aggregate(x, y, self.local_bins, x_min=-local_view_width/2, x_max=local_view_width/2)
        
        # Normalize: center at 0, ignoring NaNs
        global_view -= np.nanmedian(global_view)
        local_view -= np.nanmedian(local_view)
        
        # Final safety check for NaNs: fill empty bins (which are NaN) with 0.0 (baseline)
        global_view[np.isnan(global_view)] = 0.0
        local_view[np.isnan(local_view)] = 0.0
        
        return global_view, local_view

    def augment(self, global_view, local_view, shift_max=10):
        """Perform random cyclic shifts for data augmentation."""
        shift = np.random.randint(-shift_max, shift_max + 1)
        aug_global = np.roll(global_view, shift)
        
        # Local shift should be smaller or proportional
        local_shift = int(shift * (self.local_bins / self.global_bins))
        aug_local = np.roll(local_view, local_shift)
        
        return aug_global, aug_local

    def save_views(self, target_id, global_view, local_view, outdir="data/processed"):
        """Save processed views as numpy files."""
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        
        target_dir = os.path.join(outdir, target_id.replace(" ", "_"))
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        np.save(os.path.join(target_dir, "global_view.npy"), global_view)
        np.save(os.path.join(target_dir, "local_view.npy"), local_view)
        log.info(f"Saved views for {target_id} to {target_dir}")
