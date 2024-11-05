import json
import uuid

import secrets

from models.user import User, UserRegistrationInfo, AccountType

BEARER_TOKEN_LENGTH = 128


accounts = {}


def initialize():
    global accounts
    with open("accounts.json", "r") as f:
        if f.readable():
            accounts = json.load(f)
        else:
            accounts = {}


def save_accounts():
    with open("accounts.json", "w") as f:
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