import json

from jinja2 import Environment, PackageLoader


class JsonTemplates(Environment):
    def __init__(self, *args, **kwargs):
        kwargs["loader"] = PackageLoader("app", "templates")
        super().__init__(*args, **kwargs)
        self.filters["jsonify"] = json.dumps

    def get_trust_policy_data(self, username):
        template = self.get_template("roles/trust_policy.json")
        context = {
            "username": username,
            "oidc_arn": "",
            "oidc_domain": "",
            "user_oidc_id": "",
            "eks_arn": "",
            "oidc_eks_provider": "",
        }
        rendered = template.render(**context)
        return json.loads(rendered)
