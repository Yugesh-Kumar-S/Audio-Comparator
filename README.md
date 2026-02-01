# Project Overview & Architecture
## Audio Frequency Comparison Application

This document outlines the technical architecture, workflow, and component structure of the application.

## 1. High-Level Workflow
The application follows a standard **Client-Server** architecture:

1.  **User Interface (Frontend)**: User uploads two audio files via the React web app.
2.  **API Request (HTTP)**: Frontend sends files to the Backend via a `POST /analyze` request.
3.  **Processing (Backend)**:
    *   **Loading**: Audio is loaded, converted to mono, and normalized.
    *   **Feature Extraction**: Librosa extracts MFCCs, Spectral features, and PSD.
    *   **Comparison**: Similarity algorithms compare the feature sets.
4.  **Response**: Backend returns a JSON object with similarity scores and graph data.
5.  **Visualization**: Frontend renders the similarity score and frequency graphs.

## 2. Directory Structure & Organization

AudioFrequencyComparison/
├── backend/                # Web Server Layer (FastAPI)
│   ├── main.py             # API entry point & route handling
│   └── temp_uploads/       # Temporary storage for processed files
├── frontend/               # User Interface Layer (React + Vite)
│   ├── src/
│   │   ├── components/     # Reusable UI components (Graph, Results)
│   │   ├── pages/          # Page layouts (Home, Results)
│   │   └── App.jsx         # Main application container
│   └── vite.config.js      # Frontend build configuration
├── src/                    # Core Logic Layer (Shared Modules)
│   ├── audio_loader.py     # Audio I/O and normalization
│   ├── feature_extractor.py# Feature extraction (MFCC, PSD)
│   ├── frequency_analysis.py # Spectral analysis computations
│   ├── similarity.py       # Similarity metrics & algorithms
│   └── visualization.py    # Plotting & visualization logic
├── audio_samples/          # Test audio recordings
├── generate_samples.py     # Utility to create test audio files
├── main.py                 # CLI entry point (optional usage)
├── requirements.txt        # Python dependency list
└── README.md               # Project documentation

## 3. Component Details

### Core Logic (`/src`)
*   **`audio_loader.py`**:
    *   Uses `librosa.load` to read audio.
    *   Resamples to 22,050 Hz (standard for speech/music analysis).
    *   Normalizes volume to -1 to +1 range.
*   **`feature_extractor.py`**:
    *   **MFCC**: Mel-frequency cepstral coefficients (timbre/voice char).
    *   **Spectral Centroid**: "Brightness" of the sound.
    *   **Power Spectral Density (PSD)**: Frequency distribution (used for the graph).
    *   **Mel Spectrogram**: Time-frequency representation.
*   **`similarity.py`**:
    *   Calculates Euclidean distance and Cosine similarity between feature vectors.
    *   Uses **Dynamic Time Warping (DTW)** to compare audio of different lengths/speeds.
    *   Weighted average produces the final "Match %".

### Web Application Modules
*   **`feature_extractor.py`** (Used by Backend): Optimized for the API. Extracts MFCCs and PSD data efficiently for the frontend.
*   **`backend/main.py`**: A FastAPI server that handles file uploads, runs analysis, and returns JSON data to reliability serve the React frontend.
*   **`frontend/`**:
    *   **`FrequencyGraph.jsx`**: A professional **Area Chart** using Recharts. Features smooth gradients, filtered voice range (0-8kHz), and interactive tooltips.
    *   **Glassmorphism UI**: Premium styling via `index.css`.

### CLI / Research Modules (Optional)
*   **`frequency_analysis.py`**: Detailed frequency breakdown (FFT, Spectrograms) used by the standalone CLI tool.
*   **`visualization.py`**: Generates static Matplotlib images (PNGs) when running locally via `python main.py`.
*   **`main.py` (Root)**: Command-line interface for running analysis without the web server. Useful for batch processing or debugging.

## 4. Data Flow Example
1.  **Frontend** sends `audio1.wav` and `audio2.wav`.
2.  **Backend** saves them to `temp_uploads/`.
3.  **Backend** calls `FeatureExtractor.extract(audio1)`.
    *   *Result*: `{ 'mfcc': [[-200, ...], ...], 'psd': [0.01, 0.05, ...] }`
4.  **Backend** calls `SimilarityCalculator.compare(feat1, feat2)`.
    *   *Result*: `85.5%`
5.  **Backend** cleans up (deletes) files in `temp_uploads/`.
6.  **Backend** responds with JSON.
7.  **Frontend** displays "85.5% Similarity" and draws the chart.

## 5. Installation & Setup

### Prerequisites
*   **Python 3.8+**
*   **Node.js 16+** (for Frontend)

### 1. Backend Setup
1.  Navigate to the project root:
    ```bash
    cd AudioFrequencyComparison
    ```
2.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### 2. Frontend Setup
1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2.  Install Node dependencies:
    ```bash
    npm install
    ```

## 6. Running the Application

Measurement requires **two** terminal windows running simultaneously.

### Terminal 1: Backend API
```bash
# Make sure you are in AudioFrequencyComparison/backend
# and your venv is activated
cd backend
python main.py
```
*The server will start at `http://localhost:8000`*

### Terminal 2: Frontend UI
```bash
# Make sure you are in AudioFrequencyComparison/frontend
cd frontend
npm run dev
```
*The app will be accessible at `http://localhost:5173`*
