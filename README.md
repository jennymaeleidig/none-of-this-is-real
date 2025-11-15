# NONE OF THIS IS REAL - MP3 Mixer

A Python script that randomly selects and concatenates MP3 files from an album directory into a single output file of a specified duration. Used for creating randomized mixes of a preset length for use on the radio or other streaming platforms.

SUPPORT THE ARTIST AND PURCHASE THE TUNES HERE - https://djrozwell.bandcamp.com/album/none-of-this-is-real

Instructions:
```
Greetings, mortal. Thou hast stumbled upon a mysterious adventure of wonder and art magic. This journey will be different each time thou listen
To listen to this whole album properly, thou must play on shuffle mode in thy media player of choice with a crossfade of five or six seconds between tracks, or thou shalt be smited
```

## DISCLAIMER:

This script is AI generated and may require adjustments to fit your specific needs. Use at your own discretion.

## Prerequisites

### 1. Python 3.6+

Make sure you have Python 3.6 or higher installed:

```bash
python3 --version
```

### 2. FFmpeg

The script requires FFmpeg to process audio files. Install it based on your operating system:

**macOS:**

```bash
brew install ffmpeg
```

### 3. Python Dependencies

This project uses pipenv for dependency management. Install pipenv if you don't have it:

```bash
pip install pipenv
```

Then install the project dependencies:

```bash
pipenv install
```

## Installation

1. Clone or download this repository
2. Install the prerequisites (see above)
3. You're ready to go!

## Usage

### Basic Usage

Create a 60-minute random mix from your tracks:

```bash
pipenv run python mp3_mixer.py --length 60
```

### Custom Output Filename

Specify a custom output filename:

```bash
pipenv run python mp3_mixer.py --length 30 --output "my_awesome_mix.mp3"
```

### Custom Tracks Directory

Use a different directory instead of the default `tracks`:

```bash
pipenv run python mp3_mixer.py --length 45 --tracks /path/to/your/music
```

### Custom Crossfade Duration

Adjust the crossfade duration between tracks (in milliseconds):

```bash
pipenv run python mp3_mixer.py --length 60 --crossfade 3000
```

### Complete Example

```bash
pipenv run python mp3_mixer.py --length 90 --output "road_trip_mix.mp3" --tracks ./tracks --crossfade 5000
```

## Command-Line Options

| Option        | Required | Default                 | Description                                       |
| ------------- | -------- | ----------------------- | ------------------------------------------------- |
| `--length`    | Yes      | -                       | Target length of the final mix in minutes         |
| `--output`    | No       | `random_mix.mp3`        | Output filename for the generated mix             |
| `--tracks`    | No       | `tracks`                | Directory containing MP3 files to mix             |
| `--crossfade` | No       | `5000 or 6000 (random)` | Crossfade duration between tracks in milliseconds |

## Project Structure

```
.
├── mp3_mixer.py          # Main script
.
.
.
└── tracks/               # Your MP3 files (organized in subdirectories)
    ├── Album 1/
    ├── Album 2/
    └── Album 3/
```

## About

- **Album Design**: This script was designed for albums designed to be played in random order (like DJ Rozwell's "NONE OF THIS IS REAL" series)
- **Multiple Runs**: Each run creates a unique random mix - run it multiple times for different variations!
- **Target Length**: The script will trim the final track to meet the exact target duration
