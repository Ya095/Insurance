from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import OperationalError
from fastapi import HTTPException

from .work_with_tariff import get_tariff_row


async def get_rate(
        cargo_type: str,
        request_date: str,
        session: AsyncSession
) -> tuple[float, bool]:
    """ Получение ставки для расчета стоимости. """

    is_other = False
    try:
        tariff_obj = await get_tariff_row(session, request_date, cargo_type)

        if tariff_obj is None:
            # Если указанный тариф не найден - считаем по тарифу "Other"
            is_other = True
            tariff_obj = await get_tariff_row(session, request_date, "Other")

        if tariff_obj is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "status": "error",
                    "details": "Tariff not found for specified cargo type and 'Other' (for this date)"
                }
            )

        return tariff_obj.rate, is_other

    except OperationalError as e:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "details": f"Database operation failed: {str(e)}"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "details": str(e)
            }
        )