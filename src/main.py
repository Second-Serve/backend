import uvicorn
from fastapi import FastAPI

import db

from routers import users

app = FastAPI()


app.include_router(users.router)


if __name__ == "__main__":
    db.initialize()
    uvicorn.run(app, host="0.0.0.0", port=80)