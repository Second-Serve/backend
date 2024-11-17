import json
from fastapi.responses import JSONResponse
from models.response import APIResponse


class APIResponseClass(JSONResponse):
    def render(self, content):
        response = APIResponse(
            result=content
        )
        response_dict = response.dict(exclude_none=True)
        response_json_string = json.dumps(response_dict)
        return bytes(response_json_string, "utf-8")