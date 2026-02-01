import librosa
import numpy as np
from typing import Tuple, Optional


class AudioLoader:

    def __init__(self, target_sr: int = 22050, mono: bool = True):

        self.target_sr = target_sr
        self.mono = mono
    
    def load(self, file_path: str) -> Tuple[np.ndarray, int]:

        audio, sr = librosa.load(
            file_path, 
            sr=self.target_sr, 
            mono=self.mono
        )
        
        audio = self.normalize(audio)
        
        return audio, sr
    
    def normalize(self, audio: np.ndarray) -> np.ndarray:

        max_val = np.max(np.abs(audio))
        if max_val > 0:
            audio = audio / max_val
        return audio
    
    def get_duration(self, audio: np.ndarray, sr: int) -> float:

        return len(audio) / sr
    
    def trim_silence(self, audio: np.ndarray, 
                     top_db: int = 20) -> np.ndarray:

        trimmed, _ = librosa.effects.trim(audio, top_db=top_db)
        return trimmed
    
    def pad_or_truncate(self, audio: np.ndarray, 
                        target_length: int) -> np.ndarray:

        if len(audio) > target_length:
            return audio[:target_length]
        elif len(audio) < target_length:
            padding = target_length - len(audio)
            return np.pad(audio, (0, padding), mode='constant')
        return audio
    
    def match_lengths(self, audio1: np.ndarray, 
                      audio2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:

        max_length = max(len(audio1), len(audio2))
        audio1 = self.pad_or_truncate(audio1, max_length)
        audio2 = self.pad_or_truncate(audio2, max_length)
        return audio1, audio2



