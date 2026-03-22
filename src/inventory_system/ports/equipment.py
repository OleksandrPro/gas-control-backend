from typing import Protocol, List
from inventory_system.schemas import EquipmentItemRead, EquipmentDataCreate, EquipmentDataRead

class IEquipmentRepository(Protocol):
    async def get_card_equipment_items(self, card_id: int) -> List[EquipmentItemRead]:
        ...

    async def add_equipment_record(self, item_id: int, new_record: EquipmentDataCreate) -> EquipmentDataRead:
        ...

    async def delete_equipment_record(self, id: int) -> bool:
        ...
