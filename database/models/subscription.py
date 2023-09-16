from .base import Base

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


if TYPE_CHECKING:
    from .procedure import ProcedureModel


class SubscriptionModel(Base):
    __tablename__ = "subscriptions"

    sub_gross: Mapped[int]
    procedure_id: Mapped[int] = mapped_column(ForeignKey("procedures.id"))

    procedure: Mapped["ProcedureModel"] = relationship(back_populates="subscriptions")
