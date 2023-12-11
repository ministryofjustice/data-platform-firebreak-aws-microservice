from fastapi import FastAPI
from api.routers import role

app = FastAPI()

app.include_router(role.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
