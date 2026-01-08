from typing import Optional
from inventory_system.models import Card
from utils.db_utils import DatabaseManager

class CardRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.manager = db_manager

    async def create(self, **data) -> Card:
        new_card = Card(**data)
        result = await self.manager.add_record(new_card)
        return result
    
    async def update(self, card_id: int, **update_data) -> Optional[Card]:
        card = await self.get_by_id(card_id)
        
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
