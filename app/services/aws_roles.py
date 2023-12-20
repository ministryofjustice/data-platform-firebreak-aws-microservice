import json
from typing import Any

import boto3
from fastapi import HTTPException

from app.core.config import get_settings
from app.core.jinja import JsonTemplates

settings = get_settings()


class BaseAWSService:
    @property
    def jinja(self) -> JsonTemplates:
        return JsonTemplates()

    def build_arn(
        self, service: str, resource: str, region: str = "", account: str = settings.aws_account_id
    ) -> str:
        service = service.lower()
        region = region.lower()
        regionless = ["iam", "s3"]
        if service in regionless:
            region = ""

        return f"arn:aws:{service}:{region}:{account}:{resource}"

    def get_client(self, service: str) -> boto3.client:
        return boto3.client(service)


class AWSRolesService(BaseAWSService):
    SERVICE = "iam"

    def __init__(self, rolename: str) -> None:
        super().__init__()
        self.rolename = rolename

    @property
    def client(self) -> boto3.client:
        return self.get_client(self.SERVICE)

    def oidc_arn(self, domain: str) -> str:
        resource = f"oidc-provider/{domain}"
        return self.build_arn(service=self.SERVICE, resource=resource)

    def get_trust_policy_data(self, oidc_user_id: str) -> dict[str, str]:
        template = self.jinja.get_template("roles/trust_policy.json")
        context = {
            "username": self.rolename,
            "oidc_arn": self.oidc_arn(settings.oidc_domain),
            "oidc_domain": settings.oidc_domain,
            "oidc_user_id": oidc_user_id,
            "eks_arn": self.oidc_arn(settings.oidc_eks_provider),
            "oidc_eks_provider": settings.oidc_eks_provider,
        }
        rendered = template.render(**context)
        return json.loads(rendered)

    def create_role(self, oidc_user_id):
        trust_policy = self.get_trust_policy_data(oidc_user_id=oidc_user_id)
        return self.client.create_role(
            RoleName=self.rolename, AssumeRolePolicyDocument=json.dumps(trust_policy)
        )

    def get_policies_for_role(self) -> list[dict]:
        policies: list[dict[str, Any]] = list()
        policies.extend(self._get_inline_policies_for_role())
        policies.extend(self._get_attached_policies_for_role())
        return policies

    def _get_inline_policies_for_role(self) -> list[dict]:
        policies: list[dict[str, Any]] = list()

        inline_policy_response = self.client.list_role_policies(
            RoleName=self.rolename,
        )
        if not inline_policy_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            return HTTPException(status_code=400)

        policy_names = inline_policy_response.get("PolicyNames", [])
        for policy_name in policy_names:
            inline_policy = self.client.get_role_policy(
                RoleName=self.rolename, PolicyName=policy_name
            )

            if not inline_policy["ResponseMetadata"]["HTTPStatusCode"] == 200:
                return HTTPException(status_code=400)

            policies.append(
                {
                    "PolicyName": policy_name,
                    "PolicyDocument": inline_policy.get("PolicyDocument", {}),
                }
            )
        return policies

    def _get_attached_policies_for_role(self) -> list[dict]:
        policies: list[dict[str, Any]] = list()

        response = self.client.list_attached_role_policies(RoleName=self.rolename)
        if not response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            return HTTPException(status_code=400)

        for policy in response.get("AttachedPolicies", []):
            policy_arn: str = policy.get("PolicyArn")
            policy_response: dict = self.client.get_policy(PolicyArn=policy_arn)
            if not policy_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                return HTTPException(status_code=400)
            policies.append(policy_response.get("Policy", {}))
        return policies
