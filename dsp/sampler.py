import numpy as np
from scipy.signal import resample

def sample_signal(signal, original_fs, new_fs):
    """
    Resamples the signal from original_fs to new_fs.
    
    Args:
        signal (np.array): The input signal.
        original_fs (int): Original sampling rate.
        new_fs (int): Target sampling rate.
        
    Returns:
        np.array: Resampled signal.
        np.array: Time axis for the resampled signal.
    """
    if new_fs == original_fs:
        t = np.arange(len(signal)) / original_fs
        return signal, t
    
    # Calculate number of samples in the new signal
    num_samples = int(len(signal) * new_fs / original_fs)
    
    # Resample
    resampled_signal = resample(signal, num_samples)
    
    # Create time axis
    t = np.arange(num_samples) / new_fs
    
    return resampled_signal, t

def quantize_signal(signal, n_bits):
    """
    Quantizes the signal to n_bits.
    
    Args:
        signal (np.array): Input signal (assumed to be normalized between -1 and 1 or similar).
        n_bits (int): Number of bits for quantization.
        
    Returns:
        np.array: Quantized signal.
        np.array: Quantization error.
    """
    # Number of levels
    L = 2 ** n_bits
    
    # Normalize signal to [-1, 1] if not already (handling potential max abs > 1)
    max_val = np.max(np.abs(signal))
    if max_val == 0:
        return signal, np.zeros_like(signal)
        
    norm_signal = signal / max_val
    
    # Quantize
    # Map [-1, 1] to [0, L-1]
    # step size delta = 2 / L (approx) or 2 / (L-1)
    # Using mid-tread quantization
    
    # Scale to levels
    # We want to map -1 to 0 and 1 to L-1
    # formula: floor((x + 1) * (L-1) / 2 + 0.5)
    
    scaled = (norm_signal + 1) * (L - 1) / 2
    quantized_levels = np.round(scaled)
    
    # Clamp to [0, L-1]
    quantized_levels = np.clip(quantized_levels, 0, L - 1)
    
    # Map back to [-1, 1]
    quantized_norm = (quantized_levels * 2 / (L - 1)) - 1
    
    # Denormalize
    quantized_signal = quantized_norm * max_val
    
    error = signal - quantized_signal
    
    return quantized_signal, error
