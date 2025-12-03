import streamlit as st
import numpy as np
import plotly.graph_objects as go
from dsp.sampler import sample_signal, quantize_signal
from app.utils import render_header

def render():
    render_header("Sampling & Quantization", "")
    
    if 'audio_data' not in st.session_state:
        st.warning("Please upload an audio file in the Home tab first.")
        return

    data = st.session_state['audio_data']
    fs = st.session_state['fs']
    
    st.markdown("### 🎛️ Controls")
    
    col1, col2 = st.columns(2)
    
    from dsp.fft_processor import compute_fft
    f_orig, mag_orig, _ = compute_fft(data, fs, window_type='Hann', scale='Linear')
    threshold = 0.01 * np.max(mag_orig)
    significant_freqs = f_orig[mag_orig > threshold]
    f_max = np.max(significant_freqs) if len(significant_freqs) > 0 else 0
    nyquist_rate = 2 * f_max
    
    with col1:
        new_fs = st.slider(
            "Sampling Rate (Hz)", 
            min_value=1000, 
            max_value=44100, 
            value=fs if fs <= 44100 else 44100,
            step=1000,
            help="Nyquist Theorem: fs must be >= 2 * f_max"
        )
        
        if new_fs < nyquist_rate:
            st.warning(f"⚠️ Aliasing Warning! Sampling rate is below Nyquist rate ({nyquist_rate:.0f} Hz).")
        else:
            st.success(f"✅ Sampling rate is sufficient (Nyquist: {nyquist_rate:.0f} Hz).")
        
    with col2:
        n_bits = st.slider(
            "Quantization Bits", 
            min_value=2, 
            max_value=16, 
            value=8,
            help="Higher bits = Less quantization noise"
        )
        
    resampled_signal, t_resampled = sample_signal(data, fs, new_fs)
    
    quantized_signal, error = quantize_signal(resampled_signal, n_bits)
    
    st.markdown("### 📊 Visualization")
    
    zoom_range = st.slider("Zoom (Samples)", 0, len(data), (0, 1000))
    start_idx, end_idx = zoom_range
    
    ratio = new_fs / fs
    start_res = int(start_idx * ratio)
    end_res = int(end_idx * ratio)
    
    fig = go.Figure()
    
    t_orig = np.arange(start_idx, end_idx) / fs
    y_orig = data[start_idx:end_idx]
    
    max_plot_points = 5000
    if len(t_orig) > max_plot_points:
        step = int(np.ceil(len(t_orig) / max_plot_points))
        t_plot = t_orig[::step]
        y_plot = y_orig[::step]
        st.caption(f"⚠️ Visualizing 1 out of every {step} samples for performance.")
    else:
        t_plot = t_orig
        y_plot = y_orig

    fig.add_trace(go.Scatter(
        x=t_plot, 
        y=y_plot,
        mode='lines',
        name='Original Signal',
        line=dict(color='#3B82F6', width=2),
        opacity=0.7
    ))
    
    t_new = t_resampled[start_res:end_res]
    y_new = quantized_signal[start_res:end_res]
    
    if len(t_new) > max_plot_points:
        step_new = int(np.ceil(len(t_new) / max_plot_points))
        t_new_plot = t_new[::step_new]
        y_new_plot = y_new[::step_new]
    else:
        t_new_plot = t_new
        y_new_plot = y_new
    
    fig.add_trace(go.Scatter(
        x=t_new_plot, 
        y=y_new_plot,
        mode='lines+markers',
        name=f'Sampled ({new_fs}Hz) & Quantized ({n_bits}-bit)',
        line=dict(color='#EF4444', width=2, shape='hv'), # 'hv' for step-like
        marker=dict(size=4)
    ))
    
    fig.update_layout(
        title="Waveform Comparison",
        xaxis_title="Time (s)",
        yaxis_title="Amplitude",
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
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### 📉 Quantization Error", help="Quantization error is the difference between the analog signal and the closest available digital value at each sampling instant. It introduces noise, often called quantization noise.")
    
    fig_err = go.Figure()
    fig_err.add_trace(go.Scatter(
        x=t_new,
        y=error[start_res:end_res],
        mode='lines',
        name='Error',
        line=dict(color='#F59E0B')
    ))
    
    fig_err.update_layout(
        title="Quantization Noise (e[n])",
        xaxis_title="Time (s)",
        yaxis_title="Amplitude",
        template="plotly_dark",
        height=300
    )
    
    st.plotly_chart(fig_err, use_container_width=True)
    
    st.markdown("### 📝 Metrics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <div>
                <div style="font-size: 0.9rem; color: #9CA3AF;">Levels (L)</div>
                <div style="font-size: 1.5rem; font-weight: bold;">{2**n_bits}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        p_signal = np.mean(resampled_signal**2)
        p_noise = np.mean(error**2)
        
        snr = 10 * np.log10(p_signal / p_noise) if p_noise > 0 else float('inf')
        
        st.markdown(f"""
        <div class="metric-container">
            <div>
                <div style="font-size: 0.9rem; color: #9CA3AF;">SNR (dB)</div>
                <div style="font-size: 1.5rem; font-weight: bold;">{snr:.2f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

