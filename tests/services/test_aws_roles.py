import json
from unittest.mock import patch

import pytest

from app.core.config import get_settings
from app.core.jinja import JsonTemplates
from app.services.aws_roles import AWSRolesService, BaseAWSService

settings = get_settings()


class TestBaseAWSService:
    @pytest.fixture
    def service(self):
        return BaseAWSService()

    def test_build_arn(self, service):
        expected = "arn:aws:foo:eu-west-1:123456:bar"

        result = service.build_arn(
            service="foo",
            resource="bar",
            region="eu-west-1",
            account="123456",
        )

        assert result == expected

    def test_get_client(self, service):
        with patch("app.services.aws_roles.boto3") as boto3:
            service.get_client("iam")
            boto3.client.assert_called_once_with("iam")

    def test_jinja(self, service):
        assert isinstance(service.jinja, JsonTemplates)


class TestAWSRolesService:
    rolename = "exampleusername"
    oidc_user_id = "user_1234"

    @pytest.fixture
    def service(self):
        return AWSRolesService(rolename=self.rolename)

    @pytest.fixture
    def oidc_arn(self):
        return "arn:aws:iam::123456:oidc-provider/{domain}"

    @pytest.fixture
    def ec2_statement(self):
        jinja = JsonTemplates()
        template = jinja.get_template("roles/trusted_entities/ec2.json")
        return json.loads(template.render())

    @pytest.fixture
    def oidc_statement(self, oidc_arn):
        jinja = JsonTemplates()
        template = jinja.get_template("roles/trusted_entities/oidc.json")
        context = {
            "oidc_user_id": self.oidc_user_id,
            "oidc_domain": settings.oidc_domain,
            "oidc_arn": oidc_arn.format(domain=settings.oidc_domain),
        }
        return json.loads(template.render(**context))

    @pytest.fixture
    def eks_statement(self, oidc_arn):
        jinja = JsonTemplates()
        template = jinja.get_template("roles/trusted_entities/eks.json")
        context = {
            "username": self.username,
            "eks_arn": oidc_arn.format(domain=settings.oidc_eks_provider),
            "oidc_eks_provider": settings.oidc_eks_provider,
        }
        return json.loads(template.render(**context))

    def test_init(self, service):
        assert service.username == self.rolename
        assert service.SERVICE == "iam"

    @pytest.mark.parametrize(
        "domain, expected",
        [
            ("test.oidc.example.com", "arn:aws:iam::123456:oidc-provider/test.oidc.example.com"),
            (
                "test.eks-oidc.example.com",
                "arn:aws:iam::123456:oidc-provider/test.eks-oidc.example.com",
            ),
        ],
    )
    def test_oidc_arn(self, service, domain, expected):
        assert service.oidc_arn(domain=domain) == expected

    def test_get_trust_policy_data(self, service, oidc_statement, eks_statement, ec2_statement):
        result = service.get_trust_policy_data(oidc_user_id=self.oidc_user_id)
        assert oidc_statement in result["Statement"]
        assert eks_statement in result["Statement"]

        assert ec2_statement in result["Statement"]
        assert result["Version"] == "2012-10-17"

    def test_create_role(self, service, oidc_statement, eks_statement, ec2_statement):
        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [
                ec2_statement,
                oidc_statement,
                eks_statement,
            ],
        }
        response = service.create_role()

        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
        assert response["Role"]["RoleName"] == self.rolename
        assert response["Role"]["AssumeRolePolicyDocument"] == trust_policy
