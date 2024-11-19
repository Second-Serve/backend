import json

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from models.user import User, UserLoginInfo, UserRegistrationInfo
from models.response import APIResponse

from util.api import APIResponseClass

import db


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def _bearer_is_admin(token: str = Depends(oauth2_scheme)) -> bool:
    user = db.verify_bearer(token)
    return user.is_admin


@router.get("/", response_class=APIResponseClass)
async def get_users(token: Annotated[str, Depends(oauth2_scheme)]) -> None:
    if _bearer_is_admin(token):
        return {
            "users": [user.dict() for user in db.get_all_users()]
        }
    else:
        raise ValueError("User is not an admin")


@router.get("/me", response_class=APIResponseClass)
async def get_my_user(token: Annotated[str, Depends(oauth2_scheme)]) -> APIResponse:
    user = db.verify_bearer(token)
    return user.dict(exclude={"password", "bearer"})


@router.delete("/{id}", response_class=APIResponseClass)
async def delete_account(id: str, token: Annotated[str, Depends(oauth2_scheme)]) -> None:
    if _bearer_is_admin(token):
        db.delete_account(id)
    else:
        raise ValueError("User is not an admin")


@router.delete("/me", response_class=APIResponseClass)
async def delete_my_account(token: Annotated[str, Depends(oauth2_scheme)]) -> None:
    user = db.verify_bearer(token)
    db.delete_account(user.id)


@router.get("/{id}", response_class=APIResponseClass)
async def get_user_by_id(id: str, token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    if _bearer_is_admin(token):
        user = db.get_user_by_id(id)
        return user.dict(exclude={"password", "bearer"})
    else:
        raise ValueError("User is not an admin")


@router.post("/", response_class=APIResponseClass)
async def create_account(user_info: UserRegistrationInfo) -> User:
    return db.create_account(user_info)


@router.put("/me", response_class=APIResponseClass)
async def update_account(new_user_info: UserRegistrationInfo, token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    user = db.verify_bearer(token)

    if new_user_info.account_type != user.account_type:
        raise ValueError("Cannot change account type")

    return db.update_account(user.id, new_user_info)


@router.put("/{id}", response_class=APIResponseClass)
async def update_user_by_id(id: str, new_user_info: UserRegistrationInfo, token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    if _bearer_is_admin(token):
        if new_user_info.account_type != new_user_info.account_type:
            raise ValueError("Cannot change account type")
        return db.update_account(id, new_user_info)
    else:
        raise ValueError("User is not an admin")


@router.post("/login", response_class=APIResponseClass)
async def login(info: UserLoginInfo) -> User:
    user = db.get_user_by_email(info.email)
    if user.password != info.password:
        raise ValueError("Invalid password")
    return user