from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import sys
import numpy as np
import json
from typing import Dict, Any

# Add src to path to import local modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.audio_loader import AudioLoader
from src.feature_extractor import FeatureExtractor
from src.similarity import SimilarityCalculator

app = FastAPI(title="Audio Frequency Comparison API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for dev; restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
loader = AudioLoader()
extractor = FeatureExtractor()
similarity_calc = SimilarityCalculator()

TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)

def process_audio(file_path: str):
    try:
        audio, sr = loader.load(file_path)
        # Trim silence for better analysis
        audio = loader.trim_silence(audio)
        return audio, sr
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing audio: {str(e)}")


# Utility to convert numpy types to native python types
def sanitize_for_json(obj):
    if isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_for_json(i) for i in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return sanitize_for_json(obj.tolist())
    else:
        return obj

@app.post("/analyze")
async def analyze_audio(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    file1_path = os.path.join(TEMP_DIR, file1.filename)
    file2_path = os.path.join(TEMP_DIR, file2.filename)
    
    try:
        # Ensure temp directory exists
        if not os.path.exists(TEMP_DIR):
            os.makedirs(TEMP_DIR)

        # Save uploaded files
        with open(file1_path, "wb") as buffer:
            shutil.copyfileobj(file1.file, buffer)
        with open(file2_path, "wb") as buffer:
            shutil.copyfileobj(file2.file, buffer)
            
        # Load and preprocess
        audio1, sr1 = process_audio(file1_path)
        audio2, sr2 = process_audio(file2_path)
        
        # Extract features
        features1 = extractor.extract(audio1, sr1)
        features2 = extractor.extract(audio2, sr2)
        
        # Compute similarity
        similarity_results = similarity_calc.compute_overall_similarity(features1, features2)
        interpretation = similarity_calc.get_similarity_interpretation(similarity_results['overall_similarity'])
        
        # Prepare graph data (PSD for frequency domain visualization)
        max_freq_points = 200 # limit points for chart
        
        def downsample_psd(freqs, psd, points):
            if len(freqs) <= points:
                return freqs, psd
            indices = np.linspace(0, len(freqs)-1, points, dtype=int)
            return freqs[indices], psd[indices]
            
        freqs1, psd1 = downsample_psd(features1['psd_freqs'], features1['psd'], max_freq_points)
        freqs2, psd2 = downsample_psd(features2['psd_freqs'], features2['psd'], max_freq_points)
        
        graph_data = {
            "audio1": {
                "label": file1.filename,
                "freqs": freqs1,
                "psd": psd1
            },
            "audio2": {
                "label": file2.filename,
                "freqs": freqs2,
                "psd": psd2
            }
        }
        
        response_data = {
            "similarity_score": similarity_results['overall_similarity'],
            "breakdown": similarity_results,
            "interpretation": interpretation,
            "graph_data": graph_data
        }
        
        # Sanitize entire response to ensure no numpy types cause crashes
        return sanitize_for_json(response_data)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # Cleanup
        try:
            if os.path.exists(file1_path):
                os.remove(file1_path)
            if os.path.exists(file2_path):
                os.remove(file2_path)
        except Exception:
            pass

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    # Run directly
    uvicorn.run(app, host="127.0.0.1", port=8000)
