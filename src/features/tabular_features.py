import numpy as np

class TabularFeatureExtractor:
    """Extract tabular features from lightcurve and BLS results."""
    def __init__(self):
        pass

    def extract(self, lc, bls_results, snr, odd_even, secondary_depth):
        """
        Create a 1D feature vector for tabular branch of NN or XGBoost.
        """
        period = bls_results.get('period', 0.0)
        duration = bls_results.get('duration', 0.0)
        
        # Compute depth roughly
        folded = lc.fold(period=period, epoch_time=bls_results.get('t0', 0.0))
        in_transit = (folded.time.value > -duration/2) & (folded.time.value < duration/2)
        out_transit = ~in_transit
        
        if len(folded[in_transit]) > 0 and len(folded[out_transit]) > 0:
            depth = np.nanmedian(folded.flux.value[out_transit]) - np.nanmedian(folded.flux.value[in_transit])
        else:
            depth = 0.0
            
        features = [
            period,
            duration,
            depth,
            snr,
            odd_even.get('odd_depth', 0.0),
            odd_even.get('even_depth', 0.0),
            odd_even.get('significance', 0.0),
            secondary_depth
        ]
        
        # Replace NaNs with 0
        features = np.nan_to_num(features, nan=0.0)
        return np.array(features)
