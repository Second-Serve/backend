import json
import uuid

from models.user import User, CustomerUser, BusinessUser


accounts = {}


def initialize():
    with open("accounts.json", "r") as f:
        if f.read():
            accounts = json.loads(f.read())
        else:
            accounts = {}


def save_accounts():
    with open("accounts.json", "w") as f:
        f.write(json.dumps(accounts))


def create_customer_account(email: str, password: str, first_name: str, last_name: str):
    new_account_id = str(uuid.uuid4())
    accounts[new_account_id] = {
        "type": "customer",
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name
    }
    save_accounts()

    return CustomerUser(
        id=new_account_id,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        campus_id=None
    )


def create_business_account(email: str, password: str, business_name: str, business_address: str, business_pickup_hours):
    new_account_id = str(uuid.uuid4())
    user = BusinessUser(
        id=new_account_id,
        email=email,
        password=password,
        business_name=business_name,
        business_address=business_address,
        business_pickup_hours=business_pickup_hours
    )
    accounts[new_account_id] = user.model_dump_json()