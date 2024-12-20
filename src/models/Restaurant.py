from pydantic import BaseModel
from typing import List, Optional

from models.pickup_hours import WeeklyPickupHours

class RestaurantRegistrationInfo(BaseModel):
    name: str
    address: str
    pickup_hours: WeeklyPickupHours | None = None
    bag_price: float
    bags_available: int

class Restaurant(BaseModel):
    id: str
    name: str
    address: str
    pickup_hours: WeeklyPickupHours | None = None
    bag_price: float
    bags_available: int
    bags_claimed: int = 0