# Voice-Based Concept Understanding Analyser (VBCUA)

An advanced AI-powered educational technology platform that evaluates how effectively technical conceptual frameworks are explained through spoken audio delivery. This platform extracts multi-dimensional speech telemetry, transcribes verbal frequencies, and calculates semantic matching precision scores against ground-truth benchmarks.

---

##  Project Architecture & Tracking Phases
This repository is organized strictly according to the tracking template configuration across sequential milestones:

*   **`1. Brainstorming & Ideation`**: Core concept definition and strategic roadmap targets.
*   **`2. Requirement Analysis`**: Functional constraints and library dependencies.
*   **`3. Project Design Phase`**: Architectural pipeline workflows and MySQL database schema diagrams.
*   **`4. Project Planning Phase`**: Milestone sprint tracking and development timelines.
*   **`5. Project Development Phase`**: Active functional codebase housing the Streamlit application environment and modular backend engines.
*   **`6.Project Testing`**: System validation passes and automated code checking logs.
*   **`7.Project Documentation`**: Local deployment configuration guides and user operations manuals.
*   **`8.Project Demonstration`**: Project walk-through structures and video review parameters.

---

##  Key Platform Features
*   ** Acoustic Analytics Engine**: Leverages `librosa` to compute speaking durations, silence boundary patterns, and average root-mean-square (`rms_energy`) amplitude values.
*   ** Speech-to-Text Pipeline**: Implements automated speech recognition via cached Hugging Face OpenAI Whisper checkpoints to safely decode spoken arrays into plain text meta-strings.
*   ** Semantic Evaluation Engine**: Utilizes Sentence-BERT (`SBERT` via `all-MiniLM-L6-v2`) deep learning embedding vectors to calculate cosine similarity metrics against benchmark definitions.
*   ** Compound Scoring Module**: Implements a balanced 100-point algorithm evaluating semantics (50 pts), delivery filler counts (20 pts), and fluency energy parameters (30 pts).
*   ** Automated PDF Compiler**: Uses `reportlab` to construct downloadable data portfolios displaying waveform charts alongside student grading analytics.

---

##  Technical Stack
*   **Interface Layer**: Streamlit
*   **Audio Signal Processing**: Librosa, SoundFile, AudioRead
*   **Machine Learning Subsystems**: PyTorch, Transformers, Sentence-Transformers, OpenAI-Whisper
*   **Data Serialization & Relational Storage**: MySQL Workbench
*   **Graphics & Reporting**: Matplotlib, ReportLab

---

##  Quick Local Deployment Guide

1. Ensure your isolated virtual workspace is fully initialized:
   ```bash
   source vbcu_env/bin/activate  # Windows users: .\vbcu_env\Scripts\activate
   ```
2. Confirm systemic library requirements are operational:
   ```bash
   pip install -r "5. Project Development Phase/requirements.txt"
   ```
3. Initialize the server engine via your terminal prompt:
   ```bash
   streamlit run "5. Project Development Phase/app.py"
   ```
