import librosa
import numpy as np
from scipy import signal
from typing import Dict, Tuple, Optional


class FrequencyAnalyzer:

    
    def __init__(self, n_fft: int = 2048, hop_length: int = 512,
                 n_mels: int = 128, n_mfcc: int = 13):

        self.n_fft = n_fft
        self.hop_length = hop_length
        self.n_mels = n_mels
        self.n_mfcc = n_mfcc
    
    def compute_fft(self, audio: np.ndarray, sr: int) -> Tuple[np.ndarray, np.ndarray]:

        fft_result = np.fft.fft(audio)
        
        n = len(audio)
        magnitudes = np.abs(fft_result[:n//2])
        
        frequencies = np.fft.fftfreq(n, 1/sr)[:n//2]
        
        magnitudes_db = librosa.amplitude_to_db(magnitudes, ref=np.max)
        
        return frequencies, magnitudes_db
    
    def compute_power_spectrum(self, audio: np.ndarray, 
                                sr: int) -> Tuple[np.ndarray, np.ndarray]:

        frequencies, psd = signal.welch(audio, sr, nperseg=self.n_fft)
        psd_db = 10 * np.log10(psd + 1e-10)
        return frequencies, psd_db
    
    def compute_spectrogram(self, audio: np.ndarray, 
                            sr: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:

        stft = librosa.stft(audio, n_fft=self.n_fft, hop_length=self.hop_length)
        
        spectrogram_db = librosa.amplitude_to_db(np.abs(stft), ref=np.max)
        
        frequencies = librosa.fft_frequencies(sr=sr, n_fft=self.n_fft)
        times = librosa.times_like(stft, sr=sr, hop_length=self.hop_length)
        
        return spectrogram_db, frequencies, times
    
    def compute_mel_spectrogram(self, audio: np.ndarray, 
                                 sr: int) -> np.ndarray:
        mel_spec = librosa.feature.melspectrogram(
            y=audio, sr=sr, 
            n_fft=self.n_fft, 
            hop_length=self.hop_length,
            n_mels=self.n_mels
        )
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        return mel_spec_db
    
    def compute_mfcc(self, audio: np.ndarray, sr: int) -> np.ndarray:

        mfccs = librosa.feature.mfcc(
            y=audio, sr=sr,
            n_mfcc=self.n_mfcc,
            n_fft=self.n_fft,
            hop_length=self.hop_length
        )
        return mfccs
    
    def compute_chromagram(self, audio: np.ndarray, sr: int) -> np.ndarray:

        chroma = librosa.feature.chroma_stft(
            y=audio, sr=sr,
            n_fft=self.n_fft,
            hop_length=self.hop_length
        )
        return chroma
    
    def compute_spectral_features(self, audio: np.ndarray, 
                                   sr: int) -> Dict[str, np.ndarray]:

        features = {}
        
        # Spectral centroid
        features['centroid'] = librosa.feature.spectral_centroid(
            y=audio, sr=sr, n_fft=self.n_fft, hop_length=self.hop_length
        )[0]
        
        # Spectral bandwidth
        features['bandwidth'] = librosa.feature.spectral_bandwidth(
            y=audio, sr=sr, n_fft=self.n_fft, hop_length=self.hop_length
        )[0]
        
        # Spectral rolloff
        features['rolloff'] = librosa.feature.spectral_rolloff(
            y=audio, sr=sr, n_fft=self.n_fft, hop_length=self.hop_length
        )[0]
        
        # Spectral contrast
        features['contrast'] = librosa.feature.spectral_contrast(
            y=audio, sr=sr, n_fft=self.n_fft, hop_length=self.hop_length
        )
        
        # Zero crossing rate
        features['zcr'] = librosa.feature.zero_crossing_rate(
            audio, hop_length=self.hop_length
        )[0]
        
        # RMS energy
        features['rms'] = librosa.feature.rms(
            y=audio, hop_length=self.hop_length
        )[0]
        
        return features
    
    def extract_all_features(self, audio: np.ndarray, 
                              sr: int) -> Dict[str, np.ndarray]:

        features = {}
        
        features['fft_freqs'], features['fft_mags'] = self.compute_fft(audio, sr)
        features['psd_freqs'], features['psd'] = self.compute_power_spectrum(audio, sr)
        
        features['spectrogram'], features['spec_freqs'], features['spec_times'] = \
            self.compute_spectrogram(audio, sr)
        features['mel_spectrogram'] = self.compute_mel_spectrogram(audio, sr)
        
        features['mfcc'] = self.compute_mfcc(audio, sr)
        features['chromagram'] = self.compute_chromagram(audio, sr)
        
        spectral_features = self.compute_spectral_features(audio, sr)
        features.update(spectral_features)
        
        return features
    
    def get_feature_summary(self, features: Dict[str, np.ndarray]) -> Dict[str, float]:

        summary = {}
        
        # MFCC statistics
        if 'mfcc' in features:
            mfcc_mean = np.mean(features['mfcc'], axis=1)
            for i, val in enumerate(mfcc_mean):
                summary[f'mfcc_{i}_mean'] = val
        
        # Spectral feature statistics
        for key in ['centroid', 'bandwidth', 'rolloff', 'zcr', 'rms']:
            if key in features:
                summary[f'{key}_mean'] = np.mean(features[key])
                summary[f'{key}_std'] = np.std(features[key])
        
        return summary



