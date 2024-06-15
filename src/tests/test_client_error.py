from typing import List
import pytest
from httpx import AsyncClient

import tests.utils as utils


@pytest.mark.asyncio
@pytest.mark.parametrize("client_payloads", [1], indirect=True)
@pytest.mark.parametrize("invalid_gender", ("test",))
async def test_post_client_gender(
    client: AsyncClient, client_payloads: List[dict], invalid_gender: str
) -> None:
    client_payload = client_payloads[0]
    client_payload["gender"] = invalid_gender
    response_create = await client.post(
        "client",
        json=client_payload,
    )
    await utils.check_422_error(response_create, "gender")
