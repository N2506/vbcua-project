import os
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

def analyze_audio_fluency(file_path):
    """
    Loads an audio file and extracts fundamental fluency metrics:
    duration, mean RMS energy (loudness), and pause ratio.
    """
    if not os.path.exists(file_path):
        return {"error": f"Audio file not found at {file_path}"}
        
    # Load audio signal with native sample rate
    y, sr = librosa.load(file_path, sr=None)
    duration = librosa.get_duration(y=y, sr=sr)
    
    # Calculate Root-Mean-Square (RMS) Energy for speech confidence tracking
    rms = librosa.feature.rms(y=y)
    avg_rms_energy = float(np.mean(rms))
    
    # Basic silence/pause ratio calculation based on an energy threshold
    silence_threshold = 0.015
    silent_frames = np.sum(rms < silence_threshold)
    total_frames = rms.size
    pause_ratio = float(silent_frames / total_frames) if total_frames > 0 else 0.0
    
    return {
        "duration_sec": round(duration, 2),
        "rms_energy": round(avg_rms_energy, 4),
        "pause_ratio": round(pause_ratio, 2)
    }

def generate_waveform_plot(file_path, save_directory="images"):
    """
    Generates a clean waveform display and saves it as a PNG image 
    to be reused inside the Streamlit UI and PDF reports.
    """
    if not os.path.exists(file_path):
        return None
        
    y, sr = librosa.load(file_path, sr=None)
    
    # Render Matplotlib figure canvas
    fig, ax = plt.subplots(figsize=(10, 3))
    librosa.display.waveshow(y, sr=sr, ax=ax, color='#1f77b4', alpha=0.7)
    
    ax.set_title("Speech Amplitude Waveform")
    ax.set_xlabel("Time (Seconds)")
    ax.set_ylabel("Amplitude")
    plt.tight_layout()
    
    # Ensure save directory paths exist
    os.makedirs(save_directory, exist_ok=True)
    output_image_path = os.path.join(save_directory, "current_waveform.png")
    plt.savefig(output_image_path, dpi=150)
    plt.close()
    
    return output_image_path
