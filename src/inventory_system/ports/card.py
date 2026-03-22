from typing import Protocol, Optional
from inventory_system.schemas import Card 


class ICardRepository(Protocol):
    async def get_by_id(self, card_id: int) -> bool:
        ...

    async def update(self, update_data: dict) -> Optional[Card]:
        ...
