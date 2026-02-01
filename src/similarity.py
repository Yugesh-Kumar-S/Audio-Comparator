import numpy as np
from scipy import stats
from scipy.spatial.distance import cosine, euclidean
from fastdtw import fastdtw
from typing import Dict, Tuple, List, Optional


class SimilarityCalculator:

    
    def __init__(self, weights: Optional[Dict[str, float]] = None):

        self.weights = weights or {
            'mfcc': 0.35,
            'spectral': 0.25,
            'frequency_distribution': 0.20,
            'temporal_pattern': 0.20
        }
    
    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:

        vec1 = vec1.flatten()
        vec2 = vec2.flatten()
        
        min_len = min(len(vec1), len(vec2))
        vec1 = vec1[:min_len]
        vec2 = vec2[:min_len]
        
        if np.all(vec1 == 0) or np.all(vec2 == 0):
            return 0.0
        
        similarity = 1 - cosine(vec1, vec2)
        return max(0, similarity)
    
    def euclidean_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:

        vec1 = vec1.flatten()
        vec2 = vec2.flatten()
        
        min_len = min(len(vec1), len(vec2))
        vec1 = vec1[:min_len]
        vec2 = vec2[:min_len]
        
        vec1_norm = (vec1 - np.mean(vec1)) / (np.std(vec1) + 1e-10)
        vec2_norm = (vec2 - np.mean(vec2)) / (np.std(vec2) + 1e-10)
        
        distance = euclidean(vec1_norm, vec2_norm)
        similarity = 1 / (1 + distance / len(vec1))
        
        return similarity
    
    def correlation_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:

        vec1 = vec1.flatten()
        vec2 = vec2.flatten()
        
        min_len = min(len(vec1), len(vec2))
        vec1 = vec1[:min_len]
        vec2 = vec2[:min_len]
        
        correlation, _ = stats.pearsonr(vec1, vec2)
        
        similarity = (correlation + 1) / 2
        
        return similarity
    
    def dtw_similarity(self, seq1: np.ndarray, seq2: np.ndarray,
                       max_samples: int = 500) -> float:

        try:
            if seq1.ndim > 1 and seq1.shape[0] < seq1.shape[1]:
                seq1 = seq1.T
            if seq2.ndim > 1 and seq2.shape[0] < seq2.shape[1]:
                seq2 = seq2.T
            
            if seq1.ndim > 1 and seq2.ndim > 1:
                min_features = min(seq1.shape[1], seq2.shape[1])
                seq1 = seq1[:, :min_features]
                seq2 = seq2[:, :min_features]
            
            if len(seq1) > max_samples:
                step = len(seq1) // max_samples
                seq1 = seq1[::step]
            if len(seq2) > max_samples:
                step = len(seq2) // max_samples
                seq2 = seq2[::step]
            
            distance, _ = fastdtw(seq1, seq2, dist=euclidean)
            
            normalized_distance = distance / (len(seq1) + len(seq2))
            similarity = 1 / (1 + normalized_distance)
            
            return similarity
        except Exception:
            return self.correlation_similarity(seq1.flatten(), seq2.flatten())
    
    def mfcc_similarity(self, mfcc1: np.ndarray, mfcc2: np.ndarray) -> float:

        mfcc1_mean = np.mean(mfcc1, axis=1)
        mfcc2_mean = np.mean(mfcc2, axis=1)
        
        cos_sim = self.cosine_similarity(mfcc1_mean, mfcc2_mean)
        
        dtw_sim = self.dtw_similarity(mfcc1, mfcc2)
        
        combined = 0.5 * cos_sim + 0.5 * dtw_sim
        
        return combined
    
    def spectral_similarity(self, features1: Dict[str, np.ndarray],
                            features2: Dict[str, np.ndarray]) -> float:
        similarities = []
        
        # Compare spectral centroid
        if 'centroid' in features1 and 'centroid' in features2:
            sim = self.correlation_similarity(features1['centroid'], 
                                              features2['centroid'])
            similarities.append(sim)
        
        # Compare spectral bandwidth
        if 'bandwidth' in features1 and 'bandwidth' in features2:
            sim = self.correlation_similarity(features1['bandwidth'],
                                              features2['bandwidth'])
            similarities.append(sim)
        
        # Compare spectral rolloff
        if 'rolloff' in features1 and 'rolloff' in features2:
            sim = self.correlation_similarity(features1['rolloff'],
                                              features2['rolloff'])
            similarities.append(sim)
        
        # Compare RMS energy
        if 'rms' in features1 and 'rms' in features2:
            sim = self.correlation_similarity(features1['rms'],
                                              features2['rms'])
            similarities.append(sim)
        
        return np.mean(similarities) if similarities else 0.5
    
    def frequency_distribution_similarity(self, psd1: np.ndarray,
                                           psd2: np.ndarray) -> float:
        # Normalize PSDs
        psd1_norm = (psd1 - np.min(psd1)) / (np.max(psd1) - np.min(psd1) + 1e-10)
        psd2_norm = (psd2 - np.min(psd2)) / (np.max(psd2) - np.min(psd2) + 1e-10)
        
        # Cosine similarity on normalized PSDs
        cos_sim = self.cosine_similarity(psd1_norm, psd2_norm)
        
        # Correlation
        corr_sim = self.correlation_similarity(psd1_norm, psd2_norm)
        
        return 0.5 * cos_sim + 0.5 * corr_sim
    
    def temporal_pattern_similarity(self, mel1: np.ndarray,
                                     mel2: np.ndarray) -> float:

        # Use DTW on mel spectrograms
        return self.dtw_similarity(mel1, mel2)
    
    def compute_overall_similarity(self, features1: Dict[str, np.ndarray],
                                    features2: Dict[str, np.ndarray]) -> Dict[str, float]:
        results = {}
        
        # MFCC similarity
        mfcc_sim = self.mfcc_similarity(features1['mfcc'], features2['mfcc'])
        results['mfcc_similarity'] = mfcc_sim * 100
        
        # Spectral similarity
        spectral_sim = self.spectral_similarity(features1, features2)
        results['spectral_similarity'] = spectral_sim * 100
        
        # Frequency distribution similarity
        freq_sim = self.frequency_distribution_similarity(
            features1['psd'], features2['psd']
        )
        results['frequency_distribution_similarity'] = freq_sim * 100
        
        # Temporal pattern similarity
        temporal_sim = self.temporal_pattern_similarity(
            features1['mel_spectrogram'], features2['mel_spectrogram']
        )
        results['temporal_pattern_similarity'] = temporal_sim * 100
        
        # Compute weighted overall score
        overall = (
            self.weights['mfcc'] * mfcc_sim +
            self.weights['spectral'] * spectral_sim +
            self.weights['frequency_distribution'] * freq_sim +
            self.weights['temporal_pattern'] * temporal_sim
        )
        results['overall_similarity'] = overall * 100
        
        return results
    
    def get_similarity_interpretation(self, score: float) -> str:

        if score >= 90:
            return "Very High - The audio recordings are extremely similar"
        elif score >= 75:
            return "High - The audio recordings share strong similarities"
        elif score >= 60:
            return "Moderate - The audio recordings have noticeable similarities"
        elif score >= 40:
            return "Low - The audio recordings have some similarities"
        elif score >= 20:
            return "Very Low - The audio recordings are quite different"
        else:
            return "Minimal - The audio recordings appear to be very different"



