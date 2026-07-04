def analyze_speech_fluency(transcript_text, pause_ratio):
    """
    Parses textual parameters for filler words and structural patterns 
    to output specific qualitative improvement insights.
    """
    if not transcript_text:
        return {"count": 0, "ratio": 0.0, "feedback": "No active speech patterns found."}
        
    fillers = ["um", "uh", "like", "basically", "actually", "so"]
    words = [w.strip(".,!?\"()").lower() for w in transcript_text.split()]
    total_words = len(words)
    
    filler_count = sum(1 for w in words if w in fillers)
    filler_ratio = float(filler_count / total_words) if total_words > 0 else 0.0
    
    # Structural Fluency Rules
    if filler_ratio > 0.12 or pause_ratio > 0.40:
        feedback = "High level of hesitation detected. Practice minimizing filler phrases and pacing transitions."
    elif filler_ratio > 0.05:
        feedback = "Moderate fluency. Good flow, but conscious pausing will help eliminate remaining filler terms."
    else:
        feedback = "Excellent verbal delivery structure! Clear pacing with minimal hesitation marks."
        
    return {
        "filler_count": filler_count,
        "total_words": total_words,
        "filler_ratio": round(filler_ratio, 3),
        "delivery_feedback": feedback
    }
