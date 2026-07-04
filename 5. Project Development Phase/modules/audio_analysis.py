import os
import numpy as np
import librosa

def extract_advanced_acoustics(file_path):
    """
    Computes professional speech metrics: speech rate, signal variance, 
    and voice loudness boundaries to gauge speaking confidence.
    """
    if not os.path.exists(file_path):
        return {"error": f"Audio targets missing at {file_path}"}
        
    try:
        y, sr = librosa.load(file_path, sr=None)
        duration = librosa.get_duration(y=y, sr=sr)
        
        # Calculate Root-Mean-Square Energy variance across frames
        rms = librosa.feature.rms(y=y)
        mean_energy = float(np.mean(rms))
        energy_variance = float(np.var(rms))
        
        # Detect active speaking frames vs silence boundaries
        silence_threshold = 0.015
        active_frames = np.sum(rms >= silence_threshold)
        total_frames = rms.size
        
        speech_ratio = float(active_frames / total_frames) if total_frames > 0 else 0.0
        pause_ratio = 1.0 - speech_ratio
        
        return {
            "duration_sec": round(duration, 2),
            "rms_energy": round(mean_energy, 4),
            "energy_variance": round(energy_variance, 5),
            "pause_ratio": round(pause_ratio, 2)
        }
    except Exception as e:
        return {"error": f"Acoustic processing fault: {str(e)}"}
