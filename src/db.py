import json
import uuid
import os.path
from models.Restaurant import Restaurant

import secrets

from models.user import User, UserRegistrationInfo, AccountType

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


def _generate_account_id():
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

    id = _generate_account_id()
    bearer = _generate_bearer()
    user = None
    if user_info.account_type == AccountType.CUSTOMER:
        user = User(
            account_type=user_info.account_type,
            id=id,
            email=user_info.email,
            password=user_info.password,
            first_name=user_info.first_name,
            last_name=user_info.last_name,
            campus_id=None,
            bearer=bearer
        )
    elif user_info.account_type == AccountType.BUSINESS:
        user = User(
            account_type=user_info.account_type,
            id=id,
            email=user_info.email,
            password=user_info.password,
            business_name=user_info.business_name,
            business_address=user_info.business_address,
            business_pickup_hours=user_info.business_pickup_hours,
            bearer=bearer
        )
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

restaurants = {}

def initialize_restaurants():
    global restaurants
    if os.path.isfile("restaurants.json"):
        with open("restaurants.json", "r") as f:
            restaurants = json.load(f)
    else:
        restaurants = {
            str(uuid.uuid4()): {
                "id": str(uuid.uuid4()),
                "name": "First Restaurant",
                "address": "123 Food St, Madison",
                "pickup_hours": "11:00 AM - 10:00 PM",
                "menu_items": ["Burger", "Fries", "Shake"]
            },
            str(uuid.uuid4()): {
                "id": str(uuid.uuid4()),
                "name": "Second Restaurant",
                "address": "456 Food Ave, Madison",
                "pickup_hours": "10:00 AM - 11:00 PM",
                "menu_items": ["Pizza1", "Pizza2"]
            },
        }
        save_restaurants()

def save_restaurants():
    with open("restaurants.json", "w") as f:
        json.dump(restaurants, f)

def get_all_restaurants():
    return [Restaurant(**data) for data in restaurants.values()]

def get_restaurant_by_id(restaurant_id: str):
    if restaurant_id in restaurants:
        return Restaurant(**restaurants[restaurant_id])
    raise ValueError("No restaurant with that id")

def add_restaurant(restaurant_data: dict):
    restaurant_id = str(uuid.uuid4())
    restaurants[restaurant_id] = {**restaurant_data, "id": restaurant_id}
    save_restaurants()
    return Restaurant(**restaurants[restaurant_id])

def delete_restaurant(restaurant_id: str):
    if restaurant_id in restaurants:
        del restaurants[restaurant_id]
        save_restaurants()
    else:
        raise ValueError("No restaurant with that id")