from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload, selectin_polymorphic
from inventory_system.schemas import EquipmentDataCreate
from utils.db_utils import DatabaseManager
from inventory_system.models import EquipmentItem, EquipmentData, PipeData, ValveData

class EquipmentRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.manager = db_manager

    async def create_item(self, card_id: int, item_type: str, description: str) -> EquipmentItem:
        item = EquipmentItem(card_id=card_id, item_type=item_type, description=description)
        return await self.manager.add_record(item, err_msg="Failed to create equipment item")

    async def add_data_entry(self, item_id: int, data_schema: EquipmentDataCreate):
        # We need to determine which model class to use based on the input type
        if data_schema.type == "pipe_data":
            model_class = PipeData
        elif data_schema.type == "valve_data":
            model_class = ValveData
        else:
            raise ValueError(f"Unknown data type: {data_schema.type}")

        # Convert Pydantic to dict and create model instance
        data_dict = data_schema.model_dump()
        # Remove 'type' field if it's handled by polymorphism automatically or keep it
        # SQLAlchemy polymorphism usually handles 'type' automatically if defined in mapper_args
        
        # We need to manually set item_id
        entry = model_class(**data_dict, item_id=item_id)
        
        return await self.manager.add_record(entry, err_msg="Failed to add data entry")

    async def get_item_by_id(self, item_id: int) -> Optional[EquipmentItem]:
        loader = selectinload(EquipmentItem.data_entries).selectin_polymorphic(
            [PipeData, ValveData]
        )
        query = select(EquipmentItem).where(EquipmentItem.id == item_id).options(loader)
        
        return await self.manager.get_first(query, err_msg=f"Item {item_id} not found")

    async def get_items_by_card(self, card_id: int):
        loader = selectinload(EquipmentItem.data_entries).selectin_polymorphic(
            [PipeData, ValveData]
        )
        
        query = select(EquipmentItem).where(EquipmentItem.card_id == card_id).options(loader)
        
        return await self.manager.get_all(query, err_msg="Failed to fetch equipment items")
    
    async def delete_item(self, item_id: int) -> bool:
        """
        Deletes the Equipment Item container. 
        Due to cascade settings, this will also delete all associated Data entries.
        """
        query = select(EquipmentItem).where(EquipmentItem.id == item_id)
        item = await self.manager.get_first(query, err_msg=f"Error finding item {item_id}")
        
        if not item:
            return False
            
        await self.manager.delete_record(item, err_msg=f"Failed to delete equipment item {item_id}")
        return True

    async def delete_data_entry(self, data_id: int) -> bool:
        """
        Deletes a specific data entry (e.g. only 'Fact' column data).
        """
        query = select(EquipmentData).where(EquipmentData.id == data_id)
        entry = await self.manager.get_first(query, err_msg=f"Error finding data entry {data_id}")
        
        if not entry:
            return False
            
        await self.manager.delete_record(entry, err_msg=f"Failed to delete data entry {data_id}")
        return True
