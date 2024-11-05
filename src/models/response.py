from pydantic import BaseModel

class APIResponse(BaseModel):
    ok: bool = True
    result: dict | None = None
    error: str | None = None