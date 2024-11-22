import json

from pydantic import ValidationError
from fastapi import HTTPException, UploadFile

from insurance_app.core.schemas.json_data import FullJsonSchema


async def validate_json(file: UploadFile) -> dict:
    """ Валидация значений .json файла """

    if not file.size:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "details": "JSON file is empty"
            }
        )

    if file.filename.endswith(".json"):
        try:
            content = await file.read()
            json_data = json.loads(content.decode())
            FullJsonSchema.model_validate(json_data)
            return json_data

        except ValidationError as e:
            raise HTTPException(
                status_code=400,
                detail={
                    "status": "error",
                    "details": str(e)
                }
            )
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=400,
                detail={
                    "status": "error",
                    "details": str(e)
                }
            )
    else:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "details": "Wrong file type! Only .json files are allowed."
            }
        )
