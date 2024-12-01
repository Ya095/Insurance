from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import aliased
from sqlalchemy.exc import IntegrityError, OperationalError
from fastapi import HTTPException

from insurance_app.core.models import Tariff, CargoType


async def get_tariff_row(
        session: AsyncSession,
        request_date: str,
        cargo_type: str
) -> Tariff | None:
    """ Получение нужной строки по тарифу """

    try:
        ct = aliased(CargoType)
        t = aliased(Tariff)

        request_date = date.fromisoformat(request_date)

        stmt = (
            select(t)
            .join(ct, ct.id == t.cargo_type)
            .where(ct.name == cargo_type, t.start_date <= request_date)
            .order_by(t.start_date.desc())
            .limit(1)
        )
        result = await session.execute(stmt)
        tariff = result.scalar_one_or_none()

        return tariff

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
