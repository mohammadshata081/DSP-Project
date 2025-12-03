import numpy as np
from scipy.fft import rfft, rfftfreq

def compute_fft(signal, fs, window_type='None', scale='Linear'):
    """
    Computes the FFT of the signal.
    
    Args:
        signal (np.array): Input signal.
        fs (int): Sampling rate.
        window_type (str): Window function ('None', 'Hann', 'Hamming').
        scale (str): Magnitude scale ('Linear', 'Log').
        
    Returns:
        np.array: Frequency axis (positive half).
        np.array: Magnitude spectrum (positive half).
        np.array: Phase spectrum (positive half).
    """
    N = len(signal)
    
    # Apply window
    if window_type == 'Hann':
        window = np.hanning(N)
        signal = signal * window
    elif window_type == 'Hamming':
        window = np.hamming(N)
        signal = signal * window
        
    # Compute FFT (using rfft for real-valued signals is faster)
    yf = rfft(signal)
    xf = rfftfreq(N, 1/fs)
    
    freqs = xf
    
    # Magnitude
    magnitude = np.abs(yf)
    
    # Normalize magnitude
    magnitude = magnitude / N
    
    if scale == 'Log':
        # Add small epsilon to avoid log(0)
        magnitude = 20 * np.log10(magnitude + 1e-10)
        
    # Phase
    phase = np.angle(yf)
    
    return freqs, magnitude, phase
