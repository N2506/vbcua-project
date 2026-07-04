import os
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import librosa

# Handle relative import paths correctly matching your exact repository filenames
from modules.speech_to_text import transcribe_audio
from modules.audio_analysis import extract_advanced_acoustics
from modules.sematic_analysis import evaluate_semantic_similarity
from modules.scoring import calculate_composite_score
from modules.report_generator import generate_pdf_report
from modules.database_logger import log_evaluation_to_db

# Configure Streamlit Application Page Metrics Layout
st.set_page_config(
    page_title="Voice-Based Concept Understanding Analyser",
    page_icon="🎙️",
    layout="wide"
)

st.title("🎙️ Voice-Based Concept Understanding Analyser")
st.markdown("---")

# Setup split dashboard column layouts
left_column, right_column = st.columns()

with left_column:
    st.header("📥 Audio Processing Portal")
    
    # 1. Load available technical baseline definitions from your database configurations
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
    
    # 2. Interactive Media Capture Controls (Drag and drop file uploader)
    uploaded_file = st.file_uploader("Upload Student Audio Performance Answer (.wav):", type=["wav"])
    
    if uploaded_file is not None:
        st.audio(uploaded_file, format="audio/wav")
        
        # Save temporary payload array assets safely inside the uploads structural file path
        upload_directory = "5. Project Development Phase/uploads"
        if not os.path.exists(upload_directory):
            os.makedirs(upload_directory)
            
        temp_audio_path = os.path.join(upload_directory, uploaded_file.name)
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
                    
                    # 1. Compute acoustic metrics using your exact function name and output dictionary structure
                    audio_metrics = extract_advanced_acoustics(temp_audio_path)
                    
                    if "error" in audio_metrics:
                        st.error(f"Audio Processing Error: {audio_metrics['error']}")
                        st.stop()
                    
                    # 2. Compute semantic embedding cosine tensor weights vs ground-truths
                    semantic_score = evaluate_semantic_similarity(extracted_text, target_benchmark)
                    
                    # Mock/Calculate a filler word ratio since your core librosa file focuses on signals
                    filler_word_ratio = 0.0
                    
                    # 3. Run compound calculations engine out of 100 points
                    final_score = calculate_composite_score(
                        semantic_score=semantic_score,
                        filler_ratio=filler_word_ratio,
                        pause_ratio=audio_metrics.get("pause_ratio", 0),
                        rms_energy=audio_metrics.get("rms_energy", 0)
                    )
                    
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
                    st.session_state["semantic_score"] = semantic_score
                    st.session_state["final_score"] = final_score
                    st.session_state["concept_name"] = concept_selection
                    st.session_state["temp_audio_path"] = temp_audio_path

with right_column:
    st.header("📊 Analytical Report Output")
    
    if st.session_state.get("pipeline_calculated", False):
        # Unpack active session variables
        extracted_text = st.session_state["extracted_text"]
        audio_metrics = st.session_state["audio_metrics"]
        semantic_score = st.session_state["semantic_score"]
        final_score = st.session_state["final_score"]
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
            status_text = "Strong Understanding"
            bg_color = "#2ecc71"       # SkillWallet Green
            text_color = "#ffffff"
        elif final_score >= 50:
            status_text = "Moderate Understanding"
            bg_color = "#f39c12"       # SkillWallet Orange
            text_color = "#ffffff"
        else:
            status_text = "Poor Understanding"
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
        
        # Save output graphic to static artifacts folders path for PDF packaging usage
        image_artifacts_directory = "5. Project Development Phase/images"
        if not os.path.exists(image_artifacts_directory):
            os.makedirs(image_artifacts_directory)
        plt.savefig(os.path.join(image_artifacts_directory, "waveform.png"), bbox_inches="tight")
        plt.close()
        
        # 4. Generate dynamic downloadable ReportLab PDF performance data summaries
        st.subheader("📥 Export Performance Summary")
        reports_directory = "5. Project Development Phase/reports"
        if not os.path.exists(reports_directory):
            os.makedirs(reports_directory)
            
        pdf_output_path = os.path.join(reports_directory, "evaluation_report.pdf")
        generate_pdf_report(pdf_output_path, concept_name, final_score, status_text, audio_metrics, extracted_text)
        
        with open(pdf_output_path, "rb") as pdf_file:
            st.download_button(
                label="📥 Download Evaluation Report (PDF)",
                data=pdf_file,
