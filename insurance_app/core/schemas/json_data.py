from datetime import date
from pydantic import BaseModel, field_validator, RootModel


class JsonRates(BaseModel):
    cargo_type: str
    rate: str

    @field_validator('rate')
    def rate_must_be_positive(cls, v):
        if float(v) <= 0:
            raise ValueError("Rate must be positive!")


class FullJsonSchema(RootModel):
    root: dict[str, list[JsonRates]]

    @field_validator('root')
    def date_format(cls, v):
        for key in v:
            try:
                date.fromisoformat(key)
            except ValueError:
                raise ValueError("Invalid date format! Example: '2020-06-01'.")
