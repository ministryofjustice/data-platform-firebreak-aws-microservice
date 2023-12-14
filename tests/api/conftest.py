import boto3
import pytest
from moto import mock_iam


@pytest.fixture(autouse=True)
def iam_client():
    with mock_iam():
        iam = boto3.client("iam")
        yield iam


@pytest.fixture
def iam_role_name():
    return "example-iam-role"


@pytest.fixture
def create_iam_role(iam_client, iam_role_name):
    return iam_client.create_role(RoleName=iam_role_name, AssumeRolePolicyDocument="example")
