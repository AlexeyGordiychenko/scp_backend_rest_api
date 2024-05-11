from fastapi import FastAPI
from fastapi.middleware import Middleware

from shopAPI.api import router as api_router
from shopAPI.core.config import settings
from shopAPI.core.fastapi.middlewares.sqlalchemy import SQLAlchemyMiddleware


def get_application():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url="/swagger",
        middleware=[Middleware(SQLAlchemyMiddleware)],
    )
    app.include_router(api_router, prefix="/api")
    return app


app = get_application()
