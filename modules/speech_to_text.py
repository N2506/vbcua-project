import os
import whisper

def transcribe_audio(file_path, model_size="base"):
    """
    Loads an audio file and transcribes it into text using OpenAI Whisper.
    Returns a dictionary with the raw transcript text.
    """
    if not os.path.exists(file_path):
        return {"error": f"Audio file not found at {file_path}"}
        
    try:
        # Load the specified Whisper model size (base is lightweight and accurate)
        model = whisper.load_model(model_size)
        
        # Run transcription pipeline
        result = model.transcribe(file_path)
        
        return {
            "text": result.get("text", "").strip(),
            "language": result.get("language", "en")
        }
    except Exception as e:
        return {"error": f"Transcription engine error: {str(e)}"}

# Quick standalone test code block
if __name__ == "__main__":
    # Test with a placeholder file if executed directly
    print("Whisper Speech-to-Text Module Initialized.")
