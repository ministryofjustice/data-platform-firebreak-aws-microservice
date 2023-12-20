from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.api.main import app


@pytest.fixture
def client():
    """
    Return a test client with authentication patches to pass
    """
    with patch("app.api.auth.VerifyToken.__call__"):
        yield TestClient(app=app, headers={"Authorization": "Bearer testtoken"})


def test_get_roles(create_iam_role, iam_role_name, client) -> None:
    response = client.get("/roles/")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["RoleName"] == iam_role_name


def test_get_role_by_name(create_iam_role, iam_role_name, client) -> None:
    response = client.get(f"/roles/{iam_role_name}/")
    data = response.json()

    assert response.status_code == 200
    assert data["RoleName"] == iam_role_name


def test_get_policies_for_role(
    iam_role_name, attach_iam_role_policy, attach_inline_policy, iam_policy_name, client
):
    response = client.get(f"/roles/{iam_role_name}/policies/")
    data = response.json()

    assert len(data) == 2
    assert response.status_code == 200
    assert data[0]["PolicyName"] == "inline-policy"
    assert data[1]["PolicyName"] == iam_policy_name


def test_create_role(client):
    response = client.post(
        "/roles/",
        json={
            "rolename": "example_user",
            "oidc_user_id": "1234",
        },
    )

    assert response.status_code == 200
    assert response.json()["RoleName"] == "example_user"


@pytest.mark.parametrize(
    "path, method",
    [
        ("/roles/", "get"),
        ("/roles/example-role/", "get"),
        ("/roles/example-role/policies", "get"),
        ("/roles/", "post"),
    ],
)
def test_unathorised_without_auth_header(path, method):
    """
    Check for all urls that without auth header, an unauthorised response is raised
    """
    client = TestClient(app=app)
    response = client.request(method=method, url=path)
    assert response.status_code == 403
