import json

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
def iam_policy_name():
    return "example-iam-policy"


@pytest.fixture
def create_iam_role(iam_client, iam_role_name):
    return iam_client.create_role(RoleName=iam_role_name, AssumeRolePolicyDocument="example")


@pytest.fixture
def iam_policy_document() -> str:
    return json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": ["s3:ListAllMyBuckets", "s3:GetBucketLocation"],
                    "Resource": "arn:aws:s3:::*",
                },
                {
                    "Effect": "Allow",
                    "Action": "s3:ListBucket",
                    "Resource": "arn:aws:s3:::BUCKET-NAME",
                    "Condition": {
                        "StringLike": {"s3:prefix": ["", "home/", "home/${aws:username}/"]}
                    },
                },
                {
                    "Effect": "Allow",
                    "Action": "s3:*",
                    "Resource": [
                        "arn:aws:s3:::BUCKET-NAME/home/${aws:username}",
                        "arn:aws:s3:::BUCKET-NAME/home/${aws:username}/*",
                    ],
                },
            ],
        }
    )


@pytest.fixture
def create_iam_role_policy(iam_client, iam_policy_name, iam_policy_document):
    return iam_client.create_policy(PolicyName=iam_policy_name, PolicyDocument=iam_policy_document)


@pytest.fixture
def attach_iam_role_policy(iam_client, create_iam_role, create_iam_role_policy, iam_role_name):
    response = create_iam_role_policy
    policy = response.get("Policy")
    return iam_client.attach_role_policy(RoleName=iam_role_name, PolicyArn=policy.get("Arn"))


@pytest.fixture
def attach_inline_policy(iam_client, iam_role_name, iam_policy_name, iam_policy_document):
    return iam_client.put_role_policy(
        PolicyDocument=iam_policy_document,
        PolicyName="inline-policy",
        RoleName=iam_role_name,
    )
