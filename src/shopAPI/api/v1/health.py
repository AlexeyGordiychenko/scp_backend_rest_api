from fastapi import APIRouter

from shopAPI.app.schemas.extras.health import Health
from shopAPI.core.config import settings

health_router = APIRouter()
router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("/")
async def health() -> Health:
    return Health(
        name=settings.PROJECT_NAME,
        version=settings.VERSION,
        status="OK",
        message="Visit /swagger for more information.",
    )
