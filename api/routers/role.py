from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core import crud, schemas
from core.databases import get_db

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/")
async def get_roles(db: Session = Depends(get_db)):
    """
    List all the roles
    """
    return crud.get_roles(db)


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
