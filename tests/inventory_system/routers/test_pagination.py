import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_pagination_logic(test_client, card_factory, seed_lookups):
    for i in range(15):
        await card_factory(
            inv_number_suffix=f"PAG-{i}", 
            cut_type_id=seed_lookups["cut_none_id"]
        )

    response_p1 = await test_client.get("/cards?page=1&size=10")
    assert response_p1.status_code == status.HTTP_200_OK
    data_p1 = response_p1.json()
    
    assert data_p1["total"] == 15
    assert data_p1["current_page"] == 1
    assert data_p1["total_pages"] == 2
    assert len(data_p1["items"]) == 10
    assert data_p1["items"][0]["inventory_number"] == "CARD-PAG-0" 
    assert data_p1["items"][9]["inventory_number"] == "CARD-PAG-9"

    response_p2 = await test_client.get("/cards?page=2&size=10")
    assert response_p2.status_code == status.HTTP_200_OK
    data_p2 = response_p2.json()
    
    assert data_p2["current_page"] == 2
    assert len(data_p2["items"]) == 5
    assert data_p2["items"][0]["inventory_number"] == "CARD-PAG-10"

@pytest.mark.asyncio
async def test_pagination_empty_page(test_client):
    response = await test_client.get("/cards?page=100&size=10")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["items"] == []
    assert data["total"] == 0
    assert data["current_page"] == 100