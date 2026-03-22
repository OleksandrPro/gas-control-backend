from typing import List, Union, Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from inventory_system.schemas import Card, CardCreateSchema, CardUpdateSchema, PaginatedResponse, CardFilter

from utils.db_utils import DatabaseManager
from database import get_session

from inventory_system.repositories.card import CardRepository
from inventory_system.repositories.equipment import EquipmentRepository
from inventory_system.services.card import CardService


cards_router = APIRouter(prefix="/cards", tags=["Cards"])

def get_card_service(session: AsyncSession = Depends(get_session)) -> CardService:
    db_manager = DatabaseManager(session)
    card_repo = CardRepository(db_manager)
    equipment_repo = EquipmentRepository(db_manager)
    return CardService(card_repo, equipment_repo)

@cards_router.get("", response_model=PaginatedResponse[Card])
async def read_all_cards(
    filter_params: Annotated[CardFilter, Depends()],
    card_service: Annotated[CardService, Depends(get_card_service)]
):
    return await card_service.list_cards(filter_params)

@cards_router.get("/{id}", response_model=Card)
async def read_card(
    id: int, 
    card_service: Annotated[CardService, Depends(get_card_service)]
):
    return await card_service.get_card(id)

@cards_router.post("", response_model=Card, status_code=status.HTTP_201_CREATED)
async def create_card(
    card: CardCreateSchema, 
    card_service: Annotated[CardService, Depends(get_card_service)]
):
    return await card_service.create_card(card)

@cards_router.patch("/{id}", response_model=Card)
async def update_card(
    id: int, 
    new_data: CardUpdateSchema, 
    card_service: Annotated[CardService, Depends(get_card_service)]
):
    return await card_service.update_card(id, new_data)

@cards_router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_card(
    card_id: int, 
    card_service: Annotated[CardService, Depends(get_card_service)]
):
    await card_service.delete_card(card_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)