from datetime import date
from .base import Base
from .mixins.id_int_pk import IdIntMixin
from sqlalchemy.orm import Mapped
from sqlalchemy import UniqueConstraint, Index


class Tariff(Base, IdIntMixin):
    """Модель тарифа страхования"""

    start_date: Mapped[date]
    cargo_type: Mapped[str]
    rate: Mapped[float]

    __table_args__ = (
        UniqueConstraint("cargo_type", "rate", "start_date"),
        Index("idx_cargo_date", "cargo_type", "start_date")
    )
