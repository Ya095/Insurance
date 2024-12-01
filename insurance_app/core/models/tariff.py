from datetime import date
from .base import Base
from .mixins.id_int_pk import IdIntMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UniqueConstraint, ForeignKey


class Tariff(Base, IdIntMixin):
    """Модель тарифа страхования"""

    start_date: Mapped[date]
    cargo_type: Mapped[int] = mapped_column(ForeignKey("cargo_types.id", ondelete="CASCADE"))
    rate: Mapped[float]

    __table_args__ = (
        UniqueConstraint("cargo_type", "rate", "start_date"),
    )
