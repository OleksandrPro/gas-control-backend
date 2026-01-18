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
from datetime import date

from main import app
from database import get_session
from inventory_system.models import (
    Base,
    Card,
    District, 
    PropertyType, 
    ObjectName, 
    PressureType,
    CutType,
    GroundLevel,
    PipeMaterial,
    EquipmentItem,
    PipeData,
    ColumnType
)
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

@pytest_asyncio.fixture(scope="function")
async def seed_lookups(db_session: AsyncSession):
    # Card lookups
    district = District(value="Test District")
    prop_type = PropertyType(value="Test Property")
    obj_name = ObjectName(value="Test Object")
    pressure = PressureType(value="High")
    cut_type = CutType(value="Full")
    
    # Equipment lookups
    ground = GroundLevel(value="Underground")
    material = PipeMaterial(value="Steel")

    db_session.add_all([district, prop_type, obj_name, pressure, cut_type, ground, material])
    await db_session.commit()

    return {
        "district_id": district.id,
        "property_type_id": prop_type.id,
        "object_name_id": obj_name.id,
        "pressure_type_id": pressure.id,
        "cut_type_id": cut_type.id,
        "ground_level_id": ground.id,
        "pipe_material_id": material.id
    }

@pytest_asyncio.fixture(scope="function")
async def card_payload(seed_lookups):
    return {
        "inventory_number": "CARD-001",
        "inventory_number_eskd": "ESKD-001",
        "gas_pipeline_section": "Test Section",
        "described_name": "Test Description",
        "address": "Test Address",
        "folder": "Folder 1",
        "total_length": 100.0,
        "build_date_dn": "2023-01-01",
        
        "district_id": seed_lookups["district_id"],
        "property_type_id": seed_lookups["property_type_id"],
        "object_name_id": seed_lookups["object_name_id"],
        "pressure_type_id": seed_lookups["pressure_type_id"],
        "cut_type_id": seed_lookups["cut_type_id"]
    }

@pytest_asyncio.fixture(scope="function")
async def seed_card(db_session: AsyncSession, card_payload):
    card_data = card_payload.copy()
    if isinstance(card_data["build_date_dn"], str):
        card_data["build_date_dn"] = date.fromisoformat(card_data["build_date_dn"])

    card = Card(**card_data)
    db_session.add(card)
    await db_session.commit()
    await db_session.refresh(card)
    return card

@pytest_asyncio.fixture(scope="function")
async def seed_card_with_equipment(db_session: AsyncSession, seed_card, seed_lookups):
    item = EquipmentItem(
        card_id=seed_card.id,
        item_type="pipe",
        description="Test Pipe"
    )
    db_session.add(item)
    await db_session.commit()
    await db_session.refresh(item)

    pipe_data = PipeData(
        item_id=item.id,
        column_type=ColumnType.BALANCE,
        type="pipe_data",
        diameter=159.0,
        length=50.5,
        groung_level_id=seed_lookups["ground_level_id"],
        material_id=seed_lookups["pipe_material_id"]
    )
    db_session.add(pipe_data)
    await db_session.commit()
    
    return seed_card