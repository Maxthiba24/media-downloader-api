import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Téléchargements
    DOWNLOAD_DIR = "downloads"
    MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB

    # Rate limiting
    RATE_LIMIT = 10  # requêtes par minute

    # Plateformes supportées
    SUPPORTED_PLATFORMS = ["youtube", "spotify", "instagram", "tiktok", "pinterest"]

    # URLs patterns
    URL_PATTERNS = {
        "youtube": [
            r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=[\w-]+",
            r"(?:https?:\/\/)?(?:www\.)?youtu\.be\/[\w-]+",
            r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/playlist\?list=[\w-]+",
        ],
        "spotify": [
            r"(?:https?:\/\/)?(?:open\.)?spotify\.com\/track\/[\w]+",
            r"(?:https?:\/\/)?(?:open\.)?spotify\.com\/playlist\/[\w]+",
        ],
        "instagram": [
            r"(?:https?:\/\/)?(?:www\.)?instagram\.com\/p\/[\w-]+",
            r"(?:https?:\/\/)?(?:www\.)?instagram\.com\/reel\/[\w-]+",
            r"(?:https?:\/\/)?(?:www\.)?instagram\.com\/stories\/[\w\/]+",
        ],
        "tiktok": [
            r"(?:https?:\/\/)?(?:www\.)?tiktok\.com\/@[\w.]+\/video\/\d+",
            r"(?:https?:\/\/)?(?:vm\.)?tiktok\.com\/[\w]+",
        ],
        "pinterest": [
            r"(?:https?:\/\/)?(?:www\.)?pinterest\.com\/pin\/[\w-]+",
            r"(?:https?:\/\/)?(?:pin\.it\/[\w]+)",
        ],
    }

    # Formats disponibles
    FORMATS = {
        "mp4_hd": {
            "label": "MP4 HD (1080p)",
            "ext": "mp4",
            "quality": "1080",
            "type": "video",
        },
        "mp4_sd": {
            "label": "MP4 SD (480p)",
            "ext": "mp4",
            "quality": "480",
            "type": "video",
        },
        "mp3": {
            "label": "MP3 (320kbps)",
            "ext": "mp3",
            "quality": "320",
            "type": "audio",
        },
        "wav": {
            "label": "WAV (Lossless)",
            "ext": "wav",
            "quality": "lossless",
            "type": "audio",
        },
    }
