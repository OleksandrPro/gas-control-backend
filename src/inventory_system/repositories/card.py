from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from inventory_system.models import Card
from utils.db_utils import DatabaseManager
from utils.pagination import Paginator
from inventory_system.schemas.base import PaginatedResponse
from inventory_system.schemas.card import CardFilter

class CardRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.manager = db_manager
        self.paginator = Paginator(self.manager)

    async def create(self, **data) -> Card:
        new_card = Card(**data)
        result = await self.manager.add_record(new_card)
        return result

    async def get_all_cards(self) -> List[Card]:
        query = select(Card)
        return await self.manager.get_all(
            query=query, 
            err_msg=f"Error loading card table {Card.__tablename__}"
        )

    async def get_by_id(self, card_id: int) -> Optional[Card]:
        query = select(Card).where(Card.id == card_id).options(
            selectinload(Card.cut_type)
        )
        return await self.manager.get_first(
            query=query,
            err_msg=f"Error finding card with ID {card_id}"
        )
    
    async def get_card(self, id: int) -> Card:
        query = select(Card).where(Card.id == id)
        card = await self.manager.get_first(query, err_msg="Error finding card with id '{id}'")
        
        if not card:
            raise HTTPException(status_code=404, detail=f"Record with id={id} not found")
        
        return card

    async def list_cards(self, filter_params: CardFilter) -> PaginatedResponse[Card]:
        query = select(Card).order_by(Card.id.desc())

        return await self.paginator.paginate(
            query, 
            page=filter_params.page, 
            size=filter_params.size
        )

    async def update(self, card_id: int, **update_data) -> Optional[Card]:
        card = await self.get_card(card_id)
        
        if not card:
            return None
            
        # update_data contains only non-None data
        for key, value in update_data.items():
            if hasattr(card, key):
                setattr(card, key, value)
        
        return await self.manager.add_record(
            card, 
            err_msg=f"Failed to update card. ID: {card_id}"
        )
    
    async def delete(self, card_id: int) -> bool:
        card = await self.get_card(card_id)
        
        if not card:
            return False
            
        await self.manager.delete_record(card, err_msg=f"Failed to delete card {card_id}")
        return True
