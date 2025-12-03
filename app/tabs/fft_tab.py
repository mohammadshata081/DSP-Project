import streamlit as st
import numpy as np
import plotly.graph_objects as go
from dsp.fft_processor import compute_fft
from app.utils import render_header

def render():
    render_header("FFT Analysis", "")
    
    if 'audio_data' not in st.session_state:
        st.warning("Please upload an audio file in the Home tab first.")
        return

    data = st.session_state['audio_data']
    fs = st.session_state['fs']
    
    st.markdown("### 🔍 Analysis")
    
    st.markdown("""
    **Fourier Analysis** decomposes a signal into its constituent frequencies. 
    It transforms the signal from the *Time Domain* to the *Frequency Domain*, 
    revealing the dominant frequencies (basis functions) that make up the sound.
    
    **Algorithm**: This app uses the **Fast Fourier Transform (FFT)**, typically implemented using the **Cooley-Tukey algorithm**, to efficiently compute the Discrete Fourier Transform (DFT).
    """)
    
    st.latex(r"X[k] = \sum_{n=0}^{N-1} x[n] e^{-j2\pi \frac{kn}{N}}")
    
    st.markdown("""
    where $x[n]$ is the input signal, $X[k]$ is the spectrum, $N$ is the number of samples, and $k$ is the frequency index.
    
    **Signal-to-Noise Ratio (SNR)**:
    """)
    
    st.latex(r"SNR = 10 \cdot \log_{10}\left(\frac{P_{signal}}{P_{noise}}\right)")
    
    st.markdown("""
    where $P_{signal}$ is the peak power and $P_{noise}$ is the mean power of the rest of the spectrum.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎛️ Controls")
        scale = st.radio(
            "Magnitude Scale",
            ["Linear", "Log"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
    freqs, magnitude_linear, phase = compute_fft(data, fs, window_type='Hann', scale='Linear')

    with col2:
        peak_idx = np.argmax(magnitude_linear)
        p_signal = magnitude_linear[peak_idx]**2
        
        mask = np.ones(len(magnitude_linear), dtype=bool)
        mask[max(0, peak_idx-2):min(len(magnitude_linear), peak_idx+3)] = False
        
        if np.any(mask):
            p_noise = np.mean(magnitude_linear[mask]**2)
            snr = 10 * np.log10(p_signal / p_noise) if p_noise > 0 else float('inf')
        else:
            snr = float('inf')
            
        st.metric("Signal-to-Noise Ratio (SNR)", f"{snr:.2f} dB")
        
    if scale == "Log":
        magnitude = 20 * np.log10(magnitude_linear + 1e-10)
    else:
        magnitude = magnitude_linear
    
    st.markdown("### 📊 Spectrum")
    
    fig_mag = go.Figure()
    
    fig_mag.add_trace(go.Scatter(
        x=freqs,
        y=magnitude,
        mode='lines',
        name='Magnitude',
        line=dict(color='#8B5CF6', width=1.5),
        fill='tozeroy',
        fillcolor='rgba(139, 92, 246, 0.2)'
    ))
    
    fig_mag.update_layout(
        title="Magnitude Spectrum",
        xaxis_title="Frequency (Hz)",
        yaxis_title="Magnitude (dB)" if scale == "Log" else "Magnitude",
        template="plotly_dark",
        height=500
    )
    
    st.plotly_chart(fig_mag, use_container_width=True)
    
    st.markdown("### 🏔️ Peak Frequencies")
    
    if len(magnitude) > 1:
        mag_no_dc = magnitude[1:]
        freqs_no_dc = freqs[1:]
        
        top_indices = np.argsort(mag_no_dc)[-5:][::-1]
        top_freqs = freqs_no_dc[top_indices]
        top_mags = mag_no_dc[top_indices]
        
        cols = st.columns(5)
        for i, (f, m) in enumerate(zip(top_freqs, top_mags)):
            with cols[i]:
                if scale == "Linear":
                    mag_str = f"{m:.5f}"
                else:
                    mag_str = f"{m:.2f}"
                    
                st.markdown(f"""
                <div style="background: #1F2937; padding: 10px; border-radius: 8px; text-align: center; border: 1px solid #374151;">
                    <div style="color: #9CA3AF; font-size: 0.8rem;">Peak {i+1}</div>
                    <div style="font-weight: bold; color: #60A5FA;">{f:.1f} Hz</div>
                    <div style="font-size: 0.8rem;">{mag_str}</div>
                </div>
                """, unsafe_allow_html=True)

