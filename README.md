# YT Subtitle Downloader (yt-dl-subtitle)

This project provides a simple CLI tool to download transcripts/subtitles from YouTube videos. It focuses on efficiency and ease of use, with the ability to compile into a standalone executable.

## Features

- **Subtitle Download**: Downloads video transcripts in specified languages.
- **Smart Fallback**: Automatically tries alternative subtitle tracks if the requested language is unavailable.
- **Metadata Extraction**: Retrieves video title and description along with subtitles.
- **Standalone Executable**: Can be compiled into a single binary for use without a Python environment.

## Installation

### From Source

Ensure you have Python 3.11+ installed.

```bash
pip install .
```

### Build Standalone Executable

To build the `yt-dl-subtitle` executable for your current platform:

```bash
# Install build dependencies
pip install pyinstaller

# Build the executable
pyinstaller yt-dl-subtitle.spec --clean
```

After compilation, the executable will be located at:
- `dist/yt-dl-subtitle` (Linux/macOS)
- `dist/yt-dl-subtitle.exe` (Windows)

## Usage

### Command-line Usage

Run the compiled executable or the python script directly.

#### Download Subtitles

```bash
./yt-dl-subtitle subtitle --url <URL> [--lang <LANG_CODE>]
```

**Arguments:**
- `--url` (required): The full URL of the YouTube video.
- `--lang` (optional): Two-letter language code (e.g., `en`, `zh`, `es`). Defaults to `en`.

**Example:**
```bash
./yt-dl-subtitle subtitle --url "https://www.youtube.com/watch?v=xxxxx" --lang zh
```

### Supported Language Codes

Most common language codes are supported, including:
`en`, `zh`, `es`, `hi`, `ar`, `pt`, `ru`, `ja`, `fr`, `de`, `ko`, `it`, `tr`, `nl`, `pl`, `vi`, `th`, `id`, `ms`, `fa`, `ur`, `bn`, `he`, `fil`, `sv`, `el`, `cs`, `hu`, `da`, `no`, `fi`, `ro`, `uk`, `sr`.

## Configuration

### Proxy Settings

If you encounter YouTube's bot detection, you can configure a proxy via environment variables or a `.env` file:

```env
PROXIES=http://your-proxy-server:port
# Or with authentication
# PROXIES=http://username:password@ip:port
```

## Development

The project uses `pytubefix` for interacting with YouTube.

### Project Structure

- `cli.py`: Main entry point for the CLI tool.
- `youtube/`: Contains logic for YouTube interaction and subtitle extraction.
- `utils/`: Common utilities and constants.
- `yt-dl-subtitle.spec`: PyInstaller configuration file.
