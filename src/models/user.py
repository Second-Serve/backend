from enum import Enum

from .pickup_hours import WeeklyPickupHours

from pydantic import BaseModel


class AccountType(str, Enum):
    CUSTOMER = "customer"
    BUSINESS = "business"    


class PublicUserInfo(BaseModel):
    account_type: AccountType
    email: str
    is_admin: bool = False
    first_name: str | None = None
    last_name: str | None = None
    business_name: str | None = None
    business_address: str | None = None
    business_pickup_hours: WeeklyPickupHours | None = None


class UserRegistrationInfo(PublicUserInfo):
    password: str


# User accounts have an ID and a bearer token, but those are not part of the registration info
class User(UserRegistrationInfo):
    id: str
    bearer: str