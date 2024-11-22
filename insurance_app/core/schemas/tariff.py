from pydantic import BaseModel, field_validator, Field
from datetime import date
from decimal import Decimal


class InsuranceRequest(BaseModel):
    cargo_type: str = Field(examples=["Glass", "Other"])
    declared_price: float | int = Field(examples=[100, 14000.94], gt=0)
    transfer_date: str = Field(examples=["2021-06-01"])

    @field_validator('transfer_date')
    def date_format(cls, v):
        try:
            transfer_date = date.fromisoformat(v)
            if transfer_date < date.today():
                raise ValueError("Transfer date cannot be in the past.")
            return v
        except ValueError:
            raise ValueError("Invalid date format! Example: '2020-06-01'.")


class ResponsePrice(BaseModel):
    status: str
    tariff: str
    insurance_cost: Decimal
