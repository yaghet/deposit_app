from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient
from main import app

from app.db.models import Wallet
from app.db.session import AsyncSessionLocal


@pytest.fixture(scope="session")
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client


@pytest.fixture(scope="session")
async def test_wallet():
    async with AsyncSessionLocal() as session:
        wallet = Wallet(uuid=str(uuid4()), balance=0)
        session.add(wallet)
        await session.commit()
        await session.refresh(wallet)
        yield wallet
        await session.delete(wallet)
        await session.commit()
