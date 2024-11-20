import json

import db

from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from models.response import APIResponse


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def bearer_is_admin(token: str = Depends(oauth2_scheme)) -> bool:
    user = db.verify_bearer(token)
    return user.is_admin


class APIResponseClass(JSONResponse):
    def render(self, content):
        response = APIResponse(
            result=content
        )
        response_dict = response.dict(exclude_none=True)
        response_json_string = json.dumps(response_dict)
        return bytes(response_json_string, "utf-8")