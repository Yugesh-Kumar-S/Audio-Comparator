#!/usr/bin/env python3

import numpy as np
from scipy.io import wavfile
from pathlib import Path

def generate_sine_wave(frequency: float, duration: float, 
                       sample_rate: int = 22050, 
                       amplitude: float = 0.5) -> np.ndarray:
    """Generate a sine wave audio signal."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    return amplitude * np.sin(2 * np.pi * frequency * t)

def generate_complex_tone(frequencies: list, duration: float,
                          sample_rate: int = 22050) -> np.ndarray:
    """Generate a complex tone with multiple harmonics."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    signal = np.zeros_like(t)
    for i, freq in enumerate(frequencies):
        amplitude = 0.5 / (i + 1)  # Decreasing amplitude for harmonics
        signal += amplitude * np.sin(2 * np.pi * freq * t)
    # Normalize
    signal = signal / np.max(np.abs(signal)) * 0.8
    return signal

def add_envelope(signal: np.ndarray, attack: float = 0.1, 
                 decay: float = 0.1) -> np.ndarray:
    """Add attack and decay envelope to the signal."""
    n = len(signal)
    attack_samples = int(n * attack)
    decay_samples = int(n * decay)
    
    envelope = np.ones(n)
    
    # Attack
    envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    # Decay
    envelope[-decay_samples:] = np.linspace(1, 0, decay_samples)
    
    return signal * envelope

def main():
    sample_rate = 22050
    duration = 3.0  # seconds
    
    output_dir = Path(__file__).parent / "audio_samples"
    output_dir.mkdir(exist_ok=True)
    
    print("Generating sample audio files for testing...")
    print("=" * 50)
    
    # Audio 1: Simple tone with harmonics (like a voice/instrument)
    base_freq = 220  # A3 note
    frequencies1 = [base_freq, base_freq * 2, base_freq * 3, base_freq * 4]
    audio1 = generate_complex_tone(frequencies1, duration, sample_rate)
    audio1 = add_envelope(audio1)
    
    # Add some variation/vibrato
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    vibrato = 1 + 0.02 * np.sin(2 * np.pi * 5 * t)  # 5 Hz vibrato
    audio1 = audio1 * vibrato
    
    # Audio 2: Similar tone with slight frequency shift (like a similar voice)
    base_freq2 = 225  # Slightly different
    frequencies2 = [base_freq2, base_freq2 * 2, base_freq2 * 3, base_freq2 * 4]
    audio2 = generate_complex_tone(frequencies2, duration, sample_rate)
    audio2 = add_envelope(audio2)
    
    # Different vibrato pattern
    vibrato2 = 1 + 0.015 * np.sin(2 * np.pi * 4.5 * t)
    audio2 = audio2 * vibrato2
    
    # Convert to 16-bit integer
    audio1_int = (audio1 * 32767).astype(np.int16)
    audio2_int = (audio2 * 32767).astype(np.int16)
    
    # Save files
    file1 = output_dir / "sample_audio_1.wav"
    file2 = output_dir / "sample_audio_2.wav"
    
    wavfile.write(str(file1), sample_rate, audio1_int)
    wavfile.write(str(file2), sample_rate, audio2_int)
    
    print(f"\nGenerated: {file1}")
    print(f"  - Base frequency: {base_freq} Hz")
    print(f"  - Harmonics: {frequencies1}")
    print(f"  - Duration: {duration}s")
    
    print(f"\nGenerated: {file2}")
    print(f"  - Base frequency: {base_freq2} Hz")
    print(f"  - Harmonics: {frequencies2}")
    print(f"  - Duration: {duration}s")
    
    # Also generate a very different audio file for comparison
    base_freq3 = 440  # A4 - one octave higher
    frequencies3 = [base_freq3, base_freq3 * 1.5, base_freq3 * 2]  # Different harmonic structure
    audio3 = generate_complex_tone(frequencies3, duration * 0.8, sample_rate)  # Different duration
    audio3 = add_envelope(audio3, attack=0.2, decay=0.3)
    audio3_int = (audio3 * 32767).astype(np.int16)
    
    file3 = output_dir / "sample_audio_3_different.wav"
    wavfile.write(str(file3), sample_rate, audio3_int)
    
    print(f"\nGenerated: {file3}")
    print(f"  - Base frequency: {base_freq3} Hz (different octave)")
    print(f"  - Harmonics: {frequencies3} (different structure)")
    print(f"  - Duration: {duration * 0.8}s")
    
    print("\n" + "=" * 50)
    print("Sample audio files generated successfully!")
    print(f"\nTo test the comparison tool, run:")
    print(f'  python main.py "{file1}" "{file2}"')
    print(f"\nFor testing with different audio:")
    print(f'  python main.py "{file1}" "{file3}"')

if __name__ == "__main__":
    main()
