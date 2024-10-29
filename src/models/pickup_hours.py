from enum import IntEnum

from pydantic import BaseModel


class Weekday(IntEnum):
    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6


class DailyPickupHours(BaseModel):
    weekday: Weekday
    start_time: str
    end_time: str


class WeeklyPickupHours(BaseModel):
    sunday: DailyPickupHours
    monday: DailyPickupHours
    tuesday: DailyPickupHours
    wednesday: DailyPickupHours
    thursday: DailyPickupHours
    friday: DailyPickupHours
    saturday: DailyPickupHours