from fastapi import APIRouter

from app.api.routes.v1 import router as v1_router

router = APIRouter()
router.include_router(v1_router)
