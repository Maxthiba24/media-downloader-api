import yt_dlp
import asyncio
from typing import Dict, Any, Optional, List
from pathlib import Path
from .utils import generate_filename, detect_platform
from .spotify import SpotifyService
from ..config import Config


class MediaExtractor:
    """Service principal pour extraire les médias"""

    def __init__(self):
        self.ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": False,
        }

    async def extract_info(self, url: str) -> Dict[str, Any]:
        """Extrait les métadonnées d'une URL"""
        platform = detect_platform(url)

        if platform == "spotify":
            return await SpotifyService.extract_info(url)

        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = await asyncio.to_thread(
                    ydl.extract_info, url, download=False
                )
                return self._format_info(info, platform)
        except Exception as e:
            raise Exception(f"Erreur d'extraction: {str(e)}")

    def _format_info(self, info: Dict, platform: str) -> Dict:
        """Formate les infos extraites"""
        is_playlist = "entries" in info

        if is_playlist:
            return {
                "id": info.get("id", ""),
                "title": info.get("title", "Playlist"),
                "source": platform,
                "type": "playlist",
                "author": info.get("uploader"),
                "thumbnail": info.get("thumbnail"),
                "playlist_items": [
                    {
                        "id": entry.get("id", f"item_{i}"),
                        "title": entry.get("title", ""),
                        "thumbnail": entry.get("thumbnail"),
                        "duration": entry.get("duration"),
                    }
                    for i, entry in enumerate(info.get("entries", []))[:50]
                ],
            }
        else:
            formats = self._extract_formats(info)

            return {
                "id": info.get("id", ""),
                "title": info.get("title", ""),
                "thumbnail": info.get("thumbnail"),
                "duration": info.get("duration"),
                "source": platform,
                "type": "video"
                if info.get("ext") in ["mp4", "webm"]
                else "audio",
                "author": info.get("uploader"),
                "formats": formats,
            }

    def _extract_formats(self, info: Dict) -> List[Dict]:
        """Extrait les formats disponibles"""
        formats: List[Dict[str, Any]] = []
        available_formats = info.get("formats", [])

        video_formats = [
            f for f in available_formats if f.get("vcodec") != "none"
        ]
        video_formats.sort(
            key=lambda x: x.get("height", 0), reverse=True
        )

        if video_formats:
            best = video_formats[0]
            formats.append(
                {
                    "format_id": "mp4_hd",
                    "label": "MP4 HD (1080p)",
                    "ext": "mp4",
                    "filesize": best.get("filesize")
                    or best.get("filesize_approx"),
                }
            )

        if len(video_formats) > 1:
            sd = video_formats[-1]
            formats.append(
                {
                    "format_id": "mp4_sd",
                    "label": "MP4 SD (480p)",
                    "ext": "mp4",
                    "filesize": sd.get("filesize")
                    or sd.get("filesize_approx"),
                }
            )

        formats.append(
            {
                "format_id": "mp3",
                "label": "MP3 (320kbps)",
                "ext": "mp3",
                "filesize": None,
            }
        )

        formats.append(
            {
                "format_id": "wav",
                "label": "WAV (Lossless)",
                "ext": "wav",
                "filesize": None,
            }
        )

        return formats

    async def download(self, url: str, format_id: str, output_dir: Path) -> str:
        """Télécharge un média"""
        platform = detect_platform(url)

        if platform == "spotify":
            return await SpotifyService.download(url, output_dir)

        ydl_opts = self._get_download_options(format_id, output_dir)

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = await asyncio.to_thread(
                    ydl.extract_info, url, download=True
                )

                if "entries" in info:
                    info = info["entries"][0]

                filename = ydl.prepare_filename(info)

                if format_id in ["mp3", "wav"]:
                    filename = Path(filename).with_suffix(f".{format_id}")

                return str(filename)
        except Exception as e:
            raise Exception(f"Erreur téléchargement: {str(e)}")

    def _get_download_options(self, format_id: str, output_dir: Path) -> Dict:
        """Retourne les options yt-dlp selon le format"""
        base_opts: Dict[str, Any] = {
            "quiet": True,
            "no_warnings": True,
            "outtmpl": str(output_dir / "%(title)s.%(ext)s"),
        }

        if format_id == "mp4_hd":
            base_opts.update(
                {
                    "format": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]",
                    "merge_output_format": "mp4",
                }
            )
        elif format_id == "mp4_sd":
            base_opts.update(
                {
                    "format": "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]",
                    "merge_output_format": "mp4",
                }
            )
        elif format_id == "mp3":
            base_opts.update(
                {
                    "format": "bestaudio/best",
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "320",
                        }
                    ],
                }
            )
        elif format_id == "wav":
            base_opts.update(
                {
                    "format": "bestaudio/best",
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "wav",
                        }
                    ],
                }
            )

        return base_opts

