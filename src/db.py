import json
import uuid
import os.path

from models.restaurant import Restaurant, RestaurantRegistrationInfo
from models.user import User, UserRegistrationInfo, AccountType

import secrets


BEARER_TOKEN_LENGTH = 128


accounts = {}


def initialize():
    global accounts
    if os.path.isfile("accounts.json"):
        with open("accounts.json", "r") as f:
            accounts = json.load(f)
    else:
        accounts = {}


def save_accounts():
    with open("accounts.json", "w+") as f:
        f.write(json.dumps(accounts))


def _generate_uuid():
    return str(uuid.uuid4())


def _generate_bearer():
    return secrets.token_urlsafe(BEARER_TOKEN_LENGTH)


def _account_with_email_exists(email: str) -> bool:
    for account in accounts.values():
        if account["email"] == email:
            return True
    return False


def get_all_users() -> list[User]:
    return [User(**account) for account in accounts.values()]


def get_user_by_id(id: str) -> User:
    if id in accounts:
        return User(**accounts[id])
    raise ValueError("No account with that id")


def get_user_by_email(email: str) -> User:
    for account in accounts.values():
        if account["email"] == email:
            return User(**account)
    raise ValueError("No account with that email")


def create_account(user_info: UserRegistrationInfo) -> User:
    if _account_with_email_exists(user_info.email):
        raise ValueError("An account with that email already exists")

    id = _generate_uuid()
    bearer = _generate_bearer()
    user = User(
        account_type=user_info.account_type,
        id=id,
        email=user_info.email,
        bearer=bearer,
        password=user_info.password,
        first_name=user_info.first_name,
        last_name=user_info.last_name
    )

    if user_info.account_type == AccountType.BUSINESS:
        user.restaurant = create_restaurant(user_info.restaurant)

    accounts[id] = user.model_dump()

    save_accounts()

    return user


def delete_account(id: str):
    if id in accounts:
        del accounts[id]
        save_accounts()
    else:
        raise ValueError("No account with that id")


def verify_bearer(bearer: str) -> User:
    for account in accounts.values():
        if account["bearer"] == bearer:
            return User(**account)
    raise ValueError("Invalid bearer token")


def get_all_restaurants():
    restaurants = []
    users = get_all_users()
    for user in users:
        if user.account_type == AccountType.BUSINESS:
            restaurants.append(user.restaurant)
    return restaurants


def get_restaurant_by_id(restaurant_id: str):
    users = get_all_users()
    for user in users:
        if user.account_type == AccountType.BUSINESS and user.restaurant.id == restaurant_id:
            return user.restaurant
    return None


def create_restaurant(restaurant_info: RestaurantRegistrationInfo):
    restaurant_id = _generate_uuid()
    restaurant = Restaurant(
        id=restaurant_id,
        name=restaurant_info.name,
        address=restaurant_info.address,
        pickup_hours=restaurant_info.pickup_hours
    )

    return restaurant


def delete_restaurant(restaurant_id: str):
    users = get_all_users()
    for user in users:
        if user.account_type == AccountType.BUSINESS and user.restaurant.id == restaurant_id:
            user.restaurant = None
            save_accounts()
            return
    raise ValueError("No restaurant with that id")