from dotenv import load_dotenv
from fastapi import FastAPI

from app.api.routers import role

load_dotenv()

# initialise the app with routes
app = FastAPI()
app.include_router(role.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
