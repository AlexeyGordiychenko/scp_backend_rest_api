from contextlib import asynccontextmanager
from fastapi import FastAPI

from api import router as api_router
from core.config import settings
from db.session import engine
from db.utils import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables(engine)
    yield


def get_application():
    app = FastAPI(
        lifespan=lifespan,
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url="/swagger",
    )
    app.include_router(api_router, prefix="/api")
    return app


app = get_application()
