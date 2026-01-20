import pytest
from fastapi import status

# Helper to generate payloads
def make_payload(column_types: list[str], seed_lookups):
    entries = []
    for c_type in column_types:
        entries.append({
            "column_type": c_type,
            "type": "pipe_data",
            "diameter": 100, "length": 10,
            "material_id": seed_lookups["pipe_material_id"],
            "groung_level_id": seed_lookups["ground_level_id"]
        })
    
    return {
        "item_type": "pipe",
        "description": "Logic Test Pipe",
        "data_entries": entries
    }

# --- SUCCESS CASES ---

@pytest.mark.asyncio
@pytest.mark.parametrize("cut_key, required_columns", [
    ("cut_none_id", ["balance", "fact"]),       # Case 1: No Cut -> Balance + Fact
    ("cut_full_id", ["balance", "cut"]),        # Case 2: Full Cut -> Balance + Cut
    ("cut_partial_id", ["balance", "fact", "cut"]), # Case 3: Partial -> All three
])
async def test_create_equipment_success_scenarios(
    test_client, card_factory, seed_lookups, cut_key, required_columns
):
    # If cut_key is None, we pass None (for No Cut scenario if mapped that way)
    # But here we use explicit IDs from seed_lookups
    cut_id = seed_lookups.get(cut_key)
    card = await card_factory(cut_type_id=cut_id, inv_number_suffix=cut_key)

    payload = make_payload(required_columns, seed_lookups)

    response = await test_client.post(f"/cards/{card.id}/equipment", json=payload)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["data_entries"]) == len(required_columns)


# --- FAILURE CASES ---

@pytest.mark.asyncio
async def test_create_equipment_empty_entries_fails(test_client, card_factory, seed_lookups):
    """
    Test that empty data_entries list is rejected.
    """
    card = await card_factory(cut_type_id=seed_lookups["cut_full_id"], inv_number_suffix="empty")
    
    payload = {
        "item_type": "pipe",
        "description": "Empty Test",
        "data_entries": [] # Empty!
    }
    
    response = await test_client.post(f"/cards/{card.id}/equipment", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid data structure" in response.json()["detail"]

@pytest.mark.asyncio
async def test_create_equipment_duplicate_types_fails(test_client, card_factory, seed_lookups):
    """
    Test that duplicate column types (e.g. 2x Balance) are rejected.
    """
    card = await card_factory(cut_type_id=seed_lookups["cut_full_id"], inv_number_suffix="dup")

    payload = make_payload(["balance", "balance"], seed_lookups)
    
    response = await test_client.post(f"/cards/{card.id}/equipment", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Duplicate column types" in response.json()["detail"]

@pytest.mark.asyncio
@pytest.mark.parametrize("cut_key, wrong_columns", [
    ("cut_none_id", ["balance", "cut"]),  # No Cut cannot have CUT
    ("cut_full_id", ["balance", "fact"]), # Full Cut cannot have FACT (based on our rules)
    ("cut_partial_id", ["balance", "cut"]), # Partial must have ALL 3 (missing fact)
])
async def test_create_equipment_wrong_combination_fails(
    test_client, card_factory, seed_lookups, cut_key, wrong_columns
):
    """
    Test that invalid combinations of columns are rejected based on card type.
    """
    cut_id = seed_lookups.get(cut_key)
    card = await card_factory(cut_type_id=cut_id, inv_number_suffix=f"fail_{cut_key}")

    payload = make_payload(wrong_columns, seed_lookups)

    response = await test_client.post(f"/cards/{card.id}/equipment", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid data structure" in response.json()["detail"]