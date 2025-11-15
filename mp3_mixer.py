#!/usr/bin/env python3
"""
MP3 Album Mixer
A script to randomly select and concatenate MP3 files from an album
into a single output file of a specified duration.
"""

import os
import random
import argparse
from pathlib import Path
from pydub import AudioSegment


def find_mp3_files_shuffled(directory):
    """
    Recursively find all MP3 files in the given directory.
    
    Args:
        directory (str): Path to the directory to search
        
    Returns:
        list: Shuffled ist of paths to MP3 files
    """
    mp3_files = []
    directory_path = Path(directory)
    
    if not directory_path.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    # Recursively search for MP3 files
    for file_path in directory_path.rglob("*.mp3"):
        mp3_files.append(str(file_path))
    
    return random.sample(mp3_files, len(mp3_files))

def create_random_mix(mp3_files, target_length_minutes, output_file, crossfade_duration=5500):
    """
    Create a random mix of MP3 files to reach the target length with crossfades.
    
    Args:
        mp3_files (list): List of paths to MP3 files
        target_length_minutes (float): Target length in minutes
        output_file (str): Path to the output MP3 file
        crossfade_duration (int): Crossfade duration in milliseconds (default: 5500ms = 5.5s)
    """
    if not mp3_files:
        raise ValueError("No MP3 files found in the specified directory")
    
    target_length_ms = int(target_length_minutes * 60 * 1000)
    combined_audio = AudioSegment.empty()
    current_length_ms = 0
    
    print(f"\n{'='*60}")
    print(f"Creating random mix from {len(mp3_files)} available tracks")
    print(f"Target length: {target_length_minutes} minutes ({target_length_ms / 1000:.1f} seconds)")
    print(f"Crossfade duration: {crossfade_duration / 1000:.1f} seconds")
    print(f"{'='*60}\n")
    
    track_count = 0
    
    while current_length_ms < target_length_ms:
        # Randomly select a track
        selected_file = mp3_files[track_count]
        track_name = os.path.basename(selected_file)
        
        try:
            # Load the audio file
            audio_segment = AudioSegment.from_mp3(selected_file)
            segment_duration_ms = len(audio_segment)
            remaining_length_ms = target_length_ms - current_length_ms
            
            # Check if we need to trim the track
            if segment_duration_ms > remaining_length_ms:
                # Trim to exact remaining length
                audio_segment = audio_segment[:remaining_length_ms]
                segment_duration_ms = remaining_length_ms
                print(f"Track {track_count + 1}: {track_name}")
                print(f"  Duration: {segment_duration_ms / 1000:.2f}s (trimmed)")
            else:
                print(f"Track {track_count + 1}: {track_name}")
                print(f"  Duration: {segment_duration_ms / 1000:.2f}s")
            
            # Add to the combined audio with crossfade
            if track_count == 0:
                # First track - no crossfade
                combined_audio = audio_segment
            else:
                # Apply crossfade for subsequent tracks
                combined_audio = combined_audio.append(audio_segment, crossfade=crossfade_duration)
            
            current_length_ms += segment_duration_ms
            track_count += 1
            
            print(f"  Progress: {current_length_ms / 1000:.2f}s / {target_length_ms / 1000:.1f}s "
                  f"({(current_length_ms / target_length_ms) * 100:.1f}%)\n")
            
        except Exception as e:
            print(f"Error processing '{track_name}': {e}")
            print(f"Skipping this track and continuing...\n")
            # Remove problematic file from the list to avoid retrying
            mp3_files.remove(selected_file)
            if not mp3_files:
                raise ValueError("No more valid MP3 files available to process")
            continue
    
    # Export the final mix
    actual_duration_ms = len(combined_audio)
    print(f"{'='*60}")
    print(f"Mix complete! Total tracks used: {track_count}")
    print(f"Target duration: {current_length_ms / 1000 / 60:.2f} minutes ({current_length_ms / 1000:.2f} seconds)")
    print(f"Actual duration (with crossfades): {actual_duration_ms / 1000 / 60:.2f} minutes ({actual_duration_ms / 1000:.2f} seconds)")
    print(f"Exporting to: {output_file}")
    print(f"{'='*60}\n")
    
    try:
        combined_audio.export(output_file, format="mp3")
        print(f"✓ Successfully created: {output_file}\n")
    except Exception as e:
        raise RuntimeError(f"Failed to export final mix: {e}")


def main():
    """Main function to handle command-line interface."""
    parser = argparse.ArgumentParser(
        description="Create a random mix of MP3 files from an album",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --length 60                    # Create a 60-minute mix
  %(prog)s --length 30 --output my_mix.mp3  # Custom output filename
  %(prog)s --length 45 --tracks ./music    # Specify custom tracks directory
        """
    )
    
    parser.add_argument(
        "--length",
        type=float,
        required=True,
        help="Target length of the final mix in minutes"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="random_mix.mp3",
        help="Output filename (default: random_mix.mp3)"
    )
    
    parser.add_argument(
        "--tracks",
        type=str,
        default="tracks",
        help="Directory containing MP3 files (default: tracks)"
    )
    
    parser.add_argument(
        "--crossfade",
        type=int,
        default=random.choice([5000, 6000]),
        help="Crossfade duration in milliseconds (default: 5500ms)"
    )
    
    args = parser.parse_args()
    
    # Validate input
    if args.length <= 0:
        parser.error("Length must be a positive number")
    
    try:
        # Find all MP3 files
        print(f"\nSearching for MP3 files in: {args.tracks}")
        mp3_files = find_mp3_files_shuffled(args.tracks)
        
        if not mp3_files:
            print(f"\n✗ No MP3 files found in '{args.tracks}'")
            print("Please check the directory path and try again.\n")
            return 1
        
        # Create the random mix
        create_random_mix(mp3_files, args.length, args.output, args.crossfade)
        return 0
        
    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}\n")
        return 1
    except ValueError as e:
        print(f"\n✗ Error: {e}\n")
        return 1
    except RuntimeError as e:
        print(f"\n✗ Error: {e}\n")
        return 1
    except KeyboardInterrupt:
        print("\n\n✗ Process interrupted by user\n")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}\n")
        return 1


if __name__ == "__main__":
    exit(main())