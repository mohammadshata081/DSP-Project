import unittest
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dsp.sampler import sample_signal, quantize_signal
from dsp.fft_processor import compute_fft
from dsp.filter_processor import apply_lowpass

class TestDSP(unittest.TestCase):
    
    def setUp(self):
        self.fs = 1000
        self.t = np.arange(0, 1, 1/self.fs)
        self.f_sig = 10
        self.signal = np.sin(2 * np.pi * self.f_sig * self.t)
        
    def test_sampling(self):
        new_fs = 500
        resampled, t_res = sample_signal(self.signal, self.fs, new_fs)
        
        expected_samples = int(len(self.signal) * new_fs / self.fs)
        self.assertEqual(len(resampled), expected_samples)
        
    def test_quantization(self):
        n_bits = 4
        quantized, error = quantize_signal(self.signal, n_bits)
        
        self.assertTrue(np.all(quantized >= -1))
        self.assertTrue(np.all(quantized <= 1))
        
        unique_levels = len(np.unique(quantized))
        self.assertLessEqual(unique_levels, 2**n_bits)
        
    def test_fft(self):
        freqs, mag, phase = compute_fft(self.signal, self.fs)
        
        peak_idx = np.argmax(mag)
        peak_freq = freqs[peak_idx]
        
        self.assertAlmostEqual(peak_freq, self.f_sig, delta=1)
        
    def test_lowpass(self):
        high_freq_sig = np.sin(2 * np.pi * 400 * self.t)
        mixed_sig = self.signal + high_freq_sig
        
        filtered = apply_lowpass(mixed_sig, self.fs, cutoff=100)
        
        freqs, mag, _ = compute_fft(filtered, self.fs)
        
        idx_10 = np.argmin(np.abs(freqs - 10))
        mag_10 = mag[idx_10]
        
        idx_400 = np.argmin(np.abs(freqs - 400))
        mag_400 = mag[idx_400]
        
        self.assertGreater(mag_10, mag_400 * 10) # At least 10x attenuation

if __name__ == '__main__':
    unittest.main()
