import pytest
from httpx import AsyncClient, Response


async def get_response(async_client: AsyncClient, uuid: str) -> Response:
    return await async_client.get(
        f"/api/v1/wallets/{uuid}/balance",
    )


@pytest.mark.asyncio
async def test_get_balance(async_client, test_wallet) -> None:
    response = await get_response(async_client, test_wallet.uuid)
    assert response.status_code == 200
    assert response.json().get("wallet_id") == test_wallet.uuid


@pytest.mark.asyncio
@pytest.mark.parametrize("invalid_uuid", ["no_exist_uuid", "1211", ""])
async def test_invalid_uuid(async_client, invalid_uuid) -> None:
    response = await get_response(async_client, invalid_uuid)
    assert (
        response.status_code == 404
    ), f"Expected 404 Not Found, but got {response.status_code}"
    detail = response.json().get("detail")
    assert detail in ("Wallet Not Found", "Not Found")
