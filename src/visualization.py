import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import librosa
import librosa.display
from typing import Dict, Tuple, Optional, List


class AudioVisualizer:

    
    def __init__(self, figsize: Tuple[int, int] = (14, 10),
                 style: str = 'seaborn-v0_8-darkgrid'):

        self.figsize = figsize
        try:
            plt.style.use(style)
        except:
            plt.style.use('default')
        
        # Color scheme for the two audio files
        self.colors = {
            'audio1': '#2196F3',  # Blue
            'audio2': '#FF5722',  # Orange
            'overlap': '#9C27B0'  # Purple (for overlapping regions)
        }
    
    def plot_waveforms(self, audio1: np.ndarray, audio2: np.ndarray,
                       sr: int, labels: Tuple[str, str] = ('Audio 1', 'Audio 2'),
                       ax: Optional[plt.Axes] = None) -> plt.Axes:

        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 4))
        
        time1 = np.arange(len(audio1)) / sr
        time2 = np.arange(len(audio2)) / sr
        
        ax.plot(time1, audio1, color=self.colors['audio1'], 
                alpha=0.7, label=labels[0], linewidth=0.5)
        ax.plot(time2, audio2, color=self.colors['audio2'], 
                alpha=0.7, label=labels[1], linewidth=0.5)
        
        ax.set_xlabel('Time (seconds)', fontsize=10)
        ax.set_ylabel('Amplitude', fontsize=10)
        ax.set_title('Waveform Comparison', fontsize=12, fontweight='bold')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
        
        return ax
    
    def plot_frequency_spectrum(self, freqs1: np.ndarray, mags1: np.ndarray,
                                 freqs2: np.ndarray, mags2: np.ndarray,
                                 labels: Tuple[str, str] = ('Audio 1', 'Audio 2'),
                                 ax: Optional[plt.Axes] = None,
                                 max_freq: int = 8000) -> plt.Axes:
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 4))
        
        # Filter to max frequency
        mask1 = freqs1 <= max_freq
        mask2 = freqs2 <= max_freq
        
        ax.plot(freqs1[mask1], mags1[mask1], color=self.colors['audio1'],
                alpha=0.7, label=labels[0], linewidth=1)
        ax.plot(freqs2[mask2], mags2[mask2], color=self.colors['audio2'],
                alpha=0.7, label=labels[1], linewidth=1)
        
        ax.set_xlabel('Frequency (Hz)', fontsize=10)
        ax.set_ylabel('Magnitude (dB)', fontsize=10)
        ax.set_title('Frequency Spectrum Comparison', fontsize=12, fontweight='bold')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, max_freq)
        
        return ax
    
    def plot_power_spectrum(self, freqs1: np.ndarray, psd1: np.ndarray,
                            freqs2: np.ndarray, psd2: np.ndarray,
                            labels: Tuple[str, str] = ('Audio 1', 'Audio 2'),
                            ax: Optional[plt.Axes] = None,
                            max_freq: int = 8000) -> plt.Axes:
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 4))
        
        # Filter to max frequency
        mask1 = freqs1 <= max_freq
        mask2 = freqs2 <= max_freq
        
        ax.semilogy(freqs1[mask1], 10**(psd1[mask1]/10), 
                    color=self.colors['audio1'], alpha=0.7, 
                    label=labels[0], linewidth=1)
        ax.semilogy(freqs2[mask2], 10**(psd2[mask2]/10), 
                    color=self.colors['audio2'], alpha=0.7, 
                    label=labels[1], linewidth=1)
        
        ax.set_xlabel('Frequency (Hz)', fontsize=10)
        ax.set_ylabel('Power Spectral Density', fontsize=10)
        ax.set_title('Power Spectrum Comparison', fontsize=12, fontweight='bold')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, max_freq)
        
        return ax
    
    def plot_spectrograms_comparison(self, spec1: np.ndarray, spec2: np.ndarray,
                                      sr: int, hop_length: int,
                                      labels: Tuple[str, str] = ('Audio 1', 'Audio 2'),
                                      axes: Optional[List[plt.Axes]] = None) -> List[plt.Axes]:

        if axes is None:
            fig, axes = plt.subplots(1, 2, figsize=(14, 4))
        
        # Plot first spectrogram
        img1 = librosa.display.specshow(spec1, sr=sr, hop_length=hop_length,
                                        x_axis='time', y_axis='hz', ax=axes[0],
                                        cmap='viridis')
        axes[0].set_title(f'Spectrogram - {labels[0]}', fontsize=11, fontweight='bold')
        axes[0].set_ylabel('Frequency (Hz)', fontsize=10)
        axes[0].set_xlabel('Time (s)', fontsize=10)
        plt.colorbar(img1, ax=axes[0], format='%+2.0f dB')
        
        # Plot second spectrogram
        img2 = librosa.display.specshow(spec2, sr=sr, hop_length=hop_length,
                                        x_axis='time', y_axis='hz', ax=axes[1],
                                        cmap='viridis')
        axes[1].set_title(f'Spectrogram - {labels[1]}', fontsize=11, fontweight='bold')
        axes[1].set_ylabel('Frequency (Hz)', fontsize=10)
        axes[1].set_xlabel('Time (s)', fontsize=10)
        plt.colorbar(img2, ax=axes[1], format='%+2.0f dB')
        
        return axes
    
    def plot_mel_spectrograms_comparison(self, mel1: np.ndarray, mel2: np.ndarray,
                                          sr: int, hop_length: int,
                                          labels: Tuple[str, str] = ('Audio 1', 'Audio 2'),
                                          axes: Optional[List[plt.Axes]] = None) -> List[plt.Axes]:

        if axes is None:
            fig, axes = plt.subplots(1, 2, figsize=(14, 4))
        
        # Plot first Mel spectrogram
        img1 = librosa.display.specshow(mel1, sr=sr, hop_length=hop_length,
                                        x_axis='time', y_axis='mel', ax=axes[0],
                                        cmap='magma')
        axes[0].set_title(f'Mel Spectrogram - {labels[0]}', fontsize=11, fontweight='bold')
        axes[0].set_ylabel('Mel Frequency', fontsize=10)
        axes[0].set_xlabel('Time (s)', fontsize=10)
        plt.colorbar(img1, ax=axes[0], format='%+2.0f dB')
        
        # Plot second Mel spectrogram
        img2 = librosa.display.specshow(mel2, sr=sr, hop_length=hop_length,
                                        x_axis='time', y_axis='mel', ax=axes[1],
                                        cmap='magma')
        axes[1].set_title(f'Mel Spectrogram - {labels[1]}', fontsize=11, fontweight='bold')
        axes[1].set_ylabel('Mel Frequency', fontsize=10)
        axes[1].set_xlabel('Time (s)', fontsize=10)
        plt.colorbar(img2, ax=axes[1], format='%+2.0f dB')
        
        return axes
    
    def plot_mfcc_comparison(self, mfcc1: np.ndarray, mfcc2: np.ndarray,
                             sr: int, hop_length: int,
                             labels: Tuple[str, str] = ('Audio 1', 'Audio 2'),
                             axes: Optional[List[plt.Axes]] = None) -> List[plt.Axes]:

        if axes is None:
            fig, axes = plt.subplots(1, 2, figsize=(14, 4))
        
        # Plot first MFCC
        img1 = librosa.display.specshow(mfcc1, sr=sr, hop_length=hop_length,
                                        x_axis='time', ax=axes[0], cmap='coolwarm')
        axes[0].set_title(f'MFCCs - {labels[0]}', fontsize=11, fontweight='bold')
        axes[0].set_ylabel('MFCC Coefficients', fontsize=10)
        axes[0].set_xlabel('Time (s)', fontsize=10)
        plt.colorbar(img1, ax=axes[0])
        
        # Plot second MFCC
        img2 = librosa.display.specshow(mfcc2, sr=sr, hop_length=hop_length,
                                        x_axis='time', ax=axes[1], cmap='coolwarm')
        axes[1].set_title(f'MFCCs - {labels[1]}', fontsize=11, fontweight='bold')
        axes[1].set_ylabel('MFCC Coefficients', fontsize=10)
        axes[1].set_xlabel('Time (s)', fontsize=10)
        plt.colorbar(img2, ax=axes[1])
        
        return axes
    
    def create_comprehensive_comparison(self, 
                                         features1: Dict[str, np.ndarray],
                                         features2: Dict[str, np.ndarray],
                                         sr: int, hop_length: int,
                                         similarity_score: float,
                                         labels: Tuple[str, str] = ('Audio 1', 'Audio 2'),
                                         save_path: Optional[str] = None) -> plt.Figure:

        # Create figure with custom layout
        fig = plt.figure(figsize=(16, 14))
        gs = gridspec.GridSpec(4, 2, figure=fig, height_ratios=[1, 1.2, 1.2, 1.2],
                               hspace=0.35, wspace=0.25)
        
        # Add main title with similarity score
        fig.suptitle(f'Audio Frequency Comparison Analysis\n'
                     f'Overall Similarity Score: {similarity_score:.1f}%',
                     fontsize=16, fontweight='bold', y=0.98)
        
        # Row 1: Frequency Spectrum (spanning both columns)
        ax1 = fig.add_subplot(gs[0, :])
        self.plot_frequency_spectrum(
            features1['fft_freqs'], features1['fft_mags'],
            features2['fft_freqs'], features2['fft_mags'],
            labels=labels, ax=ax1
        )
        
        # Row 2: Spectrograms side by side
        ax2a = fig.add_subplot(gs[1, 0])
        ax2b = fig.add_subplot(gs[1, 1])
        self.plot_spectrograms_comparison(
            features1['spectrogram'], features2['spectrogram'],
            sr, hop_length, labels=labels, axes=[ax2a, ax2b]
        )
        
        # Row 3: Mel Spectrograms side by side
        ax3a = fig.add_subplot(gs[2, 0])
        ax3b = fig.add_subplot(gs[2, 1])
        self.plot_mel_spectrograms_comparison(
            features1['mel_spectrogram'], features2['mel_spectrogram'],
            sr, hop_length, labels=labels, axes=[ax3a, ax3b]
        )
        
        # Row 4: MFCCs side by side
        ax4a = fig.add_subplot(gs[3, 0])
        ax4b = fig.add_subplot(gs[3, 1])
        self.plot_mfcc_comparison(
            features1['mfcc'], features2['mfcc'],
            sr, hop_length, labels=labels, axes=[ax4a, ax4b]
        )
        
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight',
                        facecolor='white', edgecolor='none')
        
        return fig
    
    def show(self):
        """Display all created plots."""
        plt.show()



