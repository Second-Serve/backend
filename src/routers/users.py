from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from models.user import User, UserRegistrationInfo
from models.response import APIResponse

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


@router.get("/")
async def get_users(token: Annotated[str, Depends(oauth2_scheme)]) -> APIResponse:
    try:
        if _bearer_is_admin(token):
            return APIResponse(
                result={
                    "users": [user.dict() for user in db.get_all_users()]
                }
            )
        else:
            raise ValueError("User is not an admin")
    except ValueError as e:
        return APIResponse(
            ok=False,
            error=str(e)
        )


@router.get("/me")
async def get_my_user(token: Annotated[str, Depends(oauth2_scheme)]) -> APIResponse:
    user = db.verify_bearer(token)
    return await get_user_by_id(user.id, token)


@router.delete("/{id}")
async def delete_account(id: str, token: Annotated[str, Depends(oauth2_scheme)]) -> APIResponse:
    try:
        if _bearer_is_admin(token):
            db.delete_account(id)
            return APIResponse(ok=True)
        else:
            raise ValueError("User is not an admin")
    except ValueError as e:
        return APIResponse(
            ok=False,
            error=str(e)
        )


@router.delete("/me")
async def delete_my_account(token: Annotated[str, Depends(oauth2_scheme)]) -> APIResponse:
    try:
        user = db.verify_bearer(token)
        db.delete_account(user.id)
        return APIResponse(
            result="Account deleted"
        )
    except ValueError as e:
        return APIResponse(
            ok=False,
            error=str(e)
        )


@router.get("/{id}")
async def get_user_by_id(id: str, token: Annotated[str, Depends(oauth2_scheme)]) -> APIResponse:
    try:
        if _bearer_is_admin(token):
            user = db.get_user_by_id(id)
            return APIResponse(
                result=user.dict()
            )
    except ValueError as e:
        return APIResponse(
            ok=False,
            error=str(e)
        )


@router.post("/")
async def create_account(user_info: UserRegistrationInfo) -> APIResponse:
    try:
        user = db.create_account(user_info)
        return APIResponse(
            result=user.dict()
        )
    except ValueError as e:
        return APIResponse(
            ok=False,
            error=str(e)
        )