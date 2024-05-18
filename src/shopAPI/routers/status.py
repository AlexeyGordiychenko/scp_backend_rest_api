from fastapi import APIRouter

from shopAPI.schemas import ApiStatus
from shopAPI.config import settings

status_router = APIRouter(
    tags=["Status"],
)


@status_router.get("/")
async def status() -> ApiStatus:
    return ApiStatus(
        name=settings.PROJECT_NAME,
        version=settings.VERSION,
        status="OK",
        message="Visit /swagger for more information.",
    )
