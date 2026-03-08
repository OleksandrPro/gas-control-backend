import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_analytics_total_sum(test_client, analytics_data):
    """Test sum of all pipes without filters."""
    expected_total = analytics_data["len_c1"] + analytics_data["len_c2"] + analytics_data["len_c3"]
    
    resp = await test_client.get("/analytics/pipes-length")
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    
    assert data["total_length"] == expected_total
    assert data["count_cards"] == analytics_data["total_cards"]

@pytest.mark.asyncio
async def test_analytics_filter_by_district(test_client, analytics_data):
    """Test filtering by District (should include C1 and C2)."""
    dist_1 = analytics_data["dist_1"]
    expected_total = analytics_data["len_c1"] + analytics_data["len_c2"]
    
    resp = await test_client.get(f"/analytics/pipes-length?district_id={dist_1}")
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    
    assert data["total_length"] == expected_total
    assert data["count_cards"] == 2

@pytest.mark.asyncio
async def test_analytics_filter_by_material(test_client, analytics_data):
    """Test filtering by Material Steel (should include C1 and C3)."""
    mat_steel = analytics_data["mat_steel_id"]
    expected_total = analytics_data["len_c1"] + analytics_data["len_c3"]
    
    resp = await test_client.get(f"/analytics/pipes-length?pipe_material_id={mat_steel}")
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    
    assert data["total_length"] == expected_total
    assert data["count_cards"] == 2

@pytest.mark.asyncio
async def test_analytics_filter_by_column_type_balance(test_client, analytics_data):
    """Test filtering by 'balance' column. Should sum lengths only from balance entries."""
    # C1 (Balance=50), C2 (Balance=0), C3 (Balance=20)
    expected_total = analytics_data["len_c1"] + analytics_data["len_c3"]
    
    resp = await test_client.get("/analytics/pipes-length?column_type=balance")
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    
    assert data["total_length"] == expected_total
    # Count includes all cards that have a balance entry (even if 0 length)
    assert data["count_cards"] == 3

@pytest.mark.asyncio
async def test_analytics_filter_by_column_type_fact_and_material(test_client, analytics_data):
    """Test complex filter: Fact column AND Plastic material (should include C2)."""
    mat_plastic = analytics_data["mat_plastic_id"]
    expected_total = analytics_data["len_c2"]
    
    query = f"column_type=fact&pipe_material_id={mat_plastic}"
    resp = await test_client.get(f"/analytics/pipes-length?{query}")
    
    data = resp.json()
    assert data["total_length"] == expected_total
    assert data["count_cards"] == 1

@pytest.mark.asyncio
async def test_analytics_zero_result(test_client, analytics_data):
    """Test filter that yields no results."""
    resp = await test_client.get("/analytics/pipes-length?pipe_diameter_min=999")
    data = resp.json()
    
    assert data["total_length"] == 0.0
    assert data["count_cards"] == 0