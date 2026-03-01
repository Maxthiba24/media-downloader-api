from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .routes import info, download, health
from .config import Config


app = FastAPI(
    title="Media Downloader API",
    description=(
        "API pour télécharger des médias depuis YouTube, "
        "Spotify, Instagram, TikTok et Pinterest"
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(info.router)
app.include_router(download.router)
app.include_router(health.router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": "Erreur interne du serveur"},
    )


@app.on_event("startup")
async def startup_event():
    from pathlib import Path

    download_dir = Path(Config.DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    print("✅ API démarrée sur http://localhost:8000")
    print(f"📁 Dossier de téléchargement: {download_dir.absolute()}")
    print(
        "🎯 Plateformes supportées: "
        + ", ".join(Config.SUPPORTED_PLATFORMS)
    )

