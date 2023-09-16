from datetime import datetime
from abc import ABC
from typing import List, Optional

from exceptions.objects import NotLaserProcedure
from config import PROCEDURE_PARAMS
from data.types import TreatemtTypes
from utils.jinja import get_template
from database.models import VisitModel


class BaseCosmet(ABC):
    _excluded_keys = ["percent", "subscriptions"]

    def __init__(self, gross: Optional[int], type: str):
        self.gross = gross
        self.type = type

    @property
    def earning(self) -> int:
        return int(self.percent * self.gross)

    def to_dict(self):
        return dict(
            (key, value)
            for (key, value) in self.__dict__.items()
            if key not in self._excluded_keys
        )

    @property
    def name(self):
        return TreatemtTypes[self.type].value

    def report(self, pdf=False) -> str:
        prefix = "for_pdf/" if pdf else ""
        filename = f"{prefix}{self.type.lower()}.j2"

        tmpl = get_template(filename)
        msg = tmpl.render(p=self)

        return msg


class Cosmetics(BaseCosmet):
    percent = 0.1


class ClassicCosmetology(BaseCosmet):
    percent = 0.4


class LaserSubscription:
    sub_visits = 4

    def __init__(self, sub_gross: int):
        self.sub_gross = sub_gross

    @property
    def visit_gross(self) -> int:
        return int(self.sub_gross / self.sub_visits)

    def to_dict(self):
        return {"sub_gross": self.sub_gross}


class Laser(BaseCosmet):
    percent = 0.1
    per_hour = 150

    def __init__(
        self,
        type: str,
        duration: int,
        gross: Optional[int] = None,
        manual_input: bool = False,
        manual_value: int = 0,
    ):
        self.subscriptions: List[LaserSubscription] = []
        self.duration = duration
        self.manual_input = manual_input
        self.manual_value = manual_value
        super().__init__(gross, type)

    def _add_per_hour_pay(func):
        def wrapper(self):
            per_hour_pay = int(self.per_hour * (self.duration / 60))
            earning = func(self)
            total_earing = per_hour_pay + earning
            return total_earing

        return wrapper

    @property
    @_add_per_hour_pay
    def earning(self) -> int:
        if self.gross:
            return super().earning
        elif self.manual_input:
            return self.manual_value
        return int(sum([sub.visit_gross * self.percent for sub in self.subscriptions]))


class Injections(BaseCosmet):
    percent = 0.5

    def __init__(self, gross: int, type: str, prime_cost: int):
        self.prime_cost = prime_cost
        super().__init__(gross, type)

    @property
    def earning(self):
        return int((self.gross - self.prime_cost) * self.percent)


class RollerMassage(BaseCosmet):
    def __init__(self, gross, type, sub=False, first=False, sub_visits=None):
        self.sub_visits = sub_visits
        self.sub = sub
        self.first = first
        self.percent = 0.2 if first else 0.3
        super().__init__(gross, type)

    @property
    def earning(self):
        if self.sub:
            return int(self.gross / self.sub_visits * self.percent)
        else:
            return super().earning


class ApparatusCosmetology(RollerMassage):
    pass


class ProceduresManager(list):
    PROCEDURES = {
        "CLASSIC_COSMETOLOGY": ClassicCosmetology,
        "APPARATUS_COSMETOLOGY": ApparatusCosmetology,
        "COSMETICS": Cosmetics,
        "ROLLER_MASSAGE": RollerMassage,
        "INJECTIONS": Injections,
        "LASER": Laser,
    }

    def add(self, **kwargs):
        info = self._get_procedure_info(kwargs)
        procedure = self.PROCEDURES[info["type"]]
        self.append(procedure(**info))

    def last(self):
        if len(self):
            return self[-1]
        else:
            return None

    def add_laser_sub(self, sub_gross: int):
        proc: Laser = self.last()
        if not isinstance(proc, Laser):
            raise NotLaserProcedure
        else:
            proc.subscriptions.append(LaserSubscription(sub_gross))

    @staticmethod
    def _get_procedure_info(data: dict) -> dict:
        info = {}
        for param in PROCEDURE_PARAMS:
            if param in data:
                info[param] = data[param]
        return info


class Visit:
    def __init__(self, date: datetime, client_name: str, db_id: int | None = None):
        self.date = date
        self.client_name = client_name
        self.procedures = ProceduresManager()
        self.db_id = db_id

    def get_total(self):
        sum = 0
        for elem in self.procedures:
            sum += elem.earning
        return sum

    def to_dict(self) -> dict:
        data = {"date": self.date, "client_name": self.client_name, "procedures": []}

        for proc in self.procedures:
            dict_proc = proc.to_dict()

            if isinstance(proc, Laser) and proc.subscriptions:
                dict_proc["subscriptions"] = []
                for sub in proc.subscriptions:
                    dict_proc["subscriptions"].append(sub.to_dict())

            data["procedures"].append(dict_proc)

        return data

    def visit_report(self, pdf=False):
        prefix = "for_pdf/" if pdf else ""
        tmpt = get_template(f"{prefix}visit.j2")
        msg = tmpt.render(visit=self, total=self.get_total())

        return msg


Minutes = int


class Workday:
    def __init__(
        self,
        date: datetime,
        visits: list[VisitModel] | None = None,
        idle_time: Minutes = 0,
    ):
        self.date = date
        self.visits = visits
        self.idle_time = idle_time

    @property
    def visits(self):
        return self._visits

    @visits.setter
    def visits(self, value: list[VisitModel]):
        if value is None:
            self._visits = []
        else:
            self._visits = [self._create_visit_from_db_model(val) for val in value]

    def _create_visit_from_db_model(self, visit: VisitModel):
        data = visit.as_dict()
        procs = data.pop("procedures")
        visit = Visit(**data)

        for proc in procs:  # type: dict
            if proc["type"] == "LASER" and proc.get("subscriptions"):
                subscriptions = proc.pop("subscriptions")
                visit.procedures.add(**proc)
                for sub in subscriptions:
                    visit.procedures.add_laser_sub(**sub)
            else:
                visit.procedures.add(**proc)
        return visit

    def get_idle_time_pay(self):
        return int(self.idle_time / 60 * 150)

    def get_total(self):
        return sum([v.get_total() for v in self.visits]) + self.get_idle_time_pay()

    def get_number_of_visits(self) -> int:
        return len(self.visits)

    def workday_report(self, pdf=False) -> str:
        prefix = "for_pdf/" if pdf else ""
        tmpt = get_template(f"{prefix}workday.j2")
        msg = tmpt.render(workday=self)
        return msg

    def date_str(self) -> str:
        return self.date.strftime("%d/%m/%Y")


class PeriodReport:
    def __init__(
        self,
        workdays: list[Workday],
        start_date: datetime,
        end_date: datetime,
        master: str,
    ):
        self.workdays = workdays
        self.start_date = start_date
        self.end_date = end_date
        self.master = master

    def get_period_str(self) -> str:
        start, end = self._get_start_end_str()
        return f"{start} - {end}"

    def get_filename(self) -> str:
        start, end = self._get_start_end_str(sep="_")
        return f"report_{start}__{end}.pdf"

    @staticmethod
    def _date_str(date: datetime, sep: str = "/") -> str:
        return date.strftime(f"%d{sep}%m{sep}%Y")

    def _get_start_end_str(self, sep: str = "/"):
        start = self._date_str(self.start_date, sep)
        end = self._date_str(self.end_date, sep)
        return start, end

    def get_period_total(self) -> int:
        return sum(w.get_total() for w in self.workdays)

    def get_report(self, file=False):
        tmpt_name = "for_pdf/period_file.j2" if file else "period_short.j2"
        tmpt = get_template(tmpt_name)
        report = tmpt.render(period=self)
        return report
