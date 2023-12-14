from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)


def test_get_roles(create_iam_role, iam_role_name) -> None:
    response = client.get("/roles/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["RoleName"] == iam_role_name


def test_get_role_by_name(create_iam_role, iam_role_name) -> None:
    response = client.get(f"/roles/{iam_role_name}/")
    data = response.json()

    assert response.status_code == 200
    assert data["RoleName"] == iam_role_name
