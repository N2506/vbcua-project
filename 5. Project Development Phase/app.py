import streamlit as st
import os
import sys

# Track clean modular directories
current_dir = os.path.dirname(os.path.abspath(__file__))
modules_dir = os.path.join(current_dir, "modules")
if modules_dir not in sys.path:
    sys.path.append(modules_dir)

# Ground-truth concept references
REFERENCE_CONCEPTS = {
    "Database Normalization": "Database normalization is the process of structuring a relational database in accordance with a series of so-called normal forms in order to reduce data redundancy and improve data integrity.",
    "OSI Model Layers": "The Open Systems Interconnection model is a conceptual model that characterizes and standardizes the communication functions of a telecommunication or computing system without regard to its underlying internal structure and technology.",
    "Machine Learning Basics": "Machine learning is a field of study in artificial intelligence concerned with the development and study of statistical algorithms that can learn from data and generalize to unseen data without explicit instructions.",
    "Cloud Computing": "Cloud computing is the on-demand availability of computer system resources, especially data storage and computing power, without direct active management by the user."
}

try:
    import audio_analysis
    import speech_to_text
    import sematic_analysis
    import feedback
    import scoring
    import report_generator
    import waveform
    import database_logger
except ImportError as e:
    st.error(f"Module Loading Error: {str(e)}")

st.set_page_config(page_title="VBCUA - Analytical Suite", page_icon="🎙️", layout="wide")

st.title("🎙️ Voice-Based Concept Understanding Analyser")
st.markdown("---")

left_panel, right_panel = st.columns(2)

with left_panel:
    st.header("📥 Audio Processing Portal")
    topic = st.selectbox("Choose the target concept topic:", list(REFERENCE_CONCEPTS.keys()))
    uploaded_audio = st.file_uploader("Upload audio tracks (.mp3, .wav, .m4a):", type=["mp3", "wav", "m4a"])
    
    if uploaded_audio is not None:
        os.makedirs("uploads", exist_ok=True)
        file_path = os.path.join("uploads", uploaded_audio.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_audio.getbuffer())
            
        st.success("Audio track uploaded successfully.")
        st.audio(file_path)
        
        if st.button("🚀 Analyze Concept Explanation", use_container_width=True):
            with st.spinner("🤖 Running composite AI scoring engines..."):
                try:
                    st.session_state["topic"] = topic
                    
                    # 1. Advanced Acoustic Attributes Extraction
                    acoustics = audio_analysis.extract_advanced_acoustics(file_path)
                    st.session_state["acoustics"] = acoustics
                    st.session_state["chart"] = waveform.generate_waveform_plot(file_path)
                    
                    # 2. Raw Speech to Text Pipeline
                    stt = speech_to_text.transcribe_audio(file_path)
                    transcript = stt.get("text", "Sample speech transcript.")
                    st.session_state["transcript"] = transcript
                    
                    # 3. Pacing & Hesitation Tracking 
                    fluency = feedback.analyze_speech_fluency(transcript, acoustics.get("pause_ratio", 0.0))
                    st.session_state["fluency"] = fluency
                    
                    # 4. Compute Semantic Overlap Percentage
                    semantic_result = sematic_analysis.evaluate_semantic_similarity(transcript, REFERENCE_CONCEPTS[topic])
                    raw_sim_score = semantic_result.get("score", 0.0)
                    
                    # 5. EXECUTE THE MULTI-FACTOR COMPOSITE ENGINE REQUIREMENT
                    composite_evaluation = scoring.evaluate_understanding(
                        similarity=raw_sim_score,
                        filler_ratio=fluency.get("filler_ratio", 0.0),
                        audio=acoustics
                    )
                    st.session_state["semantic"] = composite_evaluation
                    
                    # 6. Push Live Transaction data directly to local MySQL workbench tables
                    if database_logger:
                        database_logger.log_evaluation_session(
                            topic=topic,
                            metrics=acoustics,
                            transcript=transcript,
                            evaluation=composite_evaluation
                        )
                    
                    st.session_state["run_complete"] = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Analysis system exception: {str(e)}")

with right_panel:
    st.header("📊 Analytical Report Output")
    if "run_complete" not in st.session_state:
        st.info("Upload an audio file on the left panel and click 'Analyze' to review metrics here.")
    else:
        acoustics = st.session_state["acoustics"]
        fluency = st.session_state["fluency"]
        semantic = st.session_state["semantic"]
        transcript = st.session_state["transcript"]
        
        # Display Fluency telemetry metrics
        st.subheader("🔊 Fluency & Delivery Signals")
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("Duration", f"{acoustics.get('duration_sec')} s")
        m_col2.metric("Pause Ratio", f"{int(acoustics.get('pause_ratio', 0) * 100)}%")
        m_col3.metric("Loudness (RMS)", f"{acoustics.get('rms_energy')}")
        
        # Display text field outputs
        st.subheader("📝 Automated Speech Transcription")
        st.text_area("Whisper Output Text:", value=transcript, height=90, disabled=True)
        
        # Display Hesitation Metrics
        st.subheader("📊 Verbal Delivery Metrics")
        f_col1, f_col2 = st.columns(2)
        f_col1.metric("Total Words Spoken", fluency.get("total_words"))
        f_col2.metric("Filler Word Count", fluency.get("filler_count"))
        st.warning(f"💡 Delivery Feedback: {fluency.get('delivery_feedback')}")
        
        # Display the composite normalized scorecard output
        st.subheader("🎯 Composite Multi-Factor Evaluation")
        s_col1, s_col2 = st.columns(2)
        s_col1.metric("Weighted Overall Score", f"{semantic.get('score')} / 100")
        
        # Apply custom layout labels dynamically matching classifications
        level_str = semantic.get("level")
        if "Strong" in level_str:
            st.success(level_str)
        elif "Moderate" in level_str:
            st.warning(level_str)
        else:
            st.error(level_str)
            
        st.info(f"💡 AI Content Insight Assessment: {semantic.get('feedback')}")
        
        # Embed graphs and printable items
        chart_path = st.session_state.get("chart", None)
        if chart_path and os.path.exists(chart_path):
            st.divider()
            st.subheader("📉 Signal Amplitude Waveform")
            st.image(chart_path, use_container_width=True)
            
        if report_generator:
            st.divider()
            st.subheader("📥 Export Performance Summary")
            try:
                pdf_file_path = report_generator.generate_pdf_report(
                    topic=st.session_state.get("topic", "Evaluation"),
                    metrics=acoustics,
                    transcript=transcript,
                    evaluation=semantic,
                    chart_path=chart_path
                )
                if os.path.exists(pdf_file_path):
                    with open(pdf_file_path, "rb") as pdf_file:
                        st.download_button(
                            label="Download Evaluation Report (PDF)",
                            data=pdf_file,
                            file_name="VBCUA_Evaluation_Report.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
            except Exception as pdf_error:
                st.error(f"Could not build PDF interface: {str(pdf_error)}")
