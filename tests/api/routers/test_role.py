from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)


def test_get_roles(get_role_response) -> None:
    response = client.get("/roles/")
    data = response.json()
    assert response.status_code == 200
    assert "RoleName" in data[0].keys()
