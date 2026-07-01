# Voice-Based Concept Understanding Analyser (VBCUA)

An advanced AI-powered educational technology system that evaluates how effectively technical conceptual frameworks are explained through spoken audio delivery. This platform extracts multi-dimensional speech telemetry, transcribes verbal frequencies, and calculates semantic matching precision scores against ground-truth benchmarks.

## 🚀 Key Features

- **Acoustic & Fluency Analytics Engine**: Leverages `librosa` to dynamically compute speaking durations, silence boundary tracking, signal variance, and acoustic energy density thresholds (RMS).
- **Speech-to-Text Pipeline**: Implements automatic speech recognition pipelines via Hugging Face and OpenAI Whisper checkpoints to translate spoken signals into clear text metadata.
- **Semantic Evaluation Engine**: Employs Sentence-BERT (`all-MiniLM-L6-v2`) deep learning embeddings to calculate semantic cosine similarity percentages against predefined benchmark definitions.
- **Relational Data Logger**: Automatically commits processing metadata, fluency stats, raw text strings, and final scores straight into your local MySQL Workbench database tables.
- **Reporting Architecture**: Generates beautifully formatted, downloadable PDF summaries embedding signal graph plots and technical feedback assessments using `reportlab`.

## 📂 Project Architecture

```text
vbcua-project/
│
├── app.py                      # Core Integrated Streamlit UI Dashboard Layout
├── requirements.txt            # Package Dependencies Configuration File
├── Dump20260701.sql            # Local MySQL Relational Database Export Schema 
│
├── modules/                    # Discrete Back-end Operational Subsystems
│   ├── audio_analysis.py       # Speech Signal Telemetry Extractor
│   ├── feedback.py             # Hesitation Tracker & Delivery Evaluator
│   ├── sematic_analysis.py     # Sentence-BERT Embedding Cosine Processor
│   ├── speech_to_text.py       # Automated Speech Recognition Pipeline
│   ├── report_generator.py     # PDF Template Builder Engine
│   └── database_logger.py      # MySQL Relational Schema Logger Bridge
│
├── uploads/                    # Temporary Directory Storing User Audios
├── reports/                    # Compiled Evaluation PDF Summary Documents
└── images/                     # Visualized Amplitude Signal Waveform Artifacts
```

## 🛠️ Environment Configuration & Launch

Follow these terminal steps inside your workspace directory to start up the project stack:

### 1. Initialize Workspace Environment
```bash
# Create isolated python virtual workspace
python3 -m venv vbcu_env

# Activate workspace parameters 
source vbcu_env/bin/activate
```

### 2. Configure Dependencies
```bash
# Install deep-learning and frontend modules
pip install -r requirements.txt
```

### 3. Initialize Relational Schema
Ensure your local instance of MySQL is operational, run the database engine, and execute the structural commands contained inside `Dump20260701.sql` to map out your 10 relational data structures.

### 4. Deploy the Front-End Platform
```bash
streamlit run app.py
```
The interface will automatically deploy and register onto `http://localhost:8501`.
s