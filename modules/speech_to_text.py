import os
from transformers import pipeline

def transcribe_audio(file_path):
    """
    Transcribes an audio file into text using a stable Hugging Face pipeline.
    """
    if not os.path.exists(file_path):
        return {"error": f"Audio file not found at {file_path}"}
        
    try:
        # Initialize an automatic speech recognition pipeline using a fast, robust model checkpoint
        asr_pipe = pipeline("automatic-speech-recognition", model="openai/whisper-tiny.en")
        
        # Process the transcription block
        result = asr_pipe(file_path)
        
        return {
            "text": result.get("text", "").strip(),
            "language": "en"
        }
    except Exception as e:
        return {"error": f"Transcription pipeline failure: {str(e)}"}
