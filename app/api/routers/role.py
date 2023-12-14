from typing import Any

import boto3
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core import crud
from app.core.databases import get_db
from app.core.jinja import JsonTemplates

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
async def get_managed_policies_by_role_name(role_name: str):
    """Return inline iam policies for a given iam role identified by role_name"""
    response = iam_client().list_attached_role_policies(RoleName=role_name)
    if not response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return HTTPException(status_code=400)

    policies: list[dict[Any, Any]] = list()
    for policy in response.get("AttachedPolicies", []):
        policy_arn: str = policy.get("PolicyArn")
        policy_response: dict = iam_client().get_policy(PolicyArn=policy_arn)
        if not policy_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            return HTTPException(status_code=400)
        policies.append(policy_response.get("Policy", {}))
    return policies


@router.get("/{username}/")
async def get_role(username: str, db: Session = Depends(get_db)):
    db_role = crud.get_role(db, username)
    if not db_role:
        raise HTTPException(status_code=404, detail="Role Does Not Exist")
    return db_role


@router.post("/")
async def create_role(username: str):
    policy = JsonTemplates().get_trust_policy_data(username=username)
    iam = iam_client()
    response = iam.create_role(RoleName=username, AssumeRolePolicyDocument=json.dumps(policy))
    return response["Role"]
