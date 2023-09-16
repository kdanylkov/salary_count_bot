from .base import Base

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy import String

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .workday import WorkDayModel
    from .visit import VisitModel


class UserModel(Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(30))

    workdays: Mapped[list["WorkDayModel"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    visits: Mapped[list["VisitModel"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
        return f"User (telegram_id={self.id}, name={self.name})"

    def __repr__(self) -> str:
        return str(self)
