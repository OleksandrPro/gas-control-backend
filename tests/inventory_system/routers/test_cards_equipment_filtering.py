import pytest
from fastapi import status

# Helper to quickly add a pipe to a card via API
async def add_pipe_to_card(
    client, 
    card_id: int, 
    material_id: int, 
    diameter: float, 
    entries_config: list = None
):
    """
    Adds pipe with customizable entries to pass validation.
    Default: Balance + Fact (for No Cut cards).
    """
    if entries_config is None:
        # Default set for "No Cut" cards
        entries_config = ["balance", "fact"]

    data_entries = []
    for col_type in entries_config:
        data_entries.append({
            "column_type": col_type,
            "type": "pipe_data",
            "diameter": diameter,
            "length": 10.0,
            "material_id": material_id,
            "groung_level_id": 1
        })

    payload = {
        "item_type": "pipe",
        "description": f"Pipe d{diameter}",
        "data_entries": data_entries
    }
    resp = await client.post(f"/cards/{card_id}/equipment", json=payload)
    assert resp.status_code == status.HTTP_200_OK, f"Add pipe failed: {resp.json()}"

@pytest.mark.asyncio
async def test_filter_cards_by_pipe_material(test_client, card_factory, seed_lookups):
    """
    Test finding cards that contain pipes of a specific material.
    """
    # 1. Setup Materials
    mat_steel_id = seed_lookups["pipe_material_id"]
    
    # Create a new material "Plastic"
    resp = await test_client.post("/dictionaries/pipe-materials", json={"value": "Plastic"})
    mat_plastic_id = resp.json()["id"]

    # 2. Setup Cards
    # Card A: Has Steel Pipe
    card_a = await card_factory(inv_number_suffix="STEEL", cut_type_id=seed_lookups["cut_none_id"])
    await add_pipe_to_card(test_client, card_a.id, mat_steel_id, 100)

    # Card B: Has Plastic Pipe
    card_b = await card_factory(inv_number_suffix="PLASTIC", cut_type_id=seed_lookups["cut_none_id"])
    await add_pipe_to_card(test_client, card_b.id, mat_plastic_id, 100)

    # Card C: No pipes (Empty)
    card_c = await card_factory(inv_number_suffix="EMPTY", cut_type_id=seed_lookups["cut_none_id"])

    # 3. Filter by Steel
    # Should return only Card A
    resp = await test_client.get(f"/cards?pipe_material_id={mat_steel_id}")
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    
    found_ids = [i["id"] for i in data["items"]]
    assert card_a.id in found_ids
    assert card_b.id not in found_ids
    assert card_c.id not in found_ids

@pytest.mark.asyncio
async def test_filter_cards_by_pipe_diameter(test_client, card_factory, seed_lookups):
    """
    Test filtering by diameter range (min, max, equal).
    """
    mat_id = seed_lookups["pipe_material_id"]

    # Card 100: d=100
    c100 = await card_factory(inv_number_suffix="D100", cut_type_id=seed_lookups["cut_none_id"])
    await add_pipe_to_card(test_client, c100.id, mat_id, 100.0)

    # Card 200: d=200
    c200 = await card_factory(inv_number_suffix="D200", cut_type_id=seed_lookups["cut_none_id"])
    await add_pipe_to_card(test_client, c200.id, mat_id, 200.0)

    # Card 300: d=300
    c300 = await card_factory(inv_number_suffix="D300", cut_type_id=seed_lookups["cut_none_id"])
    await add_pipe_to_card(test_client, c300.id, mat_id, 300.0)

    # Test A: Exact match (d=200)
    resp = await test_client.get("/cards?pipe_diameter_equal=200")
    ids = [i["id"] for i in resp.json()["items"]]
    assert c200.id in ids
    assert c100.id not in ids
    assert c300.id not in ids

    # Test B: Min diameter (>= 200) -> Should be 200 and 300
    resp = await test_client.get("/cards?pipe_diameter_min=200")
    ids = [i["id"] for i in resp.json()["items"]]
    assert c200.id in ids
    assert c300.id in ids
    assert c100.id not in ids

    # Test C: Range (150 <= d <= 250) -> Should be 200 only
    resp = await test_client.get("/cards?pipe_diameter_min=150&pipe_diameter_max=250")
    ids = [i["id"] for i in resp.json()["items"]]
    assert c200.id in ids
    assert c100.id not in ids
    assert c300.id not in ids

@pytest.mark.asyncio
async def test_filter_cards_by_data_column_type(test_client, card_factory, seed_lookups):
    """
    Test filtering by data context (Fact vs Cut).
    """
    mat_id = seed_lookups["pipe_material_id"]

    # Card A: No Cut (Has Balance + Fact, NO Cut)
    card_a = await card_factory(inv_number_suffix="NO_CUT", cut_type_id=seed_lookups["cut_none_id"])
    await add_pipe_to_card(test_client, card_a.id, mat_id, 100, entries_config=["balance", "fact"])

    # Card B: Full Cut (Has Balance + Cut, NO Fact)
    card_b = await card_factory(inv_number_suffix="FULL_CUT", cut_type_id=seed_lookups["cut_full_id"])
    await add_pipe_to_card(test_client, card_b.id, mat_id, 100, entries_config=["balance", "cut"])

    # 1. Filter: Cards that have 'FACT' data
    # Should find Card A (No Cut), but NOT Card B (Full Cut)
    resp = await test_client.get("/cards?column_type=fact")
    assert resp.status_code == status.HTTP_200_OK
    ids = [i["id"] for i in resp.json()["items"]]
    assert card_a.id in ids
    assert card_b.id not in ids

    # 2. Filter: Cards that have 'CUT' data
    # Should find Card B, but NOT Card A
    resp = await test_client.get("/cards?column_type=cut")
    ids = [i["id"] for i in resp.json()["items"]]
    assert card_b.id in ids
    assert card_a.id not in ids