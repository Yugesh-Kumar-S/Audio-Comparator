import librosa
import numpy as np
import scipy.signal
from typing import Dict, Any

class FeatureExtractor:

    
    def __init__(self, n_mfcc: int = 13, n_mels: int = 128, hop_length: int = 512):

        self.n_mfcc = n_mfcc
        self.n_mels = n_mels
        self.hop_length = hop_length
        
    def extract(self, audio: np.ndarray, sr: int) -> Dict[str, Any]:

        features = {}
        
        # 1. MFCCs
        features['mfcc'] = librosa.feature.mfcc(
            y=audio, sr=sr, n_mfcc=self.n_mfcc, hop_length=self.hop_length
        )
        
        # 2. Spectral Centroid
        features['centroid'] = librosa.feature.spectral_centroid(
            y=audio, sr=sr, hop_length=self.hop_length
        )
        
        # 3. Spectral Bandwidth
        features['bandwidth'] = librosa.feature.spectral_bandwidth(
            y=audio, sr=sr, hop_length=self.hop_length
        )
        
        # 4. Spectral Rolloff
        features['rolloff'] = librosa.feature.spectral_rolloff(
            y=audio, sr=sr, hop_length=self.hop_length
        )
        
        # 5. RMS Energy
        features['rms'] = librosa.feature.rms(
            y=audio, hop_length=self.hop_length
        )
        
        # 6. Mel Spectrogram
        features['mel_spectrogram'] = librosa.feature.melspectrogram(
            y=audio, sr=sr, n_mels=self.n_mels, hop_length=self.hop_length
        )
        
        # 7. Power Spectral Density (PSD) using Welch's method
        # Returns (frequencies, power_spectrum)
        freqs, psd = scipy.signal.welch(audio, fs=sr, nperseg=2048)
        features['psd'] = psd
        features['psd_freqs'] = freqs
        
        return features

if __name__ == "__main__":
    # Test stub
    print("FeatureExtractor initialized.")
