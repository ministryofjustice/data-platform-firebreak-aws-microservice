from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBearer

from app.api.routers import role
from app.core import databases, models

load_dotenv()

# TODO remove if DB not used
models.Base.metadata.create_all(bind=databases.engine)

# require authentication for all endpoints
token_auth_scheme = HTTPBearer()

# initialise the app with routes
app = FastAPI(dependencies=[Depends(token_auth_scheme)])
app.include_router(role.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
