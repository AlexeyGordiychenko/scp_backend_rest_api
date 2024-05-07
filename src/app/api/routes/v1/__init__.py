from importlib import import_module

from fastapi import APIRouter

router = APIRouter(prefix="/v1")
routes = ("client",)
for module_name in routes:
    api_module = import_module(f"app.api.routes.v1.{module_name}")
    api_module_router = api_module.router
    router.include_router(api_module_router)
