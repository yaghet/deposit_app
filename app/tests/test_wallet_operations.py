from decimal import Decimal
from typing import Union

import pytest
from httpx import AsyncClient, Response

TEST_OPERATION_DATA = {"amount": 100.00, "operation_type": "DEPOSIT"}


async def post_operation(
    async_client: AsyncClient,
    wallet_uuid: str,
    json_data: dict[str, Union[Decimal, str]],
) -> Response:
    return await async_client.post(
        f"/api/v1/wallets/{wallet_uuid}/operation",
        json=json_data,
    )


@pytest.mark.asyncio
async def test_create_deposit_success(async_client: AsyncClient, test_wallet):
    response = await post_operation(async_client, test_wallet.uuid, TEST_OPERATION_DATA)

    assert (
        response.status_code == 200
    ), f"Expected 200 OK, but got {response.status_code}"
    data = response.json()
    assert data.get("wallet_id") == test_wallet.uuid, "Walled ID mismatch"
    assert data.get("balance") == "100.00", "Balance mismatch"


@pytest.mark.asyncio
@pytest.mark.parametrize("invalid_uuid", ["invalid-uuid", "1111", ""])
async def test_invalid_uuid(async_client, invalid_uuid):
    response = await post_operation(async_client, invalid_uuid, TEST_OPERATION_DATA)

    assert (
        response.status_code == 404
    ), f"Expected 404 for invalid UUID, but got {response.status_code}"
    detail = response.json().get("detail")
    assert detail in (
        "Wallet Not Found",
        "Not Found",
    ), f"Unexpected detail message {detail}"


@pytest.mark.asyncio
async def test_invalid_body(async_client, test_wallet):
    invalid_operation_body = {
        "No_exist_field": 100,
        "invalid_field_name_price": 100.00,
    }
    response = await post_operation(
        async_client, test_wallet.uuid, invalid_operation_body
    )

    assert (
        response.status_code == 422
    ), f"Expected 422 Unprocessable Entity, but got {response.status_code}"
    data = response.json()
    assert "detail" in data, f"Response messing detail field"


@pytest.mark.asyncio
async def test_reduce_balance_to_minus(async_client, test_wallet):
    test_data = {"amount": 1000.00, "operation_type": "WITHDRAW"}
    response = await post_operation(async_client, test_wallet.uuid, json_data=test_data)

    assert (
        response.status_code == 400
    ), f"Expected 400 Bad request, but got {response.status_code}"
    detail = response.json().get("detail")
    assert detail == "Insufficient funds", f"Detail must be Insufficient funds"
