from fastapi import APIRouter, Depends

from app.config import get_settings, Settings


router = APIRouter()


@router.get("/health")
async def healthcheck(settings: Settings = Depends(get_settings)):
    return {
        "health": "Healthy!",
        "environment": settings.environment,
        "testing": settings.testing,
    }
