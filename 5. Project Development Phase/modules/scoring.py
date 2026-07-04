def evaluate_understanding(similarity, filler_ratio, audio):
    """
    Combines semantic alignment, verbal filler pacing, silence pause metrics, 
    and energy density loudness to build a standardized composite score out of 100.
    """
    score = 0
    
    # 1. Content Semantic Similarity Weight (Max 50 points)
    # Convert incoming score percentage decimal back to raw float range [0.0 - 1.0] if necessary
    sim_val = similarity / 100.0 if similarity > 1.0 else similarity
    if sim_val > 0.7:
        score += 50
    elif sim_val > 0.4:
        score += 30
    else:
        score += 10
        
    # 2. Verbal Hesitation Filler Ratio Weight (Max 20 points)
    if filler_ratio < 0.05:
        score += 20
    else:
        score += 10
        
    # 3. Acoustic Pause Ratio Boundary Weight (Max 15 points)
    if audio.get("pause_ratio", 0.0) < 0.25:
        score += 15
    else:
        score += 5
        
    # 4. Energy Loudness Confident Variance Weight (Max 15 points)
    if audio.get("rms_energy", 0.0) > 0.01:
        score += 15
    else:
        score += 5
        
    # Standardized qualitative classification groupings
    if score >= 80:
        return {
            "score": score,
            "level": "Strong Understanding",
            "feedback": "Excellent conceptual delivery! Clear acoustics, structured vocabulary, and close semantic baseline alignment."
        }
    elif score >= 50:
        return {
            "score": score,
            "level": "Moderate Understanding",
            "feedback": "Acceptable explanation base. Try incorporating richer field terminologies and minimizing conversational pause voids."
        }
    else:
        return {
            "score": score,
            "level": "Poor Understanding",
            "feedback": "The spoken content requires major structural expansions regarding technical key concepts."
        }
