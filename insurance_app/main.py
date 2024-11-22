import uvicorn
from fastapi import FastAPI
from insurance_app.api import router as api_router
from insurance_app.core.config import settings
from contextlib import asynccontextmanager
from insurance_app.core.models.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # start up
    yield
    # shut down
    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan
)
main_app.include_router(
    api_router
)

if __name__ == "__main__":
    uvicorn.run("main:main_app", host=settings.run.host, port=settings.run.port, reload=True)
