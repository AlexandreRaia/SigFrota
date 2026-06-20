import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_login_invalido(client: AsyncClient):
    response = await client.post("/api/v1/auth/login", json={
        "username": "naoexiste",
        "password": "senhaerrada",
    })
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_sem_token(client: AsyncClient):
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 403
