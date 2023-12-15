import json

from jinja2 import Environment, PackageLoader

from app.core.config import get_settings

settings = get_settings()


class JsonTemplates(Environment):
    def __init__(self, *args, **kwargs):
        kwargs["loader"] = PackageLoader("app", "templates")
        super().__init__(*args, **kwargs)
        self.filters["jsonify"] = json.dumps

    def arn(
        self, service: str, resource: str, region: str = "", account: str = settings.aws_account_id
    ):
        service = service.lower()
        region = region.lower()
        regionless = ["iam", "s3"]
        if service in regionless:
            region = ""

        return f"arn:aws:{service}:{region}:{account}:{resource}"

    def oidc_arn(self, domain: str):
        resource = f"oidc-provider/{domain}"
        return self.arn(service="iam", resource=resource)

    def get_trust_policy_data(self, username):
        template = self.get_template("roles/trust_policy.json")
        context = {
            "username": username,
            "oidc_arn": self.oidc_arn(settings.oidc_domain),
            "oidc_domain": settings.oidc_domain,
            "user_oidc_id": username,  # TODO where should this come from?
            "eks_arn": self.oidc_arn(settings.oidc_eks_provider),
            "oidc_eks_provider": settings.oidc_eks_provider,
        }
        rendered = template.render(**context)
        return json.loads(rendered)
