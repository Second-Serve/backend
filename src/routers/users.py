from typing import Annotated

from pydantic import BaseModel, SecretStr

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from models.user import UserInfo


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

FAKE_USERS_DB = [
    {
        "id": 0,
        "email": "satanur@wisc.edu",
        "first_name": "Diya",
        "last_name": "Satanur"
    },
    {
        "id": 1,
        "email": "asunil2@wisc.edu",
        "first_name": "Aditi",
        "last_name": "Sunil"
    },
    {
        "id": 2,
        "email": "ozinn@wisc.edu",
        "first_name": "Owen",
        "last_name": "Zinn"
    },
    {
        "id": 3,
        "email": "dodhia@wisc.edu",
        "first_name": "Arushi",
        "last_name": "Dodhia"
    }
]


@router.get("/")
async def get_users(token: Annotated[str, Depends(oauth2_scheme)]):
    # TODO: Implement this function
    return FAKE_USERS_DB


@router.get("/me")
async def get_users_me():
    # TODO: Implement this function
    return FAKE_USERS_DB[0]


@router.get("/{id}")
async def get_users_by_id(id: int):
    # TODO: Implement this function
    for user in FAKE_USERS_DB:
        if user["id"] == id:
            return user


@router.post("/")
async def create_account(user_info: UserInfo):
    pass