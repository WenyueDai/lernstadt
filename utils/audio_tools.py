# utils/audio_tools.py
import base64
import streamlit as st

def autoplay_audio(file_path: str):
    """
    Embed an audio file that auto-plays in the Streamlit app using HTML injection.
    """
    with open(file_path, "rb") as f:
        audio_bytes = f.read()
        b64_audio = base64.b64encode(audio_bytes).decode()

    audio_html = f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)
