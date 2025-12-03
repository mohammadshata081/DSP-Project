import streamlit as st
import os
import sys



from app.utils import load_css, render_header, save_to_history, get_recent_files
from app.tabs import sampling_tab, fft_tab, denoise_tab
import soundfile as sf
import numpy as np

st.set_page_config(
    page_title="DSP Processor App",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()

with st.sidebar:
    st.title("🎛️ DSP Tools")
    
    page = st.radio(
        "Navigate",
        ["Home", "Sampling & Quantization", "FFT Analysis", "Denoising"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### 📂 Recent Files")
    
    recent_files = get_recent_files()
    if not recent_files:
        st.caption("No recent files")
    else:
        for file_path in recent_files:
            filename = os.path.basename(file_path)
            if st.button(f"📄 {filename}", key=file_path, use_container_width=True):
                if os.path.exists(file_path):
                    data, fs = sf.read(file_path)
                    if len(data.shape) > 1:
                        data = data.mean(axis=1)
                    st.session_state['audio_data'] = data
                    st.session_state['fs'] = fs
                    st.session_state['current_file'] = filename
                    st.success(f"Loaded: {filename}")
                else:
                    st.error("File not found.")
    
    st.markdown("---")
    st.markdown("Created for DSP Course")

if page == "Home":
    render_header("DSP Processor App", "")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 📤 Upload Audio File")
        
        uploaded_file = st.file_uploader("Upload Audio", type=['wav'], label_visibility="collapsed")
        
        if uploaded_file:
            save_to_history(uploaded_file)
            
            st.session_state['uploaded_file'] = uploaded_file
            st.success(f"Loaded: {uploaded_file.name}")
            
            data, fs = sf.read(uploaded_file)
            if len(data.shape) > 1:
                data = data.mean(axis=1)
                
            st.session_state['audio_data'] = data
            st.session_state['fs'] = fs
            st.session_state['current_file'] = uploaded_file.name
            
            st.audio(uploaded_file)
            
    if 'current_file' in st.session_state:
        st.info(f"Currently analyzing: **{st.session_state['current_file']}**")

elif page == "Sampling & Quantization":
    sampling_tab.render()

elif page == "FFT Analysis":
    fft_tab.render()

elif page == "Denoising":
    denoise_tab.render()
