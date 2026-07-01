import streamlit as st
import os
import sys

# Ensure proper local folder navigation parameters
current_dir = os.path.dirname(os.path.abspath(__file__))
modules_dir = os.path.join(current_dir, "modules")
if modules_dir not in sys.path:
    sys.path.append(modules_dir)

# Ground-truth concept benchmarks
REFERENCE_CONCEPTS = {
    "Database Normalization": "Database normalization is the process of structuring a relational database in accordance with a series of so-called normal forms in order to reduce data redundancy and improve data integrity.",
    "OSI Model Layers": "The Open Systems Interconnection model is a conceptual model that characterizes and standardizes the communication functions of a telecommunication or computing system without regard to its underlying internal structure and technology.",
    "Machine Learning Basics": "Machine learning is a field of study in artificial intelligence concerned with the development and study of statistical algorithms that can learn from data and generalize to unseen data without explicit instructions.",
    "Cloud Computing": "Cloud computing is the on-demand availability of computer system resources, especially data storage and computing power, without direct active management by the user."
}

# Protected application imports
try:
    import audio_analysis
    import speech_to_text
    import sematic_analysis
    import feedback
    import report_generator
    import waveform
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
            with st.spinner("🤖 Running AI evaluation pipelines..."):
                st.session_state["topic"] = topic
                
                # 1. Extract Advanced Acoustics
                acoustics = audio_analysis.extract_advanced_acoustics(file_path)
                st.session_state["acoustics"] = acoustics
                st.session_state["chart"] = waveform.generate_waveform_plot(file_path)
                
                # 2. Textual Transcription Pipeline
                stt = speech_to_text.transcribe_audio(file_path)
                transcript = stt.get("text", "Sample speech transcript.")
                st.session_state["transcript"] = transcript
                
                # 3. Fluency Feedback Checking
                st.session_state["fluency"] = feedback.analyze_speech_fluency(transcript, acoustics.get("pause_ratio", 0))
                
                # 4. Deep Learning Similarity Metrics
                st.session_state["semantic"] = sematic_analysis.evaluate_semantic_similarity(transcript, REFERENCE_CONCEPTS[topic])
                
                st.session_state["run_complete"] = True
                st.rerun()

with right_panel:
    st.header("📊 Analytical Report Output")
    if "run_complete" not in st.session_state:
        st.info("Upload an audio file on the left panel and click 'Analyze' to review metrics here.")
    else:
        acoustics = st.session_state["acoustics"]
        fluency = st.session_state["fluency"]
        semantic = st.session_state["semantic"]
        transcript = st.session_state["transcript"]
        
        # Display Fluency Dashboard
        st.subheader("🔊 Fluency & Delivery Signals")
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("Duration", f"{acoustics.get('duration_sec')} s")
        m_col2.metric("Pause Ratio", f"{int(acoustics.get('pause_ratio', 0) * 100)}%")
        m_col3.metric("Loudness (RMS)", f"{acoustics.get('rms_energy')}")
        
        # Display Text Transcription Output
        st.subheader("📝 Automated Speech Transcription")
        st.text_area("Whisper Output Text:", value=transcript, height=90, disabled=True)
        
        # Display Hesitation Breakdown Metrics
        st.subheader("📊 Verbal Delivery Metrics")
        f_col1, f_col2 = st.columns(2)
        f_col1.metric("Total Words Spoken", fluency.get("total_words"))
        f_col2.metric("Filler Word Count", fluency.get("filler_count"))
        st.warning(f"💡 Delivery Feedback: {fluency.get('delivery_feedback')}")
        
        # Display AI Semantic Scores
        st.subheader("🎯 Conceptual Semantic Evaluation")
        s_col1, s_col2 = st.columns(2)
        s_col1.metric("Semantic Accuracy", f"{semantic.get('score')}%")
        s_col2.info(f"Level: {semantic.get('level')}")
        st.success(f"💡 AI Content Insight: {semantic.get('feedback')}")
        
        # 1. Re-integrate Waveform Visualization Chart
        chart_path = st.session_state.get("chart", None)
        if chart_path and os.path.exists(chart_path):
            st.divider()
            st.subheader("📉 Signal Amplitude Waveform")
            st.image(chart_path, use_container_width=True)
            
        # 2. Re-integrate PDF Report Downloader Link
        if report_generator:
            st.divider()
            st.subheader("📥 Export Performance Summary")
            try:
                # Mock evaluation dictionary matching the expected structure of report_generator
                eval_dict = {
                    "score": semantic.get("score"),
                    "level": semantic.get("level"),
                    "feedback": semantic.get("feedback")
                }
                
                pdf_file_path = report_generator.generate_pdf_report(
                    topic=topic,
                    metrics=acoustics,
                    transcript=transcript,
                    evaluation=eval_dict,
                    chart_path=chart_path
                )
                
                if os.path.exists(pdf_file_path):
                    with open(pdf_file_path, "rb") as pdf_file:
                        st.download_button(
                            label="Download Evaluation Report (PDF)",
                            data=pdf_file,
                            file_name=f"VBCUA_{topic.replace(' ', '_')}_Report.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
            except Exception as pdf_error:
                st.error(f"Could not build PDF interface: {str(pdf_error)}")
