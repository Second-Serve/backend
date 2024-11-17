from fastapi.responses import JSONResponse
import uvicorn
from fastapi import FastAPI, Request

import db

from models.response import APIResponse

from routers import users, restaurants

app = FastAPI()
app.include_router(users.router)
app.include_router(restaurants.router)


@app.exception_handler(ValueError)
def value_error_handler(request: Request, e: ValueError):
    response = APIResponse(
        ok=False,
        error=str(e)
    )
    return JSONResponse(content=response.dict(), status_code=400)


if __name__ == "__main__":
    db.initialize()
    uvicorn.run(app, host="0.0.0.0", port=80)