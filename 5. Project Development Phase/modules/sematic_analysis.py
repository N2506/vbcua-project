import os
import streamlit as st
from sentence_transformers import SentenceTransformer, util

@st.cache_resource
def load_cached_semantic_model():
    """
    Loads and caches the Sentence-BERT embedding transformer model in system memory
    to drastically decrease computation latency under repeated runs.
    """
    return SentenceTransformer('all-MiniLM-L6-v2')

def evaluate_semantic_similarity(user_transcript, reference_concept_text):
    """
    Compares the user transcript against the reference text using the cached 
    Sentence-BERT embedding model and cosine similarity.
    """
    if not user_transcript or not reference_concept_text:
        return {"error": "Missing text inputs for calculation."}
        
    try:
        # Fetch the cached model instance instantly
        model = load_cached_semantic_model()
        
        embedding_user = model.encode(user_transcript, convert_to_tensor=True)
        embedding_ref = model.encode(reference_concept_text, convert_to_tensor=True)
        
        similarity_score = float(util.cos_sim(embedding_user, embedding_ref))
        
        return {
            "score": round(similarity_score * 100, 1)
        }
    except Exception as e:
        return {"error": f"Semantic model engine failure: {str(e)}"}
