import calendar
from datetime import datetime
from dataclasses import dataclass


@dataclass(frozen=False)
class CreatedAtDatetimeInfo:
    day: int
    month: str  # full name of month (in ENG)
    year: int

    def __init__(self, timestamp: float):
        self.timestamp = timestamp
        self.get_month_and_year_from_timestamp()

    def get_month_and_year_from_timestamp(self):
        created_at: datetime = datetime.fromtimestamp(self.timestamp)
        self.day, self.month, self.year = created_at.day, self.get_month_as_string(created_at.month), created_at.year

    @staticmethod
    def get_month_as_string(month: int):
        return calendar.month_name[month]
