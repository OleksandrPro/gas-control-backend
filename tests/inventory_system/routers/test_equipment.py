import pytest
from sqlalchemy import select
from sqlalchemy.orm import selectinload, selectin_polymorphic
from fastapi import status

from inventory_system.models import EquipmentItem, PipeData, EquipmentData, ValveData

def get_valid_full_cut_entries(seed_lookups, item_type="pipe"):
    if item_type == "pipe":
        base = {
            "type": "pipe_data", 
            "diameter": 100, "length": 10,
            "material_id": seed_lookups["pipe_material_id"],
            "groung_level_id": seed_lookups["ground_level_id"]
        }
    else: # valve
        base = {
            "type": "valve_data",
            "diameter": 50, "quantity": 5,
            "model_number": "V-123"
        }

    return [
        {**base, "column_type": "balance"},
        {**base, "column_type": "cut"}
    ]

@pytest.mark.asyncio
async def test_create_pipe_persistence(test_client, db_session, seed_card, seed_lookups):
    """
    Test verifying that complex polymorphic data is actually stored in the DB tables.
    """
    card_id = seed_card.id

    payload = {
        "item_type": "pipe",
        "description": "Main Gas Pipe",
        "data_entries": get_valid_full_cut_entries(seed_lookups, "pipe")
    }

    response = await test_client.post(f"/cards/{card_id}/equipment", json=payload)

    assert response.status_code == status.HTTP_200_OK, f"Error details: {response.json()}"
    created_id = response.json()["id"]

    query = select(EquipmentItem).where(EquipmentItem.id == created_id).options(
        selectinload(EquipmentItem.data_entries).selectin_polymorphic([PipeData, ValveData])
    )
    
    result = await db_session.execute(query)
    item_in_db = result.scalar_one_or_none()

    assert item_in_db is not None
    assert item_in_db.item_type == "pipe"
    assert item_in_db.card_id == card_id
    
    assert len(item_in_db.data_entries) == 2
    data_entry = item_in_db.data_entries[0]
    
    assert isinstance(data_entry, EquipmentData)
    assert data_entry.type == "pipe_data"
    assert data_entry.material_id == seed_lookups["pipe_material_id"]

@pytest.mark.asyncio
async def test_get_equipment_via_api(test_client, seed_card, seed_lookups):
    card_id = seed_card.id

    payload = {
        "item_type": "pipe",
        "description": "Test Pipe",
        "data_entries": get_valid_full_cut_entries(seed_lookups, "pipe")
    }
    
    response = await test_client.post(f"/cards/{card_id}/equipment", json=payload)

    assert response.status_code == status.HTTP_200_OK, f"Error details: {response.json()}"

    response = await test_client.get(f"/cards/{card_id}/equipment")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["item_type"] == "pipe"
    assert data[0]["data_entries"][0]["length"] == 10

@pytest.mark.asyncio
async def test_update_equipment_data(test_client, seed_card, seed_lookups):
    card_id = seed_card.id
    create_payload = {
        "item_type": "pipe",
        "description": "Update Test Pipe",
        "data_entries": get_valid_full_cut_entries(seed_lookups, "pipe")
    }
    create_resp = await test_client.post(f"/cards/{card_id}/equipment", json=create_payload)
    assert create_resp.status_code == status.HTTP_200_OK, f"Error: {create_resp.json()}"
    
    data_id = create_resp.json()["data_entries"][0]["id"]

    new_length = 999.9
    patch_resp = await test_client.patch(f"/equipment-data/{data_id}", json={"length": new_length})
    
    assert patch_resp.status_code == status.HTTP_200_OK
    assert patch_resp.json()["length"] == new_length

    get_resp = await test_client.get(f"/cards/{card_id}/equipment")
    assert get_resp.json()[0]["data_entries"][0]["length"] == new_length

@pytest.mark.asyncio
async def test_delete_equipment_item(test_client, seed_card, seed_lookups):
    card_id = seed_card.id
    payload = {
        "item_type": "pipe", 
        "description": "Delete Test Pipe",
        "data_entries": get_valid_full_cut_entries(seed_lookups, "pipe")
    } 
    resp = await test_client.post(f"/cards/{card_id}/equipment", json=payload)
    assert resp.status_code == status.HTTP_200_OK, f"Error: {resp.json()}"
    
    item_id = resp.json()["id"]

    del_resp = await test_client.delete(f"/equipment-items/{item_id}")
    assert del_resp.status_code == status.HTTP_204_NO_CONTENT

    get_resp = await test_client.get(f"/cards/{card_id}/equipment")
    assert len(get_resp.json()) == 0

@pytest.mark.asyncio
async def test_create_valve_polymorphism(test_client, seed_card, seed_lookups):
    card_id = seed_card.id
    payload = {
        "item_type": "valve",
        "description": "Valve Check",
        "data_entries": get_valid_full_cut_entries(seed_lookups, "valve")
    }

    response = await test_client.post(f"/cards/{card_id}/equipment", json=payload)
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["item_type"] == "valve"
    assert data["data_entries"][0]["quantity"] == 5
    assert "length" not in data["data_entries"][0]
