from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal
from insurance_app.api.api_v1.crud.get_count_rate import get_rate
from insurance_app.core.schemas.tariff import InsuranceRequest


async def count_result_price(
        request: InsuranceRequest,
        session: AsyncSession
) -> tuple[Decimal, bool]:
    """ Получение ставки для расчета стоимости """

    request.cargo_type = request.cargo_type.capitalize()

    rate, is_other = await get_rate(request.cargo_type, request.transfer_date, session)
    insurance_cost = Decimal(request.declared_price) * Decimal(rate)

    return insurance_cost.quantize(Decimal('0.0005')).normalize(), is_other
