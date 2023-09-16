from .base import Base
from config import PROCEDURE_PARAMS

from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


if TYPE_CHECKING:
    from .visit import VisitModel
    from .subscription import SubscriptionModel


class ProcedureModel(Base):
    __tablename__ = "procedures"

    type: Mapped[str]
    gross: Mapped[int] = mapped_column(nullable=True, use_existing_column=True)
    sub: Mapped[bool] = mapped_column(nullable=True, use_existing_column=True)
    first: Mapped[bool] = mapped_column(nullable=True, use_existing_column=True)
    sub_visits: Mapped[int] = mapped_column(nullable=True, use_existing_column=True)
    prime_cost: Mapped[int] = mapped_column(nullable=True)
    duration: Mapped[Optional[int]]
    manual_input: Mapped[Optional[bool]]
    manual_value: Mapped[Optional[int]]

    visit_id: Mapped[int] = mapped_column(ForeignKey("visits.id"))

    visit: Mapped["VisitModel"] = relationship(back_populates="procedures")
    subscriptions: Mapped[list["SubscriptionModel"]] = relationship(
        back_populates="procedure", cascade="all, delete-orphan"
    )

    def as_dict(self):
        data = {}

        for c in self.__table__.columns:
            if c.name in PROCEDURE_PARAMS and getattr(self, c.name) is not None:
                data[c.name] = getattr(self, c.name)

        if self.type == "LASER" and self.subscriptions:
            data["subscriptions"] = []
            for sub in self.subscriptions:
                data["subscriptions"].append({"sub_gross": sub.sub_gross})

        return data
