from typing import Annotated, Optional

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel


router = APIRouter(prefix="/roles", tags=["roles"])


class Role(BaseModel):
    name: str
    permissions: Optional[list[str]] = None
    username: str


class RoleResponse(BaseModel):
    name: str

michael = Role(name='Michael', permissions=["write"], username="michael")
mitch = Role(name='Mitch', permissions=["read"], username="mitch")

roles = [michael, mitch]
# roles = {
#     "michael": {
#         "name": "michael",
#         "permissions":["write"]
#     },
#     "mitch": {
#         "name": "mitch",
#         "permissions":["read"]
#     }
# }


@router.get("/", response_model=list[RoleResponse])
async def get_roles():
    """
    List all the roles
    """
    return roles


@router.get("/{username}/", response_model=RoleResponse)
async def get_roles(username: str):
    for role in roles:
        if role.username == username:
            return role
    raise HTTPException(status_code=404, detail="Role not found")


@router.post("/", response_model=RoleResponse)
async def create_role(role: Role):
    print(role.name)
    print(role.permissions)
    return list[role]