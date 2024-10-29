from .pickup_hours import WeeklyPickupHours

from pydantic import BaseModel, SecretStr


class UserInfo(BaseModel):
    email: str
    password: SecretStr


class User(UserInfo):
    id: int 


class CustomerUser(User):
    campus_id: str | None
    first_name: str
    last_name: str


class BusinessUser(User):
    business_name: str
    business_address: str
    business_pickup_hours: WeeklyPickupHours