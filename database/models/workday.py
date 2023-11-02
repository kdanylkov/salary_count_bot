from .base import Base

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


if TYPE_CHECKING:
    from .user import UserModel
    from .visit import VisitModel


class WorkDayModel(Base):
    __tablename__ = "workdays"

    date: Mapped[datetime]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    idle_time: Mapped[int] = mapped_column(default=0)

    user: Mapped["UserModel"] = relationship(back_populates="workdays")
    visits: Mapped[list["VisitModel"]] = relationship(
        back_populates="workday", cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
        return f'Workday of {self.user.name} for date: {self.date.strftime("%Y%m%d")}'

    def __repr__(self):
        return str(self)
