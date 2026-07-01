import os
from sentence_transformers import SentenceTransformer, util

def evaluate_semantic_similarity(user_transcript, reference_concept_text):
    """
    Compares the user's transcription against the ground truth reference concept 
    using Sentence-BERT semantic embeddings and cosine similarity.
    """
    if not user_transcript or not reference_concept_text:
        return {"error": "Missing text inputs for calculation."}
        
    try:
        # Load a lightweight, highly accurate embedding model
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Compute sentence embeddings for both blocks of text
        embedding_user = model.encode(user_transcript, convert_to_tensor=True)
        embedding_ref = model.encode(reference_concept_text, convert_to_tensor=True)
        
        # Calculate cosine similarity score (returns a decimal between 0 and 1)
        similarity_score = float(util.cos_sim(embedding_user, embedding_ref)[0][0])
        
        # Determine qualitative understanding level threshold groups
        if similarity_score >= 0.80:
            understanding_level = "Strong Understanding"
            feedback = "Excellent coverage of the core definitions and concepts!"
        elif similarity_score >= 0.55:
            understanding_level = "Moderate Understanding"
            feedback = "Good baseline. Try to include more specific structural details or terminology."
        else:
            understanding_level = "Poor Understanding"
            feedback = "The explanation deviates significantly from the expected technical parameters."
            
        return {
            "score": round(similarity_score * 100, 1), # convert to percentage
            "level": understanding_level,
            "feedback": feedback
        }
    except Exception as e:
        return {"error": f"Semantic model engine failure: {str(e)}"}
