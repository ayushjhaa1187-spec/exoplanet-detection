import numpy as np
import logging

log = logging.getLogger(__name__)

import matplotlib.pyplot as plt
import os

class ExoplanetVetter:
    def __init__(self):
        pass

    def plot_folded_transit(self, lc, period, t0, duration, out_path):
        """Generate a diagnostic plot of the folded transit."""
        folded = lc.fold(period=period, epoch_time=t0)
        
        plt.figure(figsize=(10, 6))
        plt.scatter(folded.time.value, folded.flux.value, s=1, color='gray', alpha=0.5, label='Data')
        
        # Bin for clarity
        binned = folded.bin(time_bin_size=duration/10)
        plt.scatter(binned.time.value, binned.flux.value, s=10, color='red', label='Binned')
        
        plt.xlim(-2*duration, 2*duration)
        plt.xlabel("Time from Transit Center (days)")
        plt.ylabel("Normalized Flux")
        plt.title(f"Folded Transit Plot (P={period:.4f}d)")
        plt.legend()
        plt.savefig(out_path)
        plt.close()
        log.info(f"Saved diagnostic plot to {out_path}")

    def calculate_snr(self, lc, period, t0, duration):
        """Calculate the Signal-to-Noise Ratio (SNR) of the transit."""
        folded = lc.fold(period=period, epoch_time=t0)
        mask = (folded.time.value > -duration/2) & (folded.time.value < duration/2)
        
        in_transit_flux = folded.flux.value[mask]
        out_transit_flux = folded.flux.value[~mask]
        
        depth = 1.0 - np.median(in_transit_flux)
        noise = np.std(out_transit_flux) / np.sqrt(len(in_transit_flux))
        
        snr = depth / noise if noise > 0 else 0
        return snr

    def odd_even_test(self, lc, period, t0, duration):
        """Compare the depth of odd and even transits to check for eclipsing binaries."""
        # This is a simplified test
        folded_odd = lc.fold(period=2*period, epoch_time=t0)
        folded_even = lc.fold(period=2*period, epoch_time=t0 + period)
        
        mask_odd = (folded_odd.time.value > -duration/2) & (folded_odd.time.value < duration/2)
        mask_even = (folded_even.time.value > -duration/2) & (folded_even.time.value < duration/2)
        
        depth_odd = 1.0 - np.median(folded_odd.flux.value[mask_odd])
        depth_even = 1.0 - np.median(folded_even.flux.value[mask_even])
        
        # If depths are significantly different, it might be an EB
        diff = np.abs(depth_odd - depth_even)
        is_suspicious = diff > 0.3 * max(depth_odd, depth_even)
        
        return {
            'depth_odd': depth_odd,
            'depth_even': depth_even,
            'is_suspicious': is_suspicious
        }

    def secondary_eclipse_test(self, lc, period, t0, duration):
        """Search for a secondary eclipse at phase 0.5."""
        folded = lc.fold(period=period, epoch_time=t0 + 0.5 * period)
        mask = (folded.time.value > -duration/2) & (folded.time.value < duration/2)
        
        secondary_depth = 1.0 - np.median(folded.flux.value[mask])
        return secondary_depth
