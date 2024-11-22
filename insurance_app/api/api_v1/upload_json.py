from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from insurance_app.core.config import settings
from insurance_app.core.models import db_helper
from .utils.json_validation import validate_json
from .crud.write_json_to_db import write_json_data_to_db

router = APIRouter(
    prefix=settings.api.v1.upload_data,
    tags=["Upload tariffs"],
)


@router.post("")
async def create_upload_file(
        session: AsyncSession = Depends(db_helper.session_getter),
        file: UploadFile = File(...)
):
    data_json = await validate_json(file)
    await write_json_data_to_db(data_json, session)

    return {
        "status": "success",
        "message": "File uploaded and processed successfully",
    }
