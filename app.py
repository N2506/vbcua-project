import streamlit as str
import os
import sys

# Maintain clean local path architecture
current_dir = os.path.dirname(os.path.abspath(__file__))
modules_dir = os.path.join(current_dir, "modules")
if modules_dir not in sys.path:
    sys.path.append(modules_dir)

# Ground-truth reference dictionary for conceptual comparisons
REFERENCE_CONCEPTS = {
    "Database Normalization": "Database normalization is the process of structuring a relational database in accordance with a series of so-called normal forms in order to reduce data redundancy and improve data integrity.",
    "OSI Model Layers": "The Open Systems Interconnection model is a conceptual model that characterizes and standardizes the communication functions of a telecommunication or computing system without regard to its underlying internal structure and technology.",
    "Machine Learning Basics": "Machine learning is a field of study in artificial intelligence concerned with the development and study of statistical algorithms that can learn from data and generalize to unseen data without explicit instructions.",
    "Cloud Computing": "Cloud computing is the on-demand availability of computer system resources, especially data storage and computing power, without direct active management by the user."
}

# Import our custom modules safely
try:
    import waveform
    import speech_to_text
    import sematic_analysis
except ImportError:
    waveform = None
    speech_to_text = None
    sematic_analysis = None

# Configure dashboard
str.set_page_config(
    page_title="VBCUA - Concept Analyser",
    page_icon="🎙️",
    layout="wide"
)

str.title("🎙️ Voice-Based Concept Understanding Analyser")
str.markdown("""
Evaluate how effectively you understand and explain conceptual topics through spoken communication. 
This tool measures conceptual accuracy, fluency, delivery metrics, and generates a structured performance report.
""")
str.divider()

left_column, right_column = str.columns(2)

with left_column:
    str.header("📥 Audio Processing Portal")
    
    target_topic = str.selectbox(
        "Choose the concept topic you are explaining:",
        list(REFERENCE_CONCEPTS.keys())
    )
    
    uploaded_file = str.file_uploader(
        "Upload your spoken explanation audio file (.mp3, .wav, .m4a):",
        type=["mp3", "wav", "m4a"]
    )
    
    if uploaded_file is not None:
        os.makedirs("uploads", exist_ok=True)
        saved_file_path = os.path.join("uploads", uploaded_file.name)
        
        with open(saved_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        str.success(f"Successfully uploaded: {uploaded_file.name}")
        str.audio(saved_file_path, format="audio/wav")
        
        if str.button("🚀 Analyze Concept Explanation", use_container_width=True):
            with str.spinner("🤖 Processing voice acoustics and running AI evaluation pipelines..."):
                try:
                    # 1. Acoustics & Fluency
                    if waveform:
                        str.session_state["metrics"] = waveform.analyze_audio_fluency(saved_file_path)
                        str.session_state["chart_path"] = waveform.generate_waveform_plot(saved_file_path)
                    
                    # 2. Whisper Speech to Text
                    user_text = ""
                    if speech_to_text:
                        stt_result = speech_to_text.transcribe_audio(saved_file_path)
                        user_text = stt_result.get("text", "")
                        str.session_state["transcript"] = user_text
                    
                    # 3. Sentence-BERT Semantic Analysis
                    if sematic_analysis and user_text:
                        ref_text = REFERENCE_CONCEPTS[target_topic]
                        str.session_state["evaluation"] = sematic_analysis.evaluate_semantic_similarity(user_text, ref_text)
                    
                    str.session_state["analysis_triggered"] = True
                    str.rerun()
                except Exception as e:
                    str.error(f"Analysis failed: {str(e)}")

with right_column:
    str.header("📊 Analytical Report Output")
    
    if "analysis_triggered" not in str.session_state:
        str.info("Upload an audio file on the left panel and click 'Analyze' to review metrics here.")
    else:
        metrics = str.session_state.get("metrics", {})
        chart_path = str.session_state.get("chart_path", None)
        transcript = str.session_state.get("transcript", "")
        evaluation = str.session_state.get("evaluation", {})
        
        if "error" in metrics:
            str.error(metrics["error"])
        else:
            # Display Extracted Fluency Metrics
            str.subheader("🔊 Fluency & Delivery Signals")
            metric_col1, metric_col2, metric_col3 = str.columns(3)
            metric_col1.metric("Duration", f"{metrics.get('duration_sec')} sec")
            metric_col2.metric("Pause Ratio", f"{int(metrics.get('pause_ratio', 0) * 100)}%")
            metric_col3.metric("RMS Energy (Loudness)", f"{metrics.get('rms_energy')}")
            
            # Render waveform chart
            if chart_path and os.path.exists(chart_path):
                str.subheader("📉 Signal Amplitude Waveform")
                str.image(chart_path, use_container_width=True)
                
            str.divider()
            
            # Display live transcript text output
            str.subheader("📝 Transcription Result")
            if transcript:
                str.text_area("Whisper Model Speech-to-Text:", value=transcript, height=100, disabled=True)
            else:
                str.warning("No speech patterns detected in audio file.")
                
            str.divider()
            
            # Display Semantic Scoring Outputs
            str.subheader("🎯 Conceptual Semantic Evaluation")
            if "error" in evaluation:
                str.error(evaluation["error"])
            elif evaluation:
                score_val = evaluation.get("score", 0.0)
                level_val = evaluation.get("level", "Unknown")
                feedback_val = evaluation.get("feedback", "")
                
                eval_col1, eval_col2 = str.columns(2)
                eval_col1.metric("Semantic Match Accuracy", f"{score_val}%")
                
                if "Strong" in level_val:
                    eval_col2.success(level_val)
                elif "Moderate" in level_val:
                    eval_col2.warning(level_val)
                else:
                    eval_col2.error(level_val)
                    
                str.info(f"💡 **AI Feedback:** {feedback_val}")