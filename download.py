from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pathlib import Path
import os
from ..services.extractor import MediaExtractor
from ..services.utils import cleanup_old_files
from ..models.schemas import DownloadRequest
from ..config import Config


router = APIRouter()
extractor = MediaExtractor()


@router.post("/api/download")
async def download_media(
    request: DownloadRequest, background_tasks: BackgroundTasks
):
    """
    Télécharge un média au format demandé
    """
    try:
        download_dir = Path(Config.DOWNLOAD_DIR)
        download_dir.mkdir(exist_ok=True)

        background_tasks.add_task(cleanup_old_files)

        filepath = await extractor.download(
            str(request.url), request.format_id, download_dir
        )

        if not os.path.exists(filepath):
            raise HTTPException(
                status_code=500,
                detail="Fichier non trouvé après téléchargement",
            )

        filename = os.path.basename(filepath)
        ext = os.path.splitext(filepath)[1].lower()
        media_type = "video/mp4" if ext == ".mp4" else "audio/mpeg"

        def _cleanup(path: str):
            try:
                os.unlink(path)
            except OSError:
                pass

        background_tasks.add_task(_cleanup, filepath)

        return FileResponse(
            path=filepath, media_type=media_type, filename=filename
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

