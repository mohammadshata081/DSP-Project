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
    
    num_samples = int(len(signal) * new_fs / original_fs)
    
    resampled_signal = resample(signal, num_samples)
    
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
    L = 2 ** n_bits
    
    max_val = np.max(np.abs(signal))
    if max_val == 0:
        return signal, np.zeros_like(signal)
        
    norm_signal = signal / max_val
    
    
    
    scaled = (norm_signal + 1) * (L - 1) / 2
    quantized_levels = np.round(scaled)
    
    quantized_levels = np.clip(quantized_levels, 0, L - 1)
    
    quantized_norm = (quantized_levels * 2 / (L - 1)) - 1
    
    quantized_signal = quantized_norm * max_val
    
    error = signal - quantized_signal
    
    return quantized_signal, error
