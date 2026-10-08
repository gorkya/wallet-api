import uuid
from decimal import Decimal

import pytest

URL = "/api/v1/wallets"


async def test_create_wallet(client):
    response = await client.post(URL)

    assert response.status_code == 201
    assert Decimal(response.json()["balance"]) == 0


async def test_get_wallet(client, wallet):
    response = await client.get(f"{URL}/{wallet.id}")

    assert response.status_code == 200
    assert response.json()["id"] == str(wallet.id)


async def test_get_unknown_wallet_returns_404(client):
    response = await client.get(f"{URL}/{uuid.uuid4()}")

    assert response.status_code == 404


async def test_get_wallet_with_invalid_uuid_returns_422(client):
    response = await client.get(f"{URL}/not-a-uuid")

    assert response.status_code == 422


async def test_deposit_and_withdraw(client, wallet):
    url = f"{URL}/{wallet.id}/operation"

    response = await client.post(
        url, json={"operation_type": "DEPOSIT", "amount": 100}
    )
    assert response.status_code == 200
    assert Decimal(response.json()["balance"]) == 100

    response = await client.post(
        url, json={"operation_type": "WITHDRAW", "amount": 40}
    )
    assert response.status_code == 200
    assert Decimal(response.json()["balance"]) == 60

    response = await client.get(f"{URL}/{wallet.id}")
    assert Decimal(response.json()["balance"]) == 60


async def test_withdraw_more_than_balance_returns_409(client, wallet):
    response = await client.post(
        f"{URL}/{wallet.id}/operation",
        json={"operation_type": "WITHDRAW", "amount": 1},
    )

    assert response.status_code == 409


async def test_operation_on_unknown_wallet_returns_404(client):
    response = await client.post(
        f"{URL}/{uuid.uuid4()}/operation",
        json={"operation_type": "DEPOSIT", "amount": 1},
    )

    assert response.status_code == 404


@pytest.mark.parametrize(
    "body",
    [
        {"operation_type": "DEPOSIT", "amount": 0},
        {"operation_type": "DEPOSIT", "amount": -5},
        {"operation_type": "DEPOSIT", "amount": 1.234},
        {"operation_type": "TRANSFER", "amount": 10},
        {"operation_type": "DEPOSIT"},
        {"amount": 10},
    ],
)
async def test_invalid_operation_body_returns_422(client, wallet, body):
    response = await client.post(f"{URL}/{wallet.id}/operation", json=body)

    assert response.status_code == 422
