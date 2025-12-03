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
    # Simple spectral subtraction implementation
    
    # Estimate noise from the beginning of the signal
    noise_samples = int(noise_estimation_duration * fs)
    if noise_samples >= len(signal):
        noise_samples = len(signal) // 10 # Fallback
        
    noise_segment = signal[:noise_samples]
    
    # Compute noise spectrum
    N = len(signal)
    noise_fft = np.fft.fft(noise_segment, n=N)
    noise_mag = np.abs(noise_fft)
    
    # Compute signal spectrum
    signal_fft = np.fft.fft(signal)
    signal_mag = np.abs(signal_fft)
    signal_phase = np.angle(signal_fft)
    
    # Subtract noise magnitude (spectral subtraction)
    # Using a simple oversubtraction factor if needed, but keeping it basic for now
    clean_mag = np.maximum(signal_mag - noise_mag, 0)
    
    # Reconstruct signal
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
    # Scipy's wiener filter is a spatial smoothing filter, usually for images.
    # For 1D audio, it acts as a local smoothing filter.
    # We can use a small window size.
    
    # However, for audio, a frequency-domain Wiener filter is often preferred.
    # But scipy.signal.wiener is time-domain. Let's use it for simplicity as a "smoothing" filter
    # or implement a frequency domain one.
    # The doc mentions: H(f) = SNR(f) / (SNR(f) + 1)
    
    # Let's implement a basic frequency domain Wiener filter similar to spectral subtraction
    # but with the Wiener gain.
    
    # Estimate noise (similar to spectral subtraction)
    noise_samples = int(0.5 * fs) # Assume 0.5s noise
    if noise_samples >= len(signal):
        noise_samples = len(signal) // 10
        
    noise_segment = signal[:noise_samples]
    N = len(signal)
    
    # Power Spectral Density (PSD)
    noise_fft = np.fft.fft(noise_segment, n=N)
    noise_psd = np.abs(noise_fft) ** 2
    
    signal_fft = np.fft.fft(signal)
    signal_psd = np.abs(signal_fft) ** 2
    
    # Estimate SNR
    # signal_psd contains both signal and noise power (approx)
    # We estimate clean signal power as signal_psd - noise_psd
    clean_psd_est = np.maximum(signal_psd - noise_psd, 0)
    
    # Wiener Filter H(f) = P_clean / (P_clean + P_noise) = P_clean / P_noisy
    # Avoid division by zero
    H = clean_psd_est / (signal_psd + 1e-10)
    
    # Apply filter
    clean_fft = H * signal_fft
    clean_signal = np.fft.ifft(clean_fft)
    
    return np.real(clean_signal)
