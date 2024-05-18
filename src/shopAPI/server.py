from fastapi import FastAPI
from fastapi.middleware import Middleware

from shopAPI.routers import api_router, status_router
from shopAPI.config import settings
from shopAPI.middlewares import SQLAlchemyMiddleware


def get_application():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url="/swagger",
        middleware=[Middleware(SQLAlchemyMiddleware)],
    )
    app.include_router(api_router, prefix="/api")
    app.include_router(status_router)
    return app


app = get_application()
