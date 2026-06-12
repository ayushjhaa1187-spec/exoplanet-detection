import numpy as np

class DecisionEngine:
    """Combines model outputs and physical vetting tests into a final decision."""
    
    CLASSES = [
        "planet_transit",
        "eclipsing_binary",
        "blend_or_contamination",
        "stellar_variability",
        "noise_no_signal"
    ]
    
    def __init__(self, snr_threshold=7.1, secondary_eclipse_threshold=0.01):
        self.snr_threshold = snr_threshold
        self.secondary_eclipse_threshold = secondary_eclipse_threshold

    def evaluate(self, model_probs, snr, odd_even, secondary_depth):
        """
        Evaluate final candidate status.
        model_probs: array of 5 probabilities corresponding to CLASSES
        """
        base_class_idx = np.argmax(model_probs)
        base_class = self.CLASSES[base_class_idx]
        confidence = float(model_probs[base_class_idx])
        
        explanation = []
        final_class = base_class
        
        # 1. SNR Check
        snr_pass = snr >= self.snr_threshold
        if not snr_pass:
            explanation.append(f"SNR ({snr:.2f}) is below threshold ({self.snr_threshold}). Likely noise.")
            final_class = "noise_no_signal"
            confidence = max(0.5, confidence)
            
        # 2. Odd-Even Check (Eclipsing Binary indicator)
        odd_even_pass = not odd_even.get('is_suspicious', False)
        if not odd_even_pass:
            explanation.append("Significant depth difference between odd and even transits. Likely Eclipsing Binary.")
            if final_class == "planet_transit":
                final_class = "eclipsing_binary"
                confidence = 0.8
                
        # 3. Secondary Eclipse Check
        secondary_pass = secondary_depth < self.secondary_eclipse_threshold
        if not secondary_pass:
            explanation.append(f"Secondary eclipse detected (depth: {secondary_depth:.4f}). Likely Eclipsing Binary or blend.")
            if final_class == "planet_transit":
                final_class = "eclipsing_binary"
                confidence = 0.8
                
        if snr_pass and odd_even_pass and secondary_pass and final_class == "planet_transit":
            explanation.append("Passed all vetting tests. Strong planet candidate.")
            
        return {
            "final_class": final_class,
            "confidence": confidence,
            "model_probability": dict(zip(self.CLASSES, [float(p) for p in model_probs])),
            "vetting_flags": {
                "snr_pass": snr_pass,
                "odd_even_pass": odd_even_pass,
                "secondary_eclipse_pass": secondary_pass
            },
            "explanation": " ".join(explanation)
        }
