import streamlit as st
import base64

def load_css():
    """
    Injects custom CSS for a premium look.
    """
    st.markdown("""
        <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

        /* Global Styles */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        
        /* Headers */
        h1, h2, h3 {
            font-weight: 700;
            letter-spacing: -0.5px;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(90deg, #3B82F6 0%, #2563EB 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.2s ease;
            box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.5);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 8px -1px rgba(59, 130, 246, 0.6);
        }

        /* Uploader Customization */
        [data-testid="stFileUploader"] section {
            pointer-events: none;
        }
        [data-testid="stFileUploader"] button {
            pointer-events: auto;
            cursor: pointer;
        }
        [data-testid="stFileUploader"] section > div > div > span {
            display: none;
        }
        [data-testid="stFileUploader"] section > div > div::before {
            content: "Upload The .WAV File";
            display: block;
            font-weight: bold;
            margin-bottom: 5px;
        }
        [data-testid="stFileUploader"] small {
            display: block !important;
        }
        
        </style>
    """, unsafe_allow_html=True)

def render_header(title, subtitle=""):
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="font-size: 3rem; margin-bottom: 0.5rem; background: linear-gradient(to right, #60A5FA, #A78BFA); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{title}</h1>
            <p style="font-size: 1.2rem; color: #9CA3AF;">{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)

def get_audio_download_link(audio_data, fs, filename="processed_audio.wav"):
    import soundfile as sf
    import io
    
    buffer = io.BytesIO()
    sf.write(buffer, audio_data, fs, format='WAV')
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode()
    
    href = f'<a href="data:audio/wav;base64,{b64}" download="{filename}" style="text-decoration: none;"><button style="background: #10B981; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold;">Download Processed Audio</button></a>'
    return href

import json
import os

RECENT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output', 'recent')
HISTORY_FILE = os.path.join(RECENT_DIR, 'history.json')

def save_to_history(uploaded_file):
    """
    Saves the uploaded file to the recent directory and updates history.json.
    """
    if not os.path.exists(RECENT_DIR):
        os.makedirs(RECENT_DIR)
        
    # Save file to disk
    file_path = os.path.join(RECENT_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    # Update history
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            try:
                history = json.load(f)
            except:
                history = []
    
    # Remove if already exists to move to top
    if file_path in history:
        history.remove(file_path)
        
    # Add to top
    history.insert(0, file_path)
    
    # Keep max 5
    history = history[:5]
    
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)
        
    return file_path

def get_recent_files():
    """
    Returns a list of recent file paths.
    """
    if not os.path.exists(HISTORY_FILE):
        return []
        
    with open(HISTORY_FILE, 'r') as f:
        try:
            return json.load(f)
        except:
            return []
