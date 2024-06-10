from datetime import datetime
import random
from typing import List
from httpx import AsyncClient


def random_date() -> str:
    start = datetime(1950, 1, 1)
    end = datetime(2000, 1, 1)
    random_date = start + (end - start) * random.random()
    return random_date.strftime("%Y-%m-%d")


async def create_clients(
    client: AsyncClient, client_payloads: List[dict]
) -> List[dict]:
    for client_payload in client_payloads:
        response_create = await client.post(
            "client",
            json=client_payload,
        )
        assert response_create.status_code == 201
        response_create_json = response_create.json()
        assert "id" in response_create_json
        client_payload["id"] = response_create_json["id"]
        assert client_payload == response_create_json
