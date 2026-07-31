# YT Subtitle Downloader (yt-dl-subtitle)

[![Build](https://github.com/JMVoid/yt-dl-subtitle-exec/actions/workflows/build.yml/badge.svg)](https://github.com/JMVoid/yt-dl-subtitle-exec/actions/workflows/build.yml)
[![Release](https://img.shields.io/github/v/release/JMVoid/yt-dl-subtitle-exec?label=Release)](https://github.com/JMVoid/yt-dl-subtitle-exec/releases/latest)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)


This project provides a simple CLI tool to download transcripts/subtitles from YouTube videos. It focuses on efficiency and ease of use, with the ability to compile into a standalone executable.

## Features

- **Subtitle Download**: Downloads video transcripts in specified languages.
- **Smart Fallback**: Automatically tries alternative subtitle tracks if the requested language is unavailable.
- **Metadata Extraction**: Retrieves video title and description along with subtitles.
- **Standalone Executable**: Can be compiled into a single binary for use without a Python environment.

## Installation

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (Python package manager)

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install Dependencies

```bash
cd yt-dl-subtitle-exec
uv sync
```

This creates a `.venv` virtual environment managed by uv with all dependencies (`yt-dlp`, `python-dotenv`, `certifi`).

### Run from Source (without compiling)

```bash
uv run python cli.py "URL" -l zh
```

### Build Standalone Executable

To build the `yt-dl-subtitle` binary for your current platform:

```bash
uv run pyinstaller yt-dl-subtitle.spec --clean
```

After compilation, the executable will be located at:
- `dist/yt-dl-subtitle` (Linux/macOS)
- `dist/yt-dl-subtitle.exe` (Windows)

⚠️ **After modifying source code, you must recompile for the binary to reflect changes.**

## Usage

### Command-line Usage

```bash
yt-dl-subtitle <URL> [-l <LANG>] [-v]
```

**Arguments:**

| Argument | Required | Default | Description |
|----------|:--------:|---------|-------------|
| `URL` | ✅ | — | YouTube video URL (positional) |
| `-l`, `--lang` | ❌ | `en` | Target language code (e.g., `zh`, `ja`, `ko`) |
| `-c`, `--cookies` | ❌ | — | Path to Netscape-format cookies file (e.g. from Chrome CDP extraction) |
| `-o`, `--output` | ❌ | — | Output file path; if not specified, output is written to stdout |
| `-v`, `--version` | ❌ | — | Show version number |

**Examples:**
```bash
# Download English subtitles (default)
./yt-dl-subtitle "https://www.youtube.com/watch?v=xxxxx"

# Download Chinese subtitles
./yt-dl-subtitle "https://www.youtube.com/watch?v=xxxxx" -l zh

# Download Japanese subtitles with fallback
./yt-dl-subtitle "https://www.youtube.com/watch?v=xxxxx" -l ja

# Use Chrome CDP cookies for authenticated subtitle access
./yt-dl-subtitle "https://www.youtube.com/watch?v=xxxxx" -l zh -c /tmp/youtube_cookies.txt

# Save output to a file
./yt-dl-subtitle "https://www.youtube.com/watch?v=xxxxx" -l en -o result.json
```

### Smart Language Fallback

If the requested language is unavailable, the tool automatically falls back through a **35-language priority list** in this order:

`en` → `zh` → `es` → `hi` → `ar` → `pt` → `ru` → `ja` → `fr` → `de` → `ko` → `it` → `tr` → `nl` → `pl` → `vi` → `th` → `id` → `ms` → `fa` → `ur` → `bn` → `he` → `fil` → `sv` → `el` → `cs` → `hu` → `da` → `no` → `fi` → `ro` → `uk` → `sr`

If none of the prioritized languages are available, any available subtitle will be used as a last resort.

### Output Format

Returns JSON to stdout by default, or to a file when `-o` is specified:

```json
{
  "status": "success",
  "title": "Video Title",
  "description": "Video Description",
  "content": "Subtitle text..."
}
```

On failure:
```json
{
  "status": "failure",
  "reason": "Error message..."
}
```

## Configuration

### Proxy Settings

If you encounter YouTube's bot detection, configure a proxy via the `YT_DL_PROXY` environment variable (reads from `.env` file or shell environment):

```env
YT_DL_PROXY=http://your-proxy-server:port
# Or with authentication:
# YT_DL_PROXY=http://username:password@ip:port
```

## Development

The project uses `yt-dlp` for interacting with YouTube. The compiled binary bundles `certifi` for TLS certificate verification on systems without up-to-date CA certificates.

### Project Structure

- `cli.py`: Main entry point for the CLI tool.
- `youtube/`: Contains logic for YouTube interaction and subtitle extraction.
- `utils/`: Common utilities and constants.
- `yt-dl-subtitle.spec`: PyInstaller configuration file.
