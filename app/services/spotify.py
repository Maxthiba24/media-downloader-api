import asyncio
import json
from typing import Dict, Any, Optional
import subprocess
from pathlib import Path


class SpotifyService:
    """Service pour gérer les téléchargements Spotify"""

    @staticmethod
    async def extract_info(url: str) -> Dict[str, Any]:
        """Extrait les infos d'un lien Spotify"""
        try:
            cmd = ["spotdl", "info", url, "--save-file", "-"]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                raise Exception(f"Spotify error: {stderr.decode()}")

            info = json.loads(stdout)

            if "tracks" in info:  # Playlist
                return {
                    "id": info.get("id", ""),
                    "title": info.get("name", ""),
                    "source": "spotify",
                    "type": "playlist",
                    "author": info.get("owner", {}).get("display_name"),
                    "thumbnail": info.get("cover_url"),
                    "playlist_items": [
                        {
                            "id": track.get("song_id", f"track_{i}"),
                            "title": track.get("name", ""),
                            "thumbnail": track.get("cover_url"),
                            "duration": track.get("duration"),
                        }
                        for i, track in enumerate(info.get("tracks", []))
                    ],
                }
            else:  # Track unique
                return {
                    "id": info.get("song_id", ""),
                    "title": info.get("name", ""),
                    "source": "spotify",
                    "type": "audio",
                    "author": info.get("artist", ""),
                    "thumbnail": info.get("cover_url"),
                    "duration": info.get("duration"),
                }
        except Exception as e:
            raise Exception(f"Erreur Spotify: {str(e)}")

    @staticmethod
    async def download(url: str, output_dir: Path) -> str:
        """Télécharge un morceau Spotify"""
        try:
            cmd = [
                "spotdl",
                url,
                "--output",
                str(output_dir / "{title}.{output-ext}"),
                "--format",
                "mp3",
                "--bitrate",
                "320k",
            ]

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await process.communicate()

            files = list(output_dir.glob("*.mp3"))
            if not files:
                raise Exception("Aucun fichier trouvé")

            return str(max(files, key=lambda f: f.stat().st_mtime))
        except Exception as e:
            raise Exception(f"Erreur téléchargement Spotify: {str(e)}")

