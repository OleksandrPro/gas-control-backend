import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

import pytest
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool
from sqlalchemy import text

from main import app
from database import get_session
from inventory_system.models import Base
from .constants import TestDB

TEST_DATABASE_URL = TestDB.ASYNC_URL

engine_test = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)

TestingSessionLocal = async_sessionmaker(
    bind=engine_test, 
    class_=AsyncSession, 
    expire_on_commit=False
)

@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session
        
        # Cleanup
        table_names = [table.name for table in Base.metadata.sorted_tables]
        
        if table_names:
            tables_str = ", ".join(f'"{name}"' for name in table_names)
            statement = text(f"TRUNCATE TABLE {tables_str} RESTART IDENTITY CASCADE;")
            
            await session.execute(statement)
            await session.commit()

@pytest_asyncio.fixture(scope="function")
async def test_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    
    app.dependency_overrides.clear()