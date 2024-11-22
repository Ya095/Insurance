from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from insurance_app.core.config import settings
from insurance_app.core.models import db_helper
from insurance_app.core.schemas.tariff import InsuranceRequest, ResponsePrice
from insurance_app.api.api_v1.utils.counting_price import count_result_price


router = APIRouter(
    prefix=settings.api.v1.count_price,
    tags=["Count price"],
)


@router.post("", response_model=ResponsePrice)
async def count_price(
        request: InsuranceRequest,
        session: AsyncSession = Depends(db_helper.session_getter),
):

    new_price, is_other = await count_result_price(
        request,
        session
    )

    tariff = request.cargo_type if not is_other else "Other"

    return ResponsePrice(
        status="success",
        tariff=tariff,
        insurance_cost=new_price,
    )