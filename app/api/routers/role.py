import boto3
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core import crud, schemas
from app.core.databases import get_db

router = APIRouter(prefix="/roles", tags=["roles"])


def iam_client():
    # TODO mock this in local dev? Try localstack?
    return boto3.client("iam")


@router.get("/")
async def get_roles():
    """
    List all the roles
    """
    response = iam_client().list_roles()
    if not response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return HTTPException(400)
    return response.get("Roles", [])


@router.get("/{username}/")
async def get_role(username: str, db: Session = Depends(get_db)):
    db_role = crud.get_role(db, username)
    if not db_role:
        raise HTTPException(status_code=404, detail="Role Does Not Exist")
    return db_role


@router.post("/")
async def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    db_role = crud.get_role(db, role.username)
    if db_role:
        raise HTTPException(status_code=400, detail="Role exists")
    return crud.create_role(db, role)
