import boto3
from fastapi import APIRouter, HTTPException, Response, Security, status

from app import services
from app.api.auth import VerifyToken
from app.core import schemas

router = APIRouter(prefix="/roles", tags=["roles"])


# refactor this to use a function? Or pass to paths directly?
auth = VerifyToken()


def iam_client() -> boto3.client:
    # TODO mock this in local dev? Try localstack?
    return boto3.client("iam")


@router.get("/", dependencies=[Security(dependency=auth, scopes=["read:roles"])])
async def get_roles():
    """
    List all the roles
    """
    response = iam_client().list_roles()
    if not response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return HTTPException(status_code=400)
    return response.get("Roles", [])


@router.get("/{role_name}/", dependencies=[Security(dependency=auth, scopes=["read:roles"])])
async def get_role_by_name(role_name: str):
    """Return an IAM role for a given role name"""
    response = iam_client().get_role(RoleName=role_name)
    if not response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Role {role_name} not found"
        )
    return response.get("Role", {})


@router.post("/", dependencies=[Security(dependency=auth, scopes=["create:roles"])])
async def create_role(role: schemas.RoleCreate) -> Response:
    aws_service = services.AWSRolesService(rolename=role.rolename)
    try:
        response = aws_service.create_role(oidc_user_id=role.oidc_user_id)
    except services.RoleExistsException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Role {role.rolename} already exists"
        )
    return response["Role"]


@router.get(
    "/{role_name}/policies/", dependencies=[Security(dependency=auth, scopes=["read:roles"])]
)
async def get_policies_by_role_name(role_name: str) -> Response:
    """Return inline iam policies for a given iam role identified by role_name"""
    service = services.AWSRolesService(rolename=role_name)
    try:
        policies: list[dict] = service.get_policies_for_role()
    except services.RoleDoesNotExistException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Role {role_name} does not exist"
        )
    return policies
