from fastapi.testclient import TestClient

from shopAPI.server import app

client = TestClient(app)


def test_post_client(client: TestClient) -> None:
    response = client.post(
        "/api/v1/client",
        json={
            "client_name": "test_name",
            "client_surname": "test_username",
            "birthday": "2000-01-01",
            "gender": "M",
            "address": {
                "country": "test_country",
                "city": "test_city",
                "street": "test_street",
            },
        },
    )
    assert response.status_code == 201
