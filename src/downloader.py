import os
import requests
import logging
from yt_dlp import YoutubeDL
from urllib.parse import urlparse
from typing import Optional

logger = logging.getLogger(__name__)


class VideoDownloadError(Exception):
    """Raised when downloading a video fails."""


class VideoDownloader:
    """
    Downloads a public video (YouTube, Loom, direct MP4) to a local file.
    """

    def __init__(self, output_dir: str = "downloads", cookies_file: Optional[str] = None) -> None:
        self.output_dir = output_dir
        self.cookies_file = cookies_file
        os.makedirs(self.output_dir, exist_ok=True)

    def download(self, url: str, cookies_browser: Optional[str] = None) -> str:
        """
        Download from a direct MP4 link or via yt-dlp, return local filepath.

        Args:
            url: Video URL to download
            cookies_browser: Optional browser name to extract cookies from
                             (e.g., 'chrome', 'firefox', 'edge', 'safari', 'opera')
        """
        direct_path = self._try_direct_download(url)
        if direct_path:
            return direct_path

        return self._download_with_yt_dlp(url, cookies_browser)

    def _try_direct_download(self, url: str) -> Optional[str]:
        parsed = urlparse(url)
        ext = os.path.splitext(parsed.path)[1].lower()
        if ext not in {".mp4", ".mov", ".m4v"}:
            return None

        local_path = os.path.join(self.output_dir, os.path.basename(parsed.path))
        try:
            resp = requests.get(url, stream=True)
            resp.raise_for_status()
            with open(local_path, "wb") as f:
                for chunk in resp.iter_content(1024 * 1024):
                    f.write(chunk)
            logger.debug("Direct download saved to %s", local_path)
            return local_path

        except requests.RequestException as e:
            logger.warning("Direct download failed, falling back to yt-dlp: %s", e)
            return None

    def _download_with_yt_dlp(self, url: str, cookies_browser: Optional[str] = None) -> str:
        ydl_opts = {
            "outtmpl": os.path.join(self.output_dir, "%(id)s.%(ext)s"),
            "format": "mp4/bestvideo+bestaudio",
            "noplaylist": True,
        }

        # Add cookies if specified
        if self.cookies_file and os.path.exists(self.cookies_file):
            ydl_opts["cookiefile"] = self.cookies_file
            logger.info("Using cookies file: %s", self.cookies_file)
        elif cookies_browser:
            # Safari is not supported
            if cookies_browser.lower() == "safari":
                logger.warning("Safari cookies are not supported due to macOS security restrictions")
            else:
                try:
                    ydl_opts["cookiesfrombrowser"] = (cookies_browser, None, None, None)
                    logger.info("Using cookies from browser: %s", cookies_browser)
                except Exception as e:
                    logger.warning("Failed to get cookies from %s: %s", cookies_browser, e)

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                path = ydl.prepare_filename(info)
                logger.debug("yt-dlp download saved to %s", path)
                return path

        except Exception as e:
            error_msg = str(e)

            # Handle general bot verification errors
            if "Sign in to confirm" in error_msg or "bot" in error_msg:
                raise VideoDownloadError(
                    "YouTube verification required. Try one of these approaches:\n"
                    "1. Use a different video URL\n"
                    "2. Use Chrome or Firefox browser cookies (Safari is not supported)\n"
                    "3. Create a cookies.txt file manually (see README)\n"
                    "Error details: " + error_msg
                )
            else:
                logger.error("yt-dlp failed: %s", e)
                raise VideoDownloadError(f"Could not download video: {e}")
