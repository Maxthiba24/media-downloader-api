from fastapi import APIRouter, Query, HTTPException
from ..services.extractor import MediaExtractor
from ..services.utils import detect_platform
from ..models.schemas import MediaInfoResponse
from ..config import Config


router = APIRouter()
extractor = MediaExtractor()


@router.get("/api/info", response_model=MediaInfoResponse)
async def get_info(url: str = Query(..., description="URL du média à analyser")):
    """
    Récupère les métadonnées d'un lien média
    """
    try:
        platform = detect_platform(url)
        if not platform:
            return MediaInfoResponse(
                success=False,
                error="URL non supportée. Plateformes supportées: "
                + ", ".join(Config.SUPPORTED_PLATFORMS),
            )

        info = await extractor.extract_info(url)
        info["source"] = platform

        return MediaInfoResponse(success=True, data=info)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

