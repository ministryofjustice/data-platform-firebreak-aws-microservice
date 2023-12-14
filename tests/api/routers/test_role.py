from fastapi.testclient import TestClient

from app.api.main import app


def test_get_roles(iam_role) -> None:
    client = TestClient(app)
    response = client.get("/roles/")

    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["RoleName"] == "example-role"
