import os
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.audio_loader import AudioLoader
from src.frequency_analysis import FrequencyAnalyzer
from src.visualization import AudioVisualizer
from src.similarity import SimilarityCalculator


def print_header():
    """Print application header."""
    print("\n" + "=" * 70)
    print("   AUDIO FREQUENCY COMPARISON AND VOICE SIMILARITY EVALUATION")
    print("=" * 70 + "\n")


def print_results(results: dict, audio1_name: str, audio2_name: str):
    """Print formatted results to console."""
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 18 + "COMPARISON RESULTS" + " " * 32 + "║")
    print("╠" + "═" * 68 + "╣")
    print(f"║  Audio 1: {audio1_name[:50]:<56} ║")
    print(f"║  Audio 2: {audio2_name[:50]:<56} ║")
    print("╠" + "═" * 68 + "╣")
    print("║  SIMILARITY BREAKDOWN:" + " " * 45 + "║")
    print(f"║  ├── MFCC Similarity:          {results['mfcc_similarity']:>6.1f}%" + " " * 22 + "║")
    print(f"║  ├── Spectral Similarity:      {results['spectral_similarity']:>6.1f}%" + " " * 22 + "║")
    print(f"║  ├── Frequency Distribution:   {results['frequency_distribution_similarity']:>6.1f}%" + " " * 22 + "║")
    print(f"║  └── Temporal Pattern (DTW):   {results['temporal_pattern_similarity']:>6.1f}%" + " " * 22 + "║")
    print("╠" + "═" * 68 + "╣")
    print(f"║  OVERALL SIMILARITY SCORE:     {results['overall_similarity']:>6.1f}%" + " " * 22 + "║")
    print("╚" + "═" * 68 + "╝")
    
    calculator = SimilarityCalculator()
    interpretation = calculator.get_similarity_interpretation(results['overall_similarity'])
    print(f"\n  Interpretation: {interpretation}")


def analyze_audio_files(audio1_path: str, audio2_path: str, 
                        output_path: str = None, show_plot: bool = True) -> dict:
    print_header()
    
    loader = AudioLoader(target_sr=22050, mono=True)
    analyzer = FrequencyAnalyzer(n_fft=2048, hop_length=512, n_mels=128, n_mfcc=13)
    visualizer = AudioVisualizer()
    similarity_calc = SimilarityCalculator()
    
    print("Processing audio files...")
    
    try:
        audio1, sr = loader.load(audio1_path)
        audio2, sr = loader.load(audio2_path)
        
        audio1 = loader.trim_silence(audio1)
        audio2 = loader.trim_silence(audio2)
        
        features1 = analyzer.extract_all_features(audio1, sr)
        features2 = analyzer.extract_all_features(audio2, sr)
        
        results = similarity_calc.compute_overall_similarity(features1, features2)
        
        audio1_name = Path(audio1_path).name
        audio2_name = Path(audio2_path).name
        print_results(results, audio1_name, audio2_name)
        
        if output_path is None:
            output_dir = Path(__file__).parent / "output"
            output_dir.mkdir(exist_ok=True)
            output_path = str(output_dir / "comparison_result.png")
        
        visualizer.create_comprehensive_comparison(
            features1, features2,
            sr=sr, hop_length=analyzer.hop_length,
            similarity_score=results['overall_similarity'],
            labels=(audio1_name, audio2_name),
            save_path=output_path
        )
        
        print(f"\nGraph saved to: {output_path}")
        
        if show_plot:
            visualizer.show()
            
    except Exception as e:
        print(f"Error: {e}")
        return {}

    return results


def main():
    """Main entry point with command-line argument parsing."""
    parser = argparse.ArgumentParser(
        description="Audio Frequency Comparison and Voice Similarity Evaluation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py audio1.wav audio2.wav
  python main.py --audio1 speech1.mp3 --audio2 speech2.mp3 --output result.png
  python main.py audio1.wav audio2.wav --no-display
        """
    )
    
    parser.add_argument('audio1', nargs='?', help='Path to first audio file')
    parser.add_argument('audio2', nargs='?', help='Path to second audio file')
    parser.add_argument('--audio1', dest='audio1_named', 
                        help='Path to first audio file (named argument)')
    parser.add_argument('--audio2', dest='audio2_named',
                        help='Path to second audio file (named argument)')
    parser.add_argument('--output', '-o', 
                        help='Output path for comparison graph')
    parser.add_argument('--no-display', action='store_true',
                        help='Do not display the plot (only save)')
    
    args = parser.parse_args()
    
    # Get audio file paths (positional or named)
    audio1_path = args.audio1 or args.audio1_named
    audio2_path = args.audio2 or args.audio2_named
    
    # Check if demo mode (no arguments)
    if not audio1_path or not audio2_path:
        print_header()
        print("No audio files provided. Running in demo mode...")
        print("\nTo analyze your own audio files, use:")
        print("  python main.py <audio1.wav> <audio2.wav>")
        print("\nOr with named arguments:")
        print("  python main.py --audio1 <file1> --audio2 <file2>")
        
        # Check for sample files
        sample_dir = Path(__file__).parent / "audio_samples"
        if sample_dir.exists():
            samples = list(sample_dir.glob("*.wav")) + list(sample_dir.glob("*.mp3"))
            if len(samples) >= 2:
                print(f"\nFound sample files! Running analysis on:")
                print(f"  Audio 1: {samples[0].name}")
                print(f"  Audio 2: {samples[1].name}")
                audio1_path = str(samples[0])
                audio2_path = str(samples[1])
            else:
                print("\n⚠ Please add at least 2 audio files to the 'audio_samples' folder.")
                print("  Supported formats: WAV, MP3, FLAC, OGG")
                return
        else:
            print(f"\n⚠ Sample directory not found. Creating '{sample_dir}'...")
            sample_dir.mkdir(exist_ok=True)
            print("  Please add audio files to this folder and run again.")
            return
    
    # Validate file paths
    if not Path(audio1_path).exists():
        print(f"\n❌ Error: Audio file not found: {audio1_path}")
        return
    if not Path(audio2_path).exists():
        print(f"\n❌ Error: Audio file not found: {audio2_path}")
        return
    
    # Run analysis
    try:
        analyze_audio_files(
            audio1_path=audio1_path,
            audio2_path=audio2_path,
            output_path=args.output,
            show_plot=not args.no_display
        )
    except Exception as e:
        print(f"\n❌ Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
