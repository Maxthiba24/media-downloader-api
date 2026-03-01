import re
import os
import uuid
import aiofiles
from pathlib import Path
from typing import Optional, Tuple
from ..config import Config


def detect_platform(url: str) -> Optional[str]:
    """Détecte la plateforme à partir de l'URL"""
    for platform, patterns in Config.URL_PATTERNS.items():
        for pattern in patterns:
            if re.match(pattern, url):
                return platform
    return None


def generate_filename(title: str, ext: str) -> str:
    """Génère un nom de fichier unique"""
    clean_title = re.sub(r"[^\w\s-]", "", title)
    clean_title = re.sub(r"[-\s]+", "-", clean_title)
    unique_id = str(uuid.uuid4())[:8]
    return f"{clean_title}-{unique_id}.{ext}"


async def cleanup_old_files(max_age_hours: int = 24):
    """Nettoie les fichiers plus vieux que max_age_hours"""
    download_dir = Path(Config.DOWNLOAD_DIR)
    if not download_dir.exists():
        return

    import time

    current_time = time.time()

    for file_path in download_dir.glob("*"):
        if file_path.is_file():
            file_age = current_time - file_path.stat().st_mtime
            if file_age > max_age_hours * 3600:
                file_path.unlink()


def format_size(size_bytes: int) -> str:
    """Convertit la taille en format lisible"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

