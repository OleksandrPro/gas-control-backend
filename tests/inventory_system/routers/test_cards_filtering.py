import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_filter_cards_by_multiple_districts(test_client, card_factory, seed_lookups):
    dist_1_id = seed_lookups["district_id"]

    dist_2_resp = await test_client.post("/dictionaries/districts", json={"value": "District 2"})
    assert dist_2_resp.status_code == status.HTTP_200_OK
    dist_2_id = dist_2_resp.json()["id"]
    
    dist_3_resp = await test_client.post("/dictionaries/districts", json={"value": "District 3"})
    assert dist_3_resp.status_code == status.HTTP_200_OK
    dist_3_id = dist_3_resp.json()["id"]
    
    card_a = await card_factory(inv_number_suffix="A", cut_type_id=seed_lookups["cut_none_id"]) 
    
    card_b = await card_factory(inv_number_suffix="B", cut_type_id=seed_lookups["cut_none_id"])
    await test_client.patch(f"/cards/{card_b.id}", json={"district_id": dist_2_id})
    
    card_c = await card_factory(inv_number_suffix="C", cut_type_id=seed_lookups["cut_none_id"])
    await test_client.patch(f"/cards/{card_c.id}", json={"district_id": dist_3_id})

    initial_response = await test_client.get("/cards")
    assert initial_response.status_code == status.HTTP_200_OK
    assert initial_response.json()["total"] == 3

    query_string = f"district_id={dist_1_id}&district_id={dist_3_id}"
    
    response = await test_client.get(f"/cards?{query_string}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert len(data["items"]) == 2
    
    found_ids = [item["id"] for item in data["items"]]
    
    print(f"Found card IDs: {found_ids}. Looking for {card_a.id} and {card_c.id}, excluding {card_b.id}.")
    
    assert card_a.id in found_ids
    assert card_c.id in found_ids
    assert card_b.id not in found_ids


@pytest.mark.asyncio
async def test_filter_cards_by_multiple_folders(test_client, card_factory, seed_lookups):
    folder_1 = "F1"
    folder_2 = "F2"
    folder_3 = "F3"

    c1 = await card_factory(inv_number_suffix="100", cut_type_id=seed_lookups["cut_none_id"])
    await test_client.patch(f"/cards/{c1.id}", json={"folder": folder_1})

    c2 = await card_factory(inv_number_suffix="101", cut_type_id=seed_lookups["cut_none_id"])
    await test_client.patch(f"/cards/{c2.id}", json={"folder": folder_1})

    c3 = await card_factory(inv_number_suffix="200", cut_type_id=seed_lookups["cut_none_id"])
    await test_client.patch(f"/cards/{c3.id}", json={"folder": folder_2})

    c4 = await card_factory(inv_number_suffix="300", cut_type_id=seed_lookups["cut_none_id"])
    await test_client.patch(f"/cards/{c4.id}", json={"folder": folder_3})
    
    resp = await test_client.get(f"/cards?folder={folder_1}&folder={folder_2}")
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    
    assert data["total"] == 3
    found_ids = [i["id"] for i in data["items"]]
    
    assert c1.id in found_ids
    assert c2.id in found_ids
    assert c3.id in found_ids
    assert c4.id not in found_ids


@pytest.mark.asyncio
async def test_filter_cards_by_multiple_property_types(test_client, card_factory, seed_lookups):
    prop_A_id = seed_lookups["property_type_id"]
    
    prop_B_resp = await test_client.post("/dictionaries/property-types", json={"value": "Prop B"})
    prop_B_id = prop_B_resp.json()["id"]

    c1 = await card_factory(inv_number_suffix="1", cut_type_id=seed_lookups["cut_none_id"])

    c2 = await card_factory(inv_number_suffix="2", cut_type_id=seed_lookups["cut_none_id"])
    await test_client.patch(f"/cards/{c2.id}", json={"property_type_id": prop_B_id})
    
    resp = await test_client.get(f"/cards?property_type_id={prop_B_id}")
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    
    assert data["total"] == 1
    found_ids = [i["id"] for i in data["items"]]
    
    assert c2.id in found_ids
    assert c1.id not in found_ids


@pytest.mark.asyncio
async def test_filter_cards_by_multiple_inventory_numbers(test_client, card_factory, seed_lookups):
    card_a = await card_factory(inv_number_suffix="A", cut_type_id=seed_lookups["cut_none_id"])
    card_b = await card_factory(inv_number_suffix="B", cut_type_id=seed_lookups["cut_none_id"])
    card_c = await card_factory(inv_number_suffix="C", cut_type_id=seed_lookups["cut_none_id"])
    
    query = f"inventory_number={card_a.inventory_number}&inventory_number={card_c.inventory_number}"
    
    resp = await test_client.get(f"/cards?{query}")
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    
    assert data["total"] == 2
    found_ids = [i["id"] for i in data["items"]]
    
    assert card_a.id in found_ids
    assert card_c.id in found_ids
    assert card_b.id not in found_ids


@pytest.mark.asyncio
async def test_filter_cards_by_inventory_number_like(test_client, card_factory, seed_lookups):
    c1 = await card_factory(inv_number_suffix="TEST-1", cut_type_id=seed_lookups["cut_none_id"])
    c2 = await card_factory(inv_number_suffix="TEST-2", cut_type_id=seed_lookups["cut_none_id"])
    c3 = await card_factory(inv_number_suffix="OTHER", cut_type_id=seed_lookups["cut_none_id"])
    
    resp = await test_client.get("/cards?inventory_number_like=TEST")
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    
    assert data["total"] == 2
    found_ids = [i["id"] for i in data["items"]]
    
    assert c1.id in found_ids
    assert c2.id in found_ids
    assert c3.id not in found_ids


@pytest.mark.asyncio
async def test_filter_cards_by_multiple_cut_types(test_client, card_factory, seed_lookups):
    cut_none = seed_lookups["cut_none_id"]
    cut_full = seed_lookups["cut_full_id"]
    cut_partial = seed_lookups["cut_partial_id"]

    c1 = await card_factory(inv_number_suffix="NONE", cut_type_id=cut_none)
    c2 = await card_factory(inv_number_suffix="FULL", cut_type_id=cut_full)
    c3 = await card_factory(inv_number_suffix="PARTIAL", cut_type_id=cut_partial)
    
    resp = await test_client.get(f"/cards?cut_type_id={cut_none}&cut_type_id={cut_full}")
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    
    assert data["total"] == 2
    found_ids = [i["id"] for i in data["items"]]
    
    assert c1.id in found_ids
    assert c2.id in found_ids
    assert c3.id not in found_ids


@pytest.mark.asyncio
async def test_filter_cards_complex_combination(test_client, card_factory, seed_lookups):
    dist_1_id = seed_lookups["district_id"]
    
    dist_2_resp = await test_client.post("/dictionaries/districts", json={"value": "Dist 2"})
    dist_2_id = dist_2_resp.json()["id"]

    c1 = await card_factory(inv_number_suffix="COMMON-1", cut_type_id=seed_lookups["cut_none_id"])
    
    c2 = await card_factory(inv_number_suffix="COMMON-2", cut_type_id=seed_lookups["cut_none_id"])
    await test_client.patch(f"/cards/{c2.id}", json={"district_id": dist_2_id})
    
    c3 = await card_factory(inv_number_suffix="DIFFERENT", cut_type_id=seed_lookups["cut_none_id"])

    query = f"inventory_number_like=COMMON&district_id={dist_1_id}"
    resp = await test_client.get(f"/cards?{query}")
    
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    
    assert data["total"] == 1
    found_ids = [i["id"] for i in data["items"]]
    
    assert c1.id in found_ids
    assert c2.id not in found_ids
    assert c3.id not in found_ids