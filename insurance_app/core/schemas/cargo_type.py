from pydantic import BaseModel


class CargoTypeSchema(BaseModel):
    id: int
    name: str
