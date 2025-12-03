import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.signal import spectrogram
from dsp.filter_processor import apply_lowpass, apply_spectral_subtraction, apply_wiener_filter
from dsp.fft_processor import compute_fft
from app.utils import render_header, get_audio_download_link

def render():
    render_header("Noise Cancellation", "")
    
    if 'audio_data' not in st.session_state:
        st.warning("Please upload an audio file in the Home tab first.")
        return

    data = st.session_state['audio_data']
    fs = st.session_state['fs']
    
    # Filter Analysis
    st.markdown("### 📘 Filter Analysis")
    st.markdown("""
    **Low-pass filters** are designed to pass signals with a frequency lower than a certain cutoff frequency and attenuate signals with frequencies higher than the cutoff frequency.
    """)
    
    st.latex(r"|H(j\omega)| = \frac{1}{\sqrt{1 + (\frac{\omega}{\omega_c})^{2n}}}")
    
    st.markdown("""
    In audio processing, they are commonly used for **denoising** by removing high-frequency hiss or static noise while preserving the core audio content (voice, music) which typically resides in lower frequencies.
    
    The recommended cutoff frequency $f_{c}$ is determined such that 95% of the total spectral energy is contained below it:
    """)
    
    st.latex(r"\sum_{f=0}^{f_{c}} |X(f)|^2 = 0.95 \times \sum_{f=0}^{f_{max}} |X(f)|^2")
    
    st.markdown("""
    This threshold is chosen to preserve the majority of the signal's energy (and thus information) while filtering out high-frequency noise components that typically carry less significant information.
    """)
    
    # Controls
    st.markdown("### 🎛️ Filter Controls")
    
    # Only Low-pass Filter is available
    method = "Low-pass Filter"
    
    # Calculate Effective Cutoff (95% Energy Bandwidth)
    from dsp.fft_processor import compute_fft
    f_spec, mag_spec, _ = compute_fft(data, fs, window_type='Hann', scale='Linear')
    total_energy = np.sum(mag_spec**2)
    cumulative_energy = np.cumsum(mag_spec**2)
    # Find frequency where 95% of energy is contained
    idx_95 = np.searchsorted(cumulative_energy, 0.95 * total_energy)
    effective_cutoff = f_spec[idx_95]
    
    st.info(f"💡 Recommended Cutoff Frequency (95% Energy): **{effective_cutoff:.0f} Hz**")
    
    cutoff = st.slider(
        "Cutoff Frequency (Hz)",
        min_value=100,
        max_value=int(fs/2)-100,
        value=int(effective_cutoff) if 100 < effective_cutoff < (fs/2)-100 else 3000,
        step=100
    )
    processed_data = apply_lowpass(data, fs, cutoff)
            
    # Playback
    st.markdown("### 🎧 Audio Preview")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Original**")
        st.audio(data, sample_rate=fs)
    with col2:
        st.markdown(f"**Processed**")
        st.audio(processed_data, sample_rate=fs)
        
    # Download
    st.markdown(get_audio_download_link(processed_data, fs, f"cleaned_{method.lower().replace(' ', '_')}.wav"), unsafe_allow_html=True)
    
    # Visualization
    st.markdown("### 📊 Spectrogram Comparison")
    
    # Compute Spectrograms
    f_orig, t_orig, Sxx_orig = spectrogram(data, fs)
    f_proc, t_proc, Sxx_proc = spectrogram(processed_data, fs)
    
    # Log scale for better visibility
    Sxx_orig_log = 10 * np.log10(Sxx_orig + 1e-10)
    Sxx_proc_log = 10 * np.log10(Sxx_proc + 1e-10)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = go.Figure(data=go.Heatmap(
            z=Sxx_orig_log,
            x=t_orig,
            y=f_orig,
            colorscale='Viridis'
        ))
        fig1.update_layout(
            title="Original Spectrogram",
            xaxis_title="Time (s)",
            yaxis_title="Frequency (Hz)",
            template="plotly_dark",
            height=400
        )
        st.plotly_chart(fig1, use_container_width=True)
        
    with col2:
        fig2 = go.Figure(data=go.Heatmap(
            z=Sxx_proc_log,
            x=t_proc,
            y=f_proc,
            colorscale='Viridis'
        ))
        fig2.update_layout(
            title="Processed Spectrogram",
            xaxis_title="Time (s)",
            yaxis_title="Frequency (Hz)",
            template="plotly_dark",
            height=400
        )
        st.plotly_chart(fig2, use_container_width=True)
        
    # Spectrum Comparison
    st.markdown("### 📉 Frequency Spectrum Comparison")
    
    # Compute FFTs
    freqs_orig, mag_orig, _ = compute_fft(data, fs, window_type='Hann', scale='Log')
    freqs_proc, mag_proc, _ = compute_fft(processed_data, fs, window_type='Hann', scale='Log')
    
    fig_spec = go.Figure()
    
    # Original Spectrum
    fig_spec.add_trace(go.Scatter(
        x=freqs_orig,
        y=mag_orig,
        mode='lines',
        name='Original Signal',
        line=dict(color='#3B82F6', width=1.5),
        opacity=0.6
    ))
    
    # Processed Spectrum
    fig_spec.add_trace(go.Scatter(
        x=freqs_proc,
        y=mag_proc,
        mode='lines',
        name='Processed Signal',
        line=dict(color='#10B981', width=1.5),
        opacity=0.9
    ))
    
    fig_spec.update_layout(
        title="Magnitude Spectrum Comparison (Log Scale)",
        xaxis_title="Frequency (Hz)",
        yaxis_title="Magnitude (dB)",
        template="plotly_dark",
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig_spec, use_container_width=True)
