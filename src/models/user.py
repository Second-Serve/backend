from enum import Enum

from .restaurant import Restaurant, RestaurantRegistrationInfo

from pydantic import BaseModel


class AccountType(str, Enum):
    CUSTOMER = "customer"
    BUSINESS = "business"    


class UserRegistrationInfo(BaseModel):
    account_type: AccountType
    email: str
    password: str
    first_name: str
    last_name: str
    restaurant: RestaurantRegistrationInfo | None = None


class UserLoginInfo(BaseModel):
    email: str
    password: str


class User(BaseModel):
    id: str
    account_type: AccountType
    email: str
    password: str
    bearer: str
    is_admin: bool = False
    first_name: str
    last_name: str
    campus_id: int | None = None
    restaurant: Restaurant | None = None