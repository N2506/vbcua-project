import os
from transformers import pipeline
import streamlit as st

@st.cache_resource
def load_cached_transcription_model():
    """
    Loads and caches the Whisper automatic speech recognition pipeline in system memory
    to prevent latency and redundant reloading overhead.
    """
    return pipeline("automatic-speech-recognition", model="openai/whisper-tiny.en")

def transcribe_audio(file_path):
    """
    Transcribes an audio file into text using the cached speech recognition pipeline.
    """
    if not os.path.exists(file_path):
        return {"error": f"Audio file not found at {file_path}"}
        
    try:
        # Fetch the cached instance instantly from memory
        asr_pipe = load_cached_transcription_model()
        result = asr_pipe(file_path)
        
        return {
            "text": result.get("text", "").strip(),
            "language": "en"
        }
    except Exception as e:
        return {"error": f"Transcription pipeline failure: {str(e)}"}
