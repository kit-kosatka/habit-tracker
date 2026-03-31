import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_register_success():
    email = f"{uuid.uuid4()}@test.com"
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/auth/register", json={"email": email, "password": "12345678"}
        )
        assert response.status_code == 201


@pytest.mark.asyncio
async def test_register_duplicate():
    email = f"{uuid.uuid4()}@test.com"
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        await client.post(
            "/auth/register", json={"email": email, "password": "12345678"}
        )
        response = await client.post(
            "/auth/register", json={"email": email, "password": "12345678"}
        )
        assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_success():
    email = f"{uuid.uuid4()}@test.com"
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        await client.post(
            "/auth/register", json={"email": email, "password": "12345678"}
        )
        response = await client.post(
            "/auth/login", json={"email": email, "password": "12345678"}
        )
        assert response.status_code == 200
        assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_wrong_password():
    email = f"{uuid.uuid4()}@test.com"
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        await client.post(
            "/auth/register", json={"email": email, "password": "12345678"}
        )
        response = await client.post(
            "/auth/login", json={"email": email, "password": "wrongpassword"}
        )
        assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_habit_with_token():
    email = f"{uuid.uuid4()}@test.com"
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        await client.post(
            "/auth/register", json={"email": email, "password": "12345678"}
        )
        login = await client.post(
            "/auth/login", json={"email": email, "password": "12345678"}
        )
        token = login.json()["access_token"]
        response = await client.post(
            "/habits/create",
            json={"title": "Зарядка"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_habit_without_token():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/habits/create", json={"title": "Зарядка"})
        assert response.status_code == 401
