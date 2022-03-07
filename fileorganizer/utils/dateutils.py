import os
import calendar
from datetime import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class CreatedAtDatetimeInfo:
    day: int
    month: str
    year: int


@dataclass(frozen=True)
class ModifiedAtDatetimeInfo:
    day: int
    month: str
    year: int


@dataclass(frozen=False)
class DatetimeInfo:
    created_at: CreatedAtDatetimeInfo
    modified_at: ModifiedAtDatetimeInfo

    def __init__(self, path: str):
        self.created_at = CreatedAtDatetimeInfo(*self.get_month_and_year_from_timestamp(os.stat(path).st_ctime))
        self.modified_at = ModifiedAtDatetimeInfo(*self.get_month_and_year_from_timestamp(os.stat(path).st_mtime))

    @staticmethod
    def get_month_and_year_from_timestamp(timestamp: float):
        d: datetime = datetime.fromtimestamp(timestamp)
        return d.day, DatetimeInfo.get_month_as_string(d.month), d.year

    @staticmethod
    def get_month_as_string(month: int):
        return calendar.month_name[month]
