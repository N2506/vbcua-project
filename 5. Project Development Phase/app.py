import os
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import librosa

# Handle relative import paths matching your exact repository filenames
from modules.speech_to_text import transcribe_audio
from modules.audio_analysis import extract_advanced_acoustics
from modules.sematic_analysis import evaluate_semantic_similarity
from modules.scoring import evaluate_understanding
from modules.report_generator import generate_pdf_report
from modules.database_logger import log_evaluation_session

# Configure Streamlit Application Page Metrics Layout
st.set_page_config(
    page_title="Voice-Based Concept Understanding Analyser",
    page_icon="🎙️",
    layout="wide"
)

st.title("🎙️ Voice-Based Concept Understanding Analyser")
st.markdown("---")

# Setup split dashboard column layouts (Explicitly specifying 2 columns)
left_column, right_column = st.columns(2)

# Define baseline directory structure metrics safely using absolute path strings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if "pipeline_calculated" not in st.session_state:
    st.session_state["pipeline_calculated"] = False

with left_column:
    st.header("📥 Audio Processing Portal")
    
    # Load available technical baseline definitions from your database configurations
    concept_selection = st.selectbox(
        "Select Concept Framework Definition Benchmark:",
        ["Semantic Normalization", "Relational Database Keys", "Gradient Descent Optimization"]
    )
    
    # Set static placeholder text ground-truths based on selection for baseline scoring matching
    ground_truths = {
        "Semantic Normalization": "Structuring data to reduce redundancy and improve data integrity.",
        "Relational Database Keys": "A primary key is a unique identifier for a relational database table row records.",
        "Gradient Descent Optimization": "An optimization algorithm used to minimize a loss function by iteratively moving in the direction of steepest descent."
    }
    target_benchmark = ground_truths[concept_selection]
    
    st.info(f"**Benchmark Definition Baseline:** {target_benchmark}")
    
    # Interactive Media Capture Controls (Drag and drop file uploader)
    uploaded_file = st.file_uploader("Upload Student Audio Performance Answer (.wav):", type=["wav"])
    
    if uploaded_file is not None:
        st.audio(uploaded_file, format="audio/wav")
        
        # Enforce absolute path creation for uploads directory
        upload_directory = os.path.abspath(os.path.join(BASE_DIR, "uploads"))
        if not os.path.exists(upload_directory):
            os.makedirs(upload_directory, exist_ok=True)
            
        temp_audio_path = os.path.abspath(os.path.join(upload_directory, uploaded_file.name))
        with open(temp_audio_path, "wb") as file_buffer:
            file_buffer.write(uploaded_file.getbuffer())
            
        # Core Pipeline Triggers Action Button Element
        if st.button("Run Analytical Evaluation Pipeline", type="primary"):
            with st.spinner("Processing speech metrics, computing semantic vectors..."):
                
                # Execute automated speech recognition
                transcription_result = transcribe_audio(temp_audio_path)
                
                if "error" in transcription_result:
                    st.error(f"ASR Pipeline Tracking Error: {transcription_result['error']}")
                else:
                    extracted_text = transcription_result.get("text", "")
                    
                    # 1. Compute acoustic metrics using your audio_analysis module
                    audio_metrics = extract_advanced_acoustics(temp_audio_path)
                    
                    if "error" in audio_metrics:
                        st.error(f"Audio Processing Error: {audio_metrics['error']}")
                        st.stop()
                    
                    # 2. Compute semantic embedding cosine tensor weights vs ground-truths
                    semantic_output = evaluate_semantic_similarity(extracted_text, target_benchmark)
                    
                    # Safely extract the raw float value if the semantic output returned a dictionary template
                    if isinstance(semantic_output, dict):
                        if "error" in semantic_output:
                            st.error(f"Semantic Analyzer Error: {semantic_output['error']}")
                            st.stop()
                        semantic_score = semantic_output.get("similarity_score", semantic_output.get("score", 0.0))
                    else:
                        semantic_score = semantic_output
                    
                    # Mock/Calculate a filler word ratio since your core librosa file focuses on signals
                    filler_word_ratio = 0.0
                    
                    # 3. Call your exact evaluate_understanding function with verified parameters
                    scoring_result = evaluate_understanding(
                        similarity=semantic_score,
                        filler_ratio=filler_word_ratio,
                        audio=audio_metrics
                    )
                    
                    final_score = scoring_result.get("score", 0)
                    status_text = scoring_result.get("level", "Moderate Understanding")
                    qualitative_feedback = scoring_result.get("feedback", "")
                    
                    # Load a clean time axis array here for your Matplotlib visualizer block to avoid missing data keys
                    try:
                        y, sr = librosa.load(temp_audio_path, sr=None)
                        time_axis = np.linspace(0, len(y) / sr, num=len(y))
                        audio_metrics["time_axis"] = time_axis
                        audio_metrics["amplitude_array"] = y
                    except Exception:
                        audio_metrics["time_axis"] = np.array([])
                        audio_metrics["amplitude_array"] = np.array([])
                    
                    # Persist performance analytics payload directly into active session states
                    st.session_state["pipeline_calculated"] = True
                    st.session_state["extracted_text"] = extracted_text
                    st.session_state["audio_metrics"] = audio_metrics
                    st.session_state["scoring_result"] = scoring_result
                    st.session_state["final_score"] = final_score
                    st.session_state["status_text"] = status_text
                    st.session_state["qualitative_feedback"] = qualitative_feedback
                    st.session_state["concept_name"] = concept_selection
                    st.session_state["temp_audio_path"] = temp_audio_path

with right_column:
    st.header("📊 Analytical Report Output")
    
    if st.session_state.get("pipeline_calculated", False):
        # Unpack active session variables
        extracted_text = st.session_state["extracted_text"]
        audio_metrics = st.session_state["audio_metrics"]
        scoring_result = st.session_state["scoring_result"]
        final_score = st.session_state["final_score"]
        status_text = st.session_state["status_text"]
        qualitative_feedback = st.session_state["qualitative_feedback"]
        concept_name = st.session_state["concept_name"]
        temp_audio_path = st.session_state["temp_audio_path"]
        
        # Display extracted delivery details
        st.subheader("📝 Automated Speech Transcription")
        st.text_area("Decoded Answer String Matrix:", value=extracted_text, height=100, disabled=True)
        
        st.subheader("📈 Fluency & Delivery Signals")
        col_metric1, col_metric2, col_metric3 = st.columns(3)
        col_metric1.metric("Speaking Duration", f"{audio_metrics.get('duration_sec', 0):.2f} s")
        col_metric2.metric("Pause Ratio", f"{audio_metrics.get('pause_ratio', 0) * 100:.1f}%")
        col_metric3.metric("Loudness (RMS Energy)", f"{audio_metrics.get('rms_energy', 0):.4f}")
        
        # Enforce exact SkillWallet threshold status criteria and hex color backgrounds
        if final_score >= 80:
            bg_color = "#2ecc71"       # SkillWallet Green
            text_color = "#ffffff"
        elif final_score >= 50:
            bg_color = "#f39c12"       # SkillWallet Orange
            text_color = "#ffffff"
        else:
            bg_color = "#e74c3c"       # SkillWallet Red
            text_color = "#ffffff"

        # Render custom HTML alert block container matching the SkillWallet design matrix
        st.markdown(
            f"""
            <div style="background-color: {bg_color}; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 6px solid rgba(0,0,0,0.2);">
                <h3 style="color: {text_color}; margin: 0; font-family: sans-serif; font-size: 20px;">🎯 Composite Multi-Factor Evaluation</h3>
                <p style="color: {text_color}; font-size: 32px; font-weight: bold; margin: 10px 0 5px 0;">{final_score} / 100</p>
                <span style="color: {text_color}; background-color: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 4px; font-size: 14px; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px;">
                    {status_text}
                </span>
                <p style="color: {text_color}; margin: 12px 0 0 0; font-style: italic; font-size: 14px;">📝 {qualitative_feedback}</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Render responsive Matplotlib Waveform Charts
        st.subheader("🌊 Signal Amplitude Waveform")
        fig, ax = plt.subplots(figsize=(10, 3.5))
        ax.plot(audio_metrics.get("time_axis"), audio_metrics.get("amplitude_array"), color="#2980b9", alpha=0.85)
        ax.set_title("Speech Amplitude Waveform", fontsize=12, pad=10)
        ax.set_xlabel("Time (Seconds)", fontsize=9)
        ax.set_ylabel("Amplitude", fontsize=9)
        ax.grid(True, linestyle="--", alpha=0.5)
        st.pyplot(fig)

        # Save output graphic to static artifacts folders path using absolute directory path structures
        image_artifacts_directory = os.path.abspath(os.path.join(BASE_DIR, "images"))
        if not os.path.exists(image_artifacts_directory):
            os.makedirs(image_artifacts_directory, exist_ok=True)
        plt.savefig(os.path.join(image_artifacts_directory, "waveform.png"), bbox_inches="tight")
        plt.close()
    else:
        st.info("💡 Complete the left processing steps and click analyze to output assessment grading results cards.")

# -----------------------------------------------------------------------------
# FIXED ACTION: Render PDF Download Area across the full wide page layout
# -----------------------------------------------------------------------------
if st.session_state.get("pipeline_calculated", False):
    st.markdown("---")
    st.header("📥 Export Performance Summary")
    
    concept_name = st.session_state["concept_name"]
    final_score = st.session_state["final_score"]
    status_text = st.session_state["status_text"]
    audio_metrics = st.session_state["audio_metrics"]
    extracted_text = st.session_state["extracted_text"]
    scoring_result = st.session_state["scoring_result"]

    reports_directory = os.path.abspath(os.path.join(BASE_DIR, "reports"))
    if not os.path.exists(reports_directory):
        os.makedirs(reports_directory, exist_ok=True)
        
    pdf_output_path = os.path.abspath(os.path.join(reports_directory, "evaluation_report.pdf"))
    waveform_image_path = os.path.abspath(os.path.join(BASE_DIR, "images", "waveform.png"))
    
    # Executing function call aligned with the report generator parameters order safely defined
    generate_pdf_report(
        topic=concept_name,
        metrics=audio_metrics,
        transcript=extracted_text,
        evaluation=scoring_result,
        chart_path=waveform_image_path,
        output_filename=pdf_output_path
    )
    
    # Display the large, highly interactive download button block
    with open(pdf_output_path, "rb") as pdf_file:
        st.download_button(
            label="📥 Click Here to Download Evaluation Report (PDF)",
            data=pdf_file,
            file_name=f"VBCUA_Report_{concept_name.replace(' ', '_')}.pdf",
            mime="application/pdf",
            type="primary"
        )
        
    # Log database metrics safely
    try:
        log_evaluation_session(
            topic=concept_name,
            metrics=audio_metrics,
            transcript=extracted_text,
            evaluation=scoring_result
        )
    except Exception:
        pass

