# 🎵 DSP Processor App

A comprehensive, interactive **Digital Signal Processing (DSP)** application built with **Streamlit**. This tool allows users to visualize, analyze, and manipulate audio signals in real-time, making it an excellent resource for education and signal processing experimentation.

## 🚀 Features

### 1. 🏠 Home
- **Drag & Drop Interface**: Easily upload `.WAV` files using a custom-styled uploader.
- **Audio Playback**: Listen to your original and processed audio files directly in the browser.
- **File History**: Quickly access your recently uploaded files.

### 2. 📉 Sampling & Quantization
Explore the fundamentals of digital audio:
- **Resampling**: Change the sampling rate and observe the effects on signal quality.
- **Nyquist Theorem**: Automatic warnings when the sampling rate falls below the Nyquist rate ($f_s < 2f_{max}$).
- **Quantization**: Adjust bit depth (e.g., 8-bit, 4-bit) and visualize the **Quantization Error**.
- **Waveform Zoom**: Interactive plots to inspect individual samples.

### 3. 📊 FFT Analysis (Frequency Domain)
Perform detailed spectral analysis:
- **DFT Equation**: View the mathematical foundation of the Discrete Fourier Transform.
- **Interactive Plots**: Switch between **Linear** and **Logarithmic (dB)** scales.
- **Peak Detection**: Automatically identifies and displays the dominant frequency component.
- **SNR Calculation**: Real-time Signal-to-Noise Ratio (SNR) computation.

### 4. 🔇 Denoising
Clean up noisy audio signals:
- **Butterworth Low-Pass Filter**: Adjustable cutoff frequency and filter order.
- **Filter Response**: Visual magnitude response of the applied filter ($|H(j\omega)|$).
- **Energy Analysis**: Calculates the frequency threshold containing 95% of the signal's energy.
- **Comparison**: Side-by-side view of Original vs. Filtered signals in both time and frequency domains.

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **Streamlit**: For the interactive web interface.
- **NumPy & SciPy**: For high-performance numerical processing and DSP algorithms.
- **Plotly**: For interactive, high-quality visualizations.
- **SoundFile**: For robust audio file handling.

---

## 📦 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/dsp-processor-app.git
   cd dsp-processor-app
   ```

2. **Create a Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Mac/Linux
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Usage

Run the application locally:

```bash
streamlit run main.py
```

The app will open in your default web browser at `http://localhost:8501`.

---

## 📂 Project Structure

```
dsp-processor-app/
├── app/
│   ├── tabs/           # UI logic for each tab (Sampling, FFT, Denoising)
│   └── utils.py        # Helper functions and custom CSS
├── dsp/
│   ├── fft_processor.py    # FFT algorithms and SNR calculations
│   ├── filter_processor.py # Filter design and application
│   └── sampler.py          # Resampling and quantization logic
├── main.py             # Application entry point
├── requirements.txt    # Python dependencies
├── packages.txt        # System dependencies (for Streamlit Cloud)
└── README.md           # Project documentation
```

## ☁️ Deployment

This app is optimized for **Streamlit Cloud**:
1. Push your code to GitHub.
2. Log in to [Streamlit Cloud](https://streamlit.io/cloud).
3. Connect your repository and select `main.py` as the entry point.
4. The `packages.txt` file ensures `libsndfile1` is installed for audio support.

---

**Created for DSP Course Project**
