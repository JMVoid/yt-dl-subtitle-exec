import argparse
import os
import asyncio
import json
import logging
from typing import Optional, Dict, Any

from pytubefix import YouTube
from youtube.yt_subtitle_dl import dl_caption_byId
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# Get environment variables
youtube_proxy: Optional[str] = os.getenv("YT_DL_PROXY")

async def download_subtitle_with_id(
    url: str, 
    target_lang: str = "en",
    proxy: Optional[str] = None
) -> Dict[str, Any]:
    """Core logic for downloading subtitles"""
    try:
        logging.info(f"Processing URL: {url}")
        # Configure proxies
        proxy_dict = None
        if proxy:
            if proxy.startswith('http://') or proxy.startswith('https://'):
                proxy_dict = {'http': proxy, 'https': proxy}
            else:
                proxy_dict = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
        
        yt = YouTube(url, proxies=proxy_dict)
        
        # Call function to get metadata and subtitle content
        success, result = dl_caption_byId(yt, target_lang)
        
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
                "title": yt.title,
                "description": yt.description,
            }

    except Exception as e:
        error_msg = f"Error processing URL {url}: {e}"
        logging.error(error_msg)
        return {"status": "failure", "reason": error_msg}

def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description='YouTube Subtitle Downloader Tool',
        usage='%(prog)s <url> [-l <lang>]'
    )
    
    # Main arguments
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('-l', '--lang', default='en', help='Target language code (default: en)')
    
    args = parser.parse_args()
    
    # Log proxy usage status
    if youtube_proxy:
        logging.info("youtube download proxy was setted and used")
    else:
        logging.info("youtube download proxy not be setted")
    
    # Download subtitle
    result = asyncio.run(download_subtitle_with_id(args.url, args.lang, youtube_proxy))
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
