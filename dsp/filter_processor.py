import numpy as np
from scipy.signal import butter, lfilter

def apply_lowpass(signal, fs, cutoff, order=5):
    """
    Applies a low-pass Butterworth filter.
    
    Args:
        signal (np.array): Input signal.
        fs (int): Sampling rate.
        cutoff (float): Cutoff frequency in Hz.
        order (int): Filter order.
        
    Returns:
        np.array: Filtered signal.
    """
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = lfilter(b, a, signal)
    return y

def apply_spectral_subtraction(signal, fs, noise_estimation_duration=0.5):
    """
    Applies spectral subtraction for noise reduction.
    Assumes the first 'noise_estimation_duration' seconds are noise.
    
    Args:
        signal (np.array): Input signal.
        fs (int): Sampling rate.
        noise_estimation_duration (float): Duration in seconds to estimate noise profile.
        
    Returns:
        np.array: Denoised signal.
    """
    
    noise_samples = int(noise_estimation_duration * fs)
    if noise_samples >= len(signal):
        noise_samples = len(signal) // 10 # Fallback
        
    noise_segment = signal[:noise_samples]
    
    N = len(signal)
    noise_fft = np.fft.fft(noise_segment, n=N)
    noise_mag = np.abs(noise_fft)
    
    signal_fft = np.fft.fft(signal)
    signal_mag = np.abs(signal_fft)
    signal_phase = np.angle(signal_fft)
    
    clean_mag = np.maximum(signal_mag - noise_mag, 0)
    
    clean_fft = clean_mag * np.exp(1j * signal_phase)
    clean_signal = np.fft.ifft(clean_fft)
    
    return np.real(clean_signal)

def apply_wiener_filter(signal, fs):
    """
    Applies a Wiener filter.
    
    Args:
        signal (np.array): Input signal.
        fs (int): Sampling rate.
        
    Returns:
        np.array: Filtered signal.
    """
    
    
    
    noise_samples = int(0.5 * fs) # Assume 0.5s noise
    if noise_samples >= len(signal):
        noise_samples = len(signal) // 10
        
    noise_segment = signal[:noise_samples]
    N = len(signal)
    
    noise_fft = np.fft.fft(noise_segment, n=N)
    noise_psd = np.abs(noise_fft) ** 2
    
    signal_fft = np.fft.fft(signal)
    signal_psd = np.abs(signal_fft) ** 2
    
    clean_psd_est = np.maximum(signal_psd - noise_psd, 0)
    
    H = clean_psd_est / (signal_psd + 1e-10)
    
    clean_fft = H * signal_fft
    clean_signal = np.fft.ifft(clean_fft)
    
    return np.real(clean_signal)
