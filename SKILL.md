---
name: yt-dl-subtitle
description: "YouTube subtitle downloader — pytubefix-based CLI with smart language fallback. Outputs JSON with title, description, and subtitle content."
version: 0.3.0
repository: "https://github.com/JMVoid/yt-dl-subtitle-exec"
---

# yt-dl-subtitle — YouTube Subtitle Downloader

Downloads subtitles/transcripts from YouTube videos via pytubefix. Supports 35+ languages with automatic fallback.

## When to Use

When an AI agent needs to extract text content from a YouTube video — whether as a standalone tool or as Step 1 of a video summarization pipeline.

## Quick Start

```bash
# Using compiled binary (31MB standalone, no Python needed):
./dist/yt-dl-subtitle "https://www.youtube.com/watch?v=VIDEO_ID" -l zh

# Using Python directly:
python3 cli.py "https://www.youtube.com/watch?v=VIDEO_ID" -l zh
```

The URL is a **positional argument** (not `--url`). Language is `-l` or `--lang`.

## Output Format

Success:
```json
{
  "status": "success",
  "title": "Video Title",
  "description": "Video description text...",
  "content": "Full subtitle/transcript text..."
}
```

Failure (no subtitles available):
```json
{
  "status": "failure",
  "reason": "No captions available for this video",
  "title": "Video Title",
  "description": "..."
}
```

## Language Support

Any ISO 639-1 two-letter code: `en`, `zh`, `ja`, `ko`, `fr`, `de`, `es`, `pt`, `ru`, `ar`, `hi`, etc.

**Smart fallback**: If the requested language isn't available, the tool tries a 35-language priority list, then falls back to any available subtitle track.

## Proxy Configuration

If YouTube blocks direct access from your IP, set the `YT_DL_PROXY` environment variable:

```bash
export YT_DL_PROXY="http://username:password@proxy-ip:port"
```

Or via `.env` file in the project directory:
```
YT_DL_PROXY=http://your-proxy:port
```

## Requirements

- Python 3.11+
- Dependencies (auto-installed with `pip install .`): `pytubefix`, `python-dotenv`
- Or use the pre-built `dist/yt-dl-subtitle` binary (no Python required, 31MB)

## Project Structure

```
yt-dl-subtitle-exec/
├── cli.py                    # CLI entry point
├── youtube/
│   ├── yt_subtitle_dl.py     # Subtitle download logic
│   └── yt_metadata_dl.py     # Video metadata extraction
├── utils/
│   ├── constant.py           # Language codes, defaults
│   └── utils.py              # Shared utilities
├── dist/yt-dl-subtitle       # Pre-built standalone executable
└── pyproject.toml
```

## Error Handling for Agents

| Situation | Output | Agent Action |
|-----------|--------|-------------|
| Subtitles exist | `status: "success"` with content | Proceed with content |
| No subtitles | `status: "failure"`, reason explains why | Fall back to audio transcription (yt-whisper) |
| URL unreachable / private | Exception in stderr | Verify URL with user |
| pytubefix blocked | Bot detection error | Check proxy is set and working |

## Related

- **Next step if no subtitles**: yt-whisper (audio download + Deepgram transcription)
- **Orchestration**: youtube-tools skill defines the full pipeline
- **Home in Hermes**: `~/hermes/youtube-data/yt-dl-subtitle-exec/`
