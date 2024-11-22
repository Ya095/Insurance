from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

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

                new_rate = Tariff(start_date=date_obj, cargo_type=rate["cargo_type"], rate=rate["rate"])
                try:
                    session.add(new_rate)
                    await session.commit()
                except IntegrityError as e:
                    print(f"Duplicate [uniq_constraint]: {e}")
    except Exception as e:
        await session.rollback()
        print(f"Error writing data to database: {str(e)}")
