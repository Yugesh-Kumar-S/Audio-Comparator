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

```
AudioFrequencyComparison/
├── backend/                # Web Server Layer
│   └── main.py             # FastAPI entry point, handles uploads & API routes
├── frontend/               # User Interface Layer
│   ├── src/                # React source code
│   │   ├── components/     # UI Components (Graph, Uploader, Results)
│   │   └── App.jsx         # Main application logic
│   └── vite.config.js      # Build config & API proxy
├── src/                    # Core Logic Layer (Business Logic)
│   ├── audio_loader.py     # Handles file loading & preprocessing
│   ├── feature_extractor.py# Computes mathematical audio features (MFCC, PSD)
│   └── similarity.py       # Implements the comparison algorithms
├── audio_samples/          # (Optional) Test audio files
├── requirements.txt        # Python dependencies
└── README.md               # General entry point
```

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

### Backend (`/backend`)
*   **`main.py`**:
    *   **FastAPI**: A high-performance web framework.
    *   **Endpoints**:
        *   `POST /analyze`: The heavy lifter. Accepts `multipart/form-data`.
    *   **Error Handling**: Catches invalid files and processing errors.
    *   **Serialization**: Converts NumPy arrays (not JSON serializable) into standard Python lists using a custom sanitizer.

### Frontend (`/frontend`)
*   **React + Vite**: Fast, modern SPA framework.
*   **Glassmorphism UI**: Custom CSS in `index.css` for the translucent, premium look.
*   **`FrequencyGraph.jsx`**: Uses `recharts` to plot the PSD (Power vs Frequency) data returned by the backend.
*   **Proxy**: `vite.config.js` proxies requests from `localhost:5173` -> `localhost:8000` to avoid CORS issues during development.

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
