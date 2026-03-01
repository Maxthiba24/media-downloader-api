from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any


class MediaFormat(BaseModel):
    format_id: str
    label: str
    ext: str
    filesize: Optional[int] = None


class PlaylistItem(BaseModel):
    id: str
    title: str
    thumbnail: Optional[str] = None
    duration: Optional[int] = None


class MediaInfoResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class DownloadRequest(BaseModel):
    url: HttpUrl
    format_id: str


class HealthResponse(BaseModel):
    status: str
    version: str
    supported: List[str]


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
