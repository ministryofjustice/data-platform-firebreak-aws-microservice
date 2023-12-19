import boto3
from fastapi import APIRouter, HTTPException

from app import services

router = APIRouter(prefix="/roles", tags=["roles"])


def iam_client() -> boto3.client:
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


@router.get("/{role_name}/")
async def get_role_by_name(role_name: str):
    """Return an IAM role for a given role name"""
    response = iam_client().get_role(RoleName=role_name)
    if not response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return HTTPException(status_code=400)
    return response.get("Role", {})


@router.get("/{role_name}/policies/")
async def get_policies_by_role_name(role_name: str):
    """Return inline iam policies for a given iam role identified by role_name"""
    service = services.AWSRolesService(rolename=role_name)
    policies = service.get_policies_for_role()
    return policies
