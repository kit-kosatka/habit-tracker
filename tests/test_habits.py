import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_get_habits():
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
        response = await client.get(
            "/habits/read", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_habit():
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
        create = await client.post(
            "/habits/create",
            json={"title": "Зарядка"},
            headers={"Authorization": f"Bearer {token}"},
        )
        habit_id = create.json()["id"]
        response = await client.get(
            f"/habits/read/{habit_id}", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_update():
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
        create = await client.post(
            "/habits/create",
            json={"title": "Зарядка"},
            headers={"Authorization": f"Bearer {token}"},
        )
        habit_id = create.json()["id"]
        response = await client.put(
            f"/habits/update/{habit_id}",
            json={"title": "Проверка", "description": "тест"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_habit():
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
        create = await client.post(
            "/habits/create",
            json={"title": "Зарядка"},
            headers={"Authorization": f"Bearer {token}"},
        )
        habit_id = create.json()["id"]
        response = await client.delete(
            f"/habits/delete/{habit_id}", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
