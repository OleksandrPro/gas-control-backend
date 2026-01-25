from typing import List, Union, Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from inventory_system.schemas import DisplayMainPageCard, CardCreateSchema, CardUpdateSchema, PaginatedResponse, CardFilter

from utils.db_utils import DatabaseManager
from database import get_session

from inventory_system.repositories.card import CardRepository


cards_router = APIRouter(prefix="/cards", tags=["Cards"])

@cards_router.get("", response_model=PaginatedResponse[DisplayMainPageCard])
async def read_all_cards(session: Annotated[AsyncSession, Depends(get_session)], filter_params: Annotated[CardFilter, Depends()]):
    #TODO later add proper response_model to avoid potential mistakes with auto jsonable_encoder
    db_manager = DatabaseManager(session)
    repo = CardRepository(db_manager=db_manager)
    return await repo.list_cards(filter_params)

@cards_router.get("/{id}")
async def read_card(id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    #TODO later add proper response_model to avoid potential mistakes with auto jsonable_encoder
    db_manager = DatabaseManager(session)
    repo = CardRepository(db_manager=db_manager)
    return await repo.get_card(id)

@cards_router.post("")
async def create_card(card: CardCreateSchema, session: Annotated[AsyncSession, Depends(get_session)]):
    db_manager = DatabaseManager(session)
    repo = CardRepository(db_manager=db_manager)
    return await repo.create(**card.model_dump())

@cards_router.patch("/{id}")
async def update_card(id: int, new_data: CardUpdateSchema, session: Annotated[AsyncSession, Depends(get_session)]):
    db_manager = DatabaseManager(session)
    repo = CardRepository(db_manager=db_manager)
    
    update_data = new_data.model_dump(exclude_unset=True)

    updated_card = await repo.update(id, **update_data)

    if not updated_card:
        raise HTTPException(status_code=404, detail="Card wasn't found")
        
    return updated_card

@cards_router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_card(
    card_id: int, 
    session: Annotated[AsyncSession, Depends(get_session)]
):
    db_manager = DatabaseManager(session)
    repo = CardRepository(db_manager)
    
    deleted = await repo.delete(card_id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Card not found")
    
    # 204 No Content is standard for delete operations
    return Response(status_code=status.HTTP_204_NO_CONTENT)