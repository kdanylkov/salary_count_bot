from .base import Base

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

if TYPE_CHECKING:
    from .workday import WorkDayModel
    from .procedure import ProcedureModel
    from .user import UserModel


class VisitModel(Base):
    __tablename__ = "visits"

    client_name: Mapped[str]
    workday_id: Mapped[str] = mapped_column(ForeignKey("workdays.id"))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))

    workday: Mapped["WorkDayModel"] = relationship(back_populates="visits")
    user: Mapped["UserModel"] = relationship(back_populates="visits")
    procedures: Mapped[list["ProcedureModel"]] = relationship(
        back_populates="visit", cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
        return f"Visit of {self.client_name} for {self.workday.date}"

    def __repr__(self) -> str:
        return str(self)

    def as_dict(self) -> dict:
        data = {
            "client_name": self.client_name,
            "date": self.workday.date,
            "db_id": self.id,
            "procedures": [],
        }
        for proc in self.procedures:
            data["procedures"].append(proc.as_dict())

        return data
