from fastapi import APIRouter
from insurance_app.core.config import settings
from .api_v1 import router as api_router_v1


# создание роутеров для всех версий апи

router = APIRouter(
    prefix=settings.api.prefix
)

router.include_router(api_router_v1)
