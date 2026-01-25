import pytest
from fastapi import status
import json

@pytest.mark.asyncio
async def test_get_all_cards(test_client):
    response = await test_client.get("/cards")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0

@pytest.mark.asyncio
async def test_get_card(test_client, seed_card):    
    response = await test_client.get(f"/cards/{seed_card.id}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["inventory_number"] == seed_card.inventory_number
    assert data["district_id"] == seed_card.district_id
    assert data["total_length"] == seed_card.total_length

@pytest.mark.asyncio
async def test_create_card_persistence(test_client, card_payload):
    response = await test_client.post("/cards", json=card_payload)
    
    assert response.status_code == status.HTTP_200_OK
    new_id = response.json()["id"]

    get_response = await test_client.get(f"/cards/{new_id}")
    
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json()["inventory_number"] == card_payload["inventory_number"]

@pytest.mark.asyncio
async def test_create_card_with_invalid_payload(test_client, card_payload):
    invalid_payload = card_payload.copy()
    del invalid_payload["inventory_number"]
    response = await test_client.post("/cards", json=invalid_payload)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

@pytest.mark.asyncio
async def test_update_card(test_client, seed_card):
    new_address = "Updated Address 123"

    response = await test_client.patch(
        f"/cards/{seed_card.id}", 
        json={"address": new_address}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["address"] == new_address
    assert data["inventory_number"] == seed_card.inventory_number

@pytest.mark.asyncio
async def test_delete_card(test_client, seed_card):
    del_response = await test_client.delete(f"/cards/{seed_card.id}")
    assert del_response.status_code == status.HTTP_204_NO_CONTENT
    
    get_response = await test_client.get(f"/cards/{seed_card.id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_create_duplicate_card_fails(test_client, seed_card, card_payload):
    payload = card_payload.copy()
    payload["inventory_number"] = seed_card.inventory_number 
    
    response = await test_client.post("/cards", json=payload)

    assert response.status_code == status.HTTP_409_CONFLICT
