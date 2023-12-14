from dotenv import load_dotenv
from fastapi import FastAPI

from app.api.routers import role
from app.core import databases, models

load_dotenv()
models.Base.metadata.create_all(bind=databases.engine)

app = FastAPI()
app.include_router(role.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
