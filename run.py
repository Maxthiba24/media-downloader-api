import uvicorn
from pathlib import Path


if __name__ == "__main__":
    Path("downloads").mkdir(exist_ok=True)

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )

