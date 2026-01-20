from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from inventory_system.models import Card
from utils.db_utils import DatabaseManager

class CardRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.manager = db_manager

    async def create(self, **data) -> Card:
        new_card = Card(**data)
        result = await self.manager.add_record(new_card)
        return result

    async def get_by_id(self, card_id: int) -> Optional[Card]:
        query = select(Card).where(Card.id == card_id).options(
            selectinload(Card.cut_type)
        )
        return await self.manager.get_first(
            query=query,
            err_msg=f"Error finding card with ID {card_id}"
        )
    
    async def update(self, card_id: int, **update_data) -> Optional[Card]:
        card = await self.manager.get_card(card_id)
        
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
        card = await self.manager.get_card(card_id)
        
        if not card:
            return False
            
        await self.manager.delete_record(card, err_msg=f"Failed to delete card {card_id}")
        return True
