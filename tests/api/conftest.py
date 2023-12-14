import boto3
import pytest
from moto import mock_iam


@pytest.fixture(autouse=True)
def iam_client():
    with mock_iam():
        iam = boto3.client("iam")
        yield iam


@pytest.fixture
def iam_role(iam_client):
    return iam_client.create_role(RoleName="example-role", AssumeRolePolicyDocument="example")
