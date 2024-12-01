from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from insurance_app.core.models import CargoType


async def get_cargo_type_by_name(session: AsyncSession, cargo_type_name: str) -> CargoType | None:
    """ Получение конкретной записи о типе груза """

    stmt = (
        select(CargoType)
        .where(CargoType.name == cargo_type_name)
    )
    try:
        result = await session.execute(stmt)
        cargo_type = result.scalar_one_or_none()

        return cargo_type

    except Exception as e:
        print(f"Error getting cargo type from database: {str(e)}")


async def create_cargo_type(session: AsyncSession, cargo_type_name: str) -> CargoType:
    """ Добавление записи о типе груза """

    cargo_type_obj = CargoType(name=cargo_type_name)

    try:
        session.add(cargo_type_obj)
        await session.commit()
        await session.refresh(cargo_type_obj)

        return cargo_type_obj

    except IntegrityError as e:
        print(f"Duplicate cargo_type: {e}")

    except Exception as e:
        await session.rollback()
        print(f"Error writing data to database: {str(e)}")
