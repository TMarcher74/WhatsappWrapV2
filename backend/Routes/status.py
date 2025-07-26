from fastapi import APIRouter, Request
from backend.constants import Tags

router = APIRouter(prefix="/status")

@router.get("/health", tags=[Tags.Status])
def health_check():
    return {"status": "ok"}

@router.get("/request-headers", tags=[Tags.Status])
def request_headers(request: Request):
    return request.headers