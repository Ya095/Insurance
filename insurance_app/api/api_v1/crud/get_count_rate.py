from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import OperationalError
from fastapi import HTTPException
from sqlalchemy import select

from insurance_app.core.models import Tariff


async def get_rate(
        cargo_type: str,
        request_date: str,
        session: AsyncSession
) -> tuple[float, bool]:
    """ Получение ставки для расчета стоимости. """

    is_other = False
    try:
        request_date = date.fromisoformat(request_date)
        stmt = (
            select(Tariff.rate)
            .where(Tariff.cargo_type == cargo_type, Tariff.start_date <= request_date)
            .order_by(Tariff.start_date.desc())
            .limit(1)
        )
        result = await session.execute(stmt)
        rate = result.scalar_one_or_none()

        if rate is None:
            # Если нет, то ищем тариф по тарифу "Other"
            is_other = True
            stmt = (
                select(Tariff.rate)
                .where(Tariff.cargo_type == "Other", Tariff.start_date <= request_date)
                .order_by(Tariff.start_date.desc())
                .limit(1)
            )
            result = await session.execute(stmt)
            rate = result.scalar_one_or_none()

        if rate is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "status": "error",
                    "details": "Tariff not found for specified cargo type and 'Other' (for this date)"
                }
            )

        return rate, is_other

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