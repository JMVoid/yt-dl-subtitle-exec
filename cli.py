import argparse
import os
import asyncio
import json
import logging
from typing import Optional, Dict, Any

__version__ = "0.3.0"

import certifi
import ssl
import urllib.request

# Use certifi's CA bundle instead of system CA certificates.
# This ensures the bundled executable works on systems without
# up-to-date CA certificates (e.g. minimal Docker images).
_certifi_cafile = certifi.where()
_ssl_context = ssl.create_default_context(cafile=_certifi_cafile)
_https_handler = urllib.request.HTTPSHandler(context=_ssl_context)
_opener = urllib.request.build_opener(_https_handler)
urllib.request.install_opener(_opener)

# Set environment variables as a fallback for any library that reads them
os.environ['SSL_CERT_FILE'] = _certifi_cafile
os.environ['REQUESTS_CA_BUNDLE'] = _certifi_cafile

from youtube.yt_subtitle_dl import dl_caption_byId
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()


async def download_subtitle_with_id(
    url: str,
    target_lang: str = "en",
    proxy: Optional[str] = None,
    cookies: Optional[str] = None,
) -> Dict[str, Any]:
    """Core logic for downloading subtitles"""
    try:
        logging.info(f"Processing URL: {url}")

        # Call function to get metadata and subtitle content
        success, result = dl_caption_byId(url, target_lang, proxy, cookies)

        if success:
            # On success, merge status with metadata
            response = {"status": "success"}
            response.update(result)
            return response
        else:
            # On failure, return dictionary with reason
            return {
                "status": "failure",
                "reason": result,
            }

    except Exception as e:
        error_msg = f"Error processing URL {url}: {e}"
        logging.error(error_msg)
        return {"status": "failure", "reason": error_msg}


def main():
    """CLI entry point"""
    youtube_proxy = os.getenv("YT_DL_PROXY")
    
    parser = argparse.ArgumentParser(
        description='YouTube Subtitle Downloader Tool',
        usage='%(prog)s <url> [-l <lang>] [-c <cookies>]'
    )

    # Main arguments
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('-l', '--lang', default='en', help='Target language code (default: en)')
    parser.add_argument('-c', '--cookies', default=None,
                        help='Path to Netscape-format cookies file (e.g. from Chrome CDP)')
    parser.add_argument('-v', '--version', action='version',
                        version=f'%(prog)s {__version__}')

    args = parser.parse_args()

    # Log proxy usage status
    if youtube_proxy:
        logging.info("youtube download proxy was set and used")
    else:
        logging.info("youtube download proxy not set")

    if args.cookies:
        logging.info(f"Using cookies file: {args.cookies}")
        youtube_proxy = None  # cookies and proxy are mutually exclusive
        logging.info("Proxy disabled (cookies are used instead)")

    # Download subtitle
    result = asyncio.run(download_subtitle_with_id(args.url, args.lang, youtube_proxy, args.cookies))
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()