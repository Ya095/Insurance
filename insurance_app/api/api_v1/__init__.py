from fastapi import APIRouter
from insurance_app.core.config import settings
from .upload_json import router as upload_json_router
from .count_price import router as count_price_router


# Подключение роутера(ов)
router = APIRouter(
    prefix=settings.api.v1.prefix
)

router.include_router(upload_json_router)
router.include_router(count_price_router)
