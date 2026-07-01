import streamlit as st
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
modules_dir = os.path.join(current_dir, "modules")
if modules_dir not in sys.path:
    sys.path.append(modules_dir)

REFERENCE_CONCEPTS = {
    "Database Normalization": "Database normalization is the process of structuring a relational database in accordance with a series of so-called normal forms in order to reduce data redundancy and improve data integrity.",
    "OSI Model Layers": "The Open Systems Interconnection model is a conceptual model that characterizes and standardizes the communication functions of a telecommunication or computing system without regard to its underlying internal structure and technology.",
    "Machine Learning Basics": "Machine learning is a field of study in artificial intelligence concerned with the development and study of statistical algorithms that can learn from data and generalize to unseen data without explicit instructions.",
    "Cloud Computing": "Cloud computing is the on-demand availability of computer system resources, especially data storage and computing power, without direct active management by the user."
}

try:
    import waveform
    import speech_to_text
    import sematic_analysis
    import report_generator
except ImportError:
    waveform = None
    speech_to_text = None
    sematic_analysis = None
    report_generator = None

st.set_page_config(
    page_title="VBCUA - Concept Analyser",
    page_icon="🎙️",
    layout="wide"
)

st.title("🎙️ Voice-Based Concept Understanding Analyser")
st.markdown("""
Evaluate how effectively you understand and explain conceptual topics through spoken communication. 
This tool measures conceptual accuracy, fluency, delivery metrics, and generates a structured performance report.
""")
st.divider()

left_column, right_column = st.columns(2)

with left_column:
    st.header("📥 Audio Processing Portal")
    
    target_topic = st.selectbox(
        "Choose the concept topic you are explaining:",
        list(REFERENCE_CONCEPTS.keys())
    )
    
    uploaded_file = st.file_uploader(
        "Upload your spoken explanation audio file (.mp3, .wav, .m4a):",
        type=["mp3", "wav", "m4a"]
    )
    
    if uploaded_file is not None:
        os.makedirs("uploads", exist_ok=True)
        saved_file_path = os.path.join("uploads", uploaded_file.name)
        
        with open(saved_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        st.success(f"Successfully uploaded: {uploaded_file.name}")
        st.audio(saved_file_path, format="audio/wav")
        
        if st.button("🚀 Analyze Concept Explanation", use_container_width=True):
            with st.spinner("🤖 Processing voice acoustics and running AI evaluation pipelines..."):
                try:
                    st.session_state["current_topic"] = target_topic
                    
                    if waveform:
                        st.session_state["metrics"] = waveform.analyze_audio_fluency(saved_file_path)
                        st.session_state["chart_path"] = waveform.generate_waveform_plot(saved_file_path)
                    
                    user_text = ""
                    if speech_to_text:
                        stt_result = speech_to_text.transcribe_audio(saved_file_path)
                        user_text = stt_result.get("text", "")
                        st.session_state["transcript"] = user_text
                    
                    if sematic_analysis and user_text:
                        ref_text = REFERENCE_CONCEPTS[target_topic]
                        st.session_state["evaluation"] = sematic_analysis.evaluate_semantic_similarity(user_text, ref_text)
                    
                    st.session_state["analysis_triggered"] = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")

with right_column:
    st.header("📊 Analytical Report Output")
    
    if "analysis_triggered" not in st.session_state:
        st.info("Upload an audio file on the left panel and click 'Analyze' to review metrics here.")
    else:
        topic = st.session_state.get("current_topic", "Concept Evaluation")
        metrics = st.session_state.get("metrics", {})
        chart_path = st.session_state.get("chart_path", None)
        transcript = st.session_state.get("transcript", "")
        evaluation = st.session_state.get("evaluation", {})
        
        if "error" in metrics:
            st.error(metrics["error"])
        else:
            st.subheader("🔊 Fluency & Delivery Signals")
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            metric_col1.metric("Duration", f"{metrics.get('duration_sec')} sec")
            metric_col2.metric("Pause Ratio", f"{int(metrics.get('pause_ratio', 0) * 100)}%")
            metric_col3.metric("RMS Energy (Loudness)", f"{metrics.get('rms_energy')}")
            
            if chart_path and os.path.exists(chart_path):
                st.subheader("📉 Signal Amplitude Waveform")
                st.image(chart_path, use_container_width=True)
                
            st.divider()
            
            st.subheader("📝 Transcription Result")
            if transcript:
                st.text_area("Whisper Model Speech-to-Text:", value=transcript, height=100, disabled=True)
            else:
                st.warning("No speech patterns detected in audio file.")
                
            st.divider()
            
            st.subheader("🎯 Conceptual Semantic Evaluation")
            if "error" in evaluation:
                st.error(evaluation["error"])
            elif evaluation:
                score_val = evaluation.get("score", 0.0)
                level_val = evaluation.get("level", "Unknown")
                feedback_val = evaluation.get("feedback", "")
                
                eval_col1, eval_col2 = st.columns(2)
                eval_col1.metric("Semantic Match Accuracy", f"{score_val}%")
                
                if "Strong" in level_val:
                    eval_col2.success(level_val)
                elif "Moderate" in level_val:
                    eval_col2.warning(level_val)
                else:
                    eval_col2.error(level_val)
                    
                st.info(f"💡 **AI Feedback:** {feedback_val}")
                
                if report_generator:
                    st.divider()
                    st.subheader("📥 Export Performance Summary")
                    try:
                        pdf_file_path = report_generator.generate_pdf_report(
                            topic=topic,
                            metrics=metrics,
                            transcript=transcript,
                            evaluation=evaluation,
                            chart_path=chart_path
                        )
                        
                        if os.path.exists(pdf_file_path):
                            with open(pdf_file_path, "rb") as pdf_file:
                                st.download_button(
                                    label="Download Evaluation Report (PDF)",
                                    data=pdf_file,
                                    file_name="Evaluation_Report.pdf",
                                    mime="application/pdf",
                                    use_container_width=True
                                )
                    except Exception as pdf_error:
                        st.error(f"Could not build PDF interface: {str(pdf_error)}")
