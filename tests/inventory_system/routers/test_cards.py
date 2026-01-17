import pytest
from fastapi import status
import json

@pytest.mark.asyncio
async def test_get_all_cards(test_client):
    response = await test_client.get("/cards")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
