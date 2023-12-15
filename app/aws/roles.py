import json

import boto3

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


class AWSRoleService(BaseAWSService):
    SERVICE = "iam"

    def __init__(self, username: str) -> None:
        super().__init__()
        self.username = username

    @property
    def client(self) -> boto3.client:
        return self.get_client(self.SERVICE)

    def oidc_arn(self, domain: str) -> str:
        resource = f"oidc-provider/{domain}"
        return self.build_arn(service=self.SERVICE, resource=resource)

    def get_trust_policy_data(self) -> dict[str, str]:
        template = self.jinja.get_template("roles/trust_policy.json")
        context = {
            "username": self.username,
            "oidc_arn": self.oidc_arn(settings.oidc_domain),
            "oidc_domain": settings.oidc_domain,
            "user_oidc_id": self.username,  # noqa: TODO this should come from the OIDC provider, via /userinfo endpoint
            "eks_arn": self.oidc_arn(settings.oidc_eks_provider),
            "oidc_eks_provider": settings.oidc_eks_provider,
        }
        rendered = template.render(**context)
        return json.loads(rendered)

    def create_role(self):
        trust_policy = self.get_trust_policy_data()
        return self.client.create_role(
            RoleName=self.username, AssumeRolePolicyDocument=json.dumps(trust_policy)
        )
