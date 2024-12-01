from .base import Base
from .mixins.id_int_pk import IdIntMixin
from sqlalchemy.orm import Mapped, mapped_column


class CargoType(Base, IdIntMixin):
    """ Типы карго тарифов """

    name: Mapped[str] = mapped_column(unique=True, index=True)

