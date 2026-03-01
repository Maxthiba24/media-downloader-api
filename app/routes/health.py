from fastapi import APIRouter
from ..models.schemas import HealthResponse
from ..config import Config


router = APIRouter()


@router.get("/api/health", response_model=HealthResponse)
async def health_check():
    """
    Vérifie que l'API est opérationnelle
    """
    return HealthResponse(
        status="ok",
        version="1.0.0",
        supported=Config.SUPPORTED_PLATFORMS,
    )

