import boto3
import pytest
from moto import mock_iam


@pytest.fixture
def iam_client(autouse=True):
    with mock_iam():
        iam = boto3.client("iam")
        yield iam


@pytest.fixture
def iam_role(iam_client):
    iam = boto3.client("iam")
    return iam.create_role(RoleName="example-role", AssumeRolePolicyDocument="example")