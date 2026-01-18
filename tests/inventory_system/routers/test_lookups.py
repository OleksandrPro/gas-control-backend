import pytest
from fastapi import status
import json

ENDPOINT_PREFIX="dictionaries/"
DISTRICT_BASE = f"{ENDPOINT_PREFIX}districts"

@pytest.mark.asyncio
async def test_get_zero_districts_from_empty_db(test_client):
    response = await test_client.get(DISTRICT_BASE)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

@pytest.mark.asyncio
async def test_get_zero_districts_from_empty_db_2(test_client):
    response = await test_client.get("/dictionaries/districts")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

@pytest.mark.asyncio
async def test_add_district(test_client):
    response = await test_client.post(DISTRICT_BASE, json={"value": "Test District"})
    assert response.status_code == status.HTTP_200_OK
    created_district = response.json()
    assert created_district.get("value") == "Test District"

@pytest.mark.asyncio
async def test_delete_used_district_fails(test_client, seed_card):
    district_id = seed_card.district_id
    
    response = await test_client.delete(f"/dictionaries/districts/{district_id}")
    
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "in use" in response.json()["detail"]

@pytest.mark.asyncio
async def test_create_duplicate_district_returns_existing(test_client):
    resp1 = await test_client.post("/dictionaries/districts", json={"value": "Unique District"})
    assert resp1.status_code == status.HTTP_200_OK
    id1 = resp1.json()["id"]

    resp2 = await test_client.post("/dictionaries/districts", json={"value": "Unique District"})
    assert resp2.status_code == status.HTTP_200_OK
    id2 = resp2.json()["id"]

    assert id1 == id2
