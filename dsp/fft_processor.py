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
    
    if window_type == 'Hann':
        window = np.hanning(N)
        signal = signal * window
    elif window_type == 'Hamming':
        window = np.hamming(N)
        signal = signal * window
        
    yf = rfft(signal)
    xf = rfftfreq(N, 1/fs)
    
    freqs = xf
    
    magnitude = np.abs(yf)
    
    magnitude = magnitude / N
    
    if scale == 'Log':
        magnitude = 20 * np.log10(magnitude + 1e-10)
        
    phase = np.angle(yf)
    
    return freqs, magnitude, phase
