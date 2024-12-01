from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from insurance_app.api.api_v1.crud.work_with_cargo_type import (
    get_cargo_type_by_name,
    create_cargo_type,
)
from insurance_app.core.models import Tariff


async def write_json_data_to_db(data_json: dict, session: AsyncSession) -> None:
    """ Запись json данных в БД """

    data_json_gen = (part_json for part_json in data_json.items())

    try:
        for date_rates, list_rates in data_json_gen:
            for rate in list_rates:

                date_obj = date.fromisoformat(date_rates)
                rate["rate"] = float(rate["rate"])
                rate["cargo_type"] = rate["cargo_type"].capitalize()

                cargo_type_obj = await get_cargo_type_by_name(
                    session,
                    rate["cargo_type"],
                )

                if cargo_type_obj is None:
                    cargo_type_obj = await create_cargo_type(
                        session,
                        rate["cargo_type"]
                    )

                new_rate = Tariff(start_date=date_obj, cargo_type=cargo_type_obj.id, rate=rate["rate"])

                try:
                    session.add(new_rate)
                    await session.commit()
                except IntegrityError as e:
                    print(f"Duplicate [uniq_constraint]: {e}")

    except Exception as e:
        await session.rollback()
        print(f"Error writing data to database: {str(e)}")
