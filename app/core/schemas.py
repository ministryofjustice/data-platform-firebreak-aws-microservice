from pydantic import BaseModel


class PermissionBase(BaseModel):
    name: str


class PermissionCreate(PermissionBase):
    pass


class Permission(PermissionBase):
    id: int

    class Config:
        orm_mode = True


class RoleBase(BaseModel):
    rolename: str


class RoleCreate(RoleBase):
    oidc_user_id: str


class RoleRead(RoleBase):
    id: int

    class Config:
        orm_mode = True
