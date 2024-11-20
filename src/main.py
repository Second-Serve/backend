import uvicorn
import db

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from models.response import APIResponse

from routers import users, restaurants

app = FastAPI()
app.include_router(users.router)
app.include_router(restaurants.router)


# TODO: Figure out how to require authentication for this route
app.mount("/restaurants/banners", StaticFiles(directory="db/images/banners/"), name="banners")

@app.exception_handler(HTTPException)
def value_error_handler(request: Request, e: HTTPException):
    print(f"An error occurred: {e}")
    response = APIResponse(
        ok=False,
        error=str(e.detail)
    )
    return JSONResponse(content=response.dict(), status_code=400)

if __name__ == "__main__":
    db.initialize()
    uvicorn.run(app, host="0.0.0.0", port=80)