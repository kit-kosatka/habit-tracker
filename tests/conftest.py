import os

os.environ["DATABASE_URL"] = (
    "postgresql+asyncpg://user:password@localhost:5432/habitdb_test"
)

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool
from app.main import app
from app.db.session import get_db

TEST_DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/habitdb_test"


@pytest.fixture(autouse=True)
async def override_db():
    engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    async def get_test_db():
        async with session_maker() as session:
            yield session

    app.dependency_overrides[get_db] = get_test_db
    yield
    await engine.dispose()
    app.dependency_overrides.clear()
