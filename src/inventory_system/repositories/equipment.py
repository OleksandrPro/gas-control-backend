from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import selectinload, selectin_polymorphic
from inventory_system.ports.equipment import IEquipmentRepository
from utils.db_utils import DatabaseManager
from inventory_system.schemas import EquipmentItemRead, EquipmentDataCreate, EquipmentDataRead
from inventory_system.models import EquipmentItem, EquipmentData, PipeData, ValveData

class EquipmentRepository(IEquipmentRepository):
    def __init__(self, db_manager: DatabaseManager):
        self.manager = db_manager

    async def create_item(self, card_id: int, item_type: str, description: str) -> Optional[EquipmentItemRead]:
        item = EquipmentItem(card_id=card_id, item_type=item_type, description=description)
        db_model = await self.manager.add_record(item, err_msg="Failed to create equipment item")
        if db_model:
            return EquipmentItemRead.model_validate(db_model)
        return None

    async def add_equipment_record(self, item_id: int, data_schema: EquipmentDataCreate) -> EquipmentDataRead:
        # We need to determine which model class to use based on the input type
        if data_schema.type == "pipe_data":
            model_class = PipeData
        elif data_schema.type == "valve_data":
            model_class = ValveData
        else:
            raise ValueError(f"Unknown data type: {data_schema.type}")

        data_dict = data_schema.model_dump()
        entry = model_class(**data_dict, item_id=item_id)
        
        db_model = await self.manager.add_record(entry, err_msg="Failed to add data entry")

        if db_model:
            return EquipmentDataRead.model_validate(db_model)
        return None

    async def get_item_by_id(self, item_id: int) -> Optional[EquipmentItemRead]:
        loader = selectinload(EquipmentItem.data_entries).selectin_polymorphic(
            [PipeData, ValveData]
        )
        query = select(EquipmentItem).where(EquipmentItem.id == item_id).options(loader)
        
        db_model = await self.manager.get_first(query, err_msg=f"Item {item_id} not found")
        if db_model:
            return EquipmentItemRead.model_validate(db_model)
        return None

    async def get_card_equipment_items(self, card_id: int) -> List[EquipmentItemRead]:
        loader = selectinload(EquipmentItem.data_entries).selectin_polymorphic(
            [PipeData, ValveData]
        )
        query = select(EquipmentItem).where(EquipmentItem.card_id == card_id).options(loader)
        
        db_models = await self.manager.get_all(query, err_msg="Failed to fetch equipment items")
        return [EquipmentItemRead.model_validate(model) for model in db_models]
    
    async def update_equipment_record(self, record_id: int, **update_data) -> Optional[EquipmentDataRead]:
        query = select(EquipmentData).where(EquipmentData.id == record_id).options(
            selectin_polymorphic(EquipmentData, [PipeData, ValveData])
        )
        entry = await self.manager.get_first(query, err_msg=f"Data entry {record_id} not found")
        
        if not entry:
            return None
            
        for key, value in update_data.items():
            if hasattr(entry, key):
                setattr(entry, key, value)
        
        db_model = await self.manager.add_record(entry, err_msg="Failed to update data entry")
        if db_model:
             return EquipmentDataRead.model_validate(db_model)
        return None

    async def update_item(self, item_id: int, **update_data) -> Optional[EquipmentItemRead]:
        query = select(EquipmentItem).where(EquipmentItem.id == item_id)
        item = await self.manager.get_first(query, err_msg=f"Item {item_id} not found")
        
        if not item:
            return None
            
        for key, value in update_data.items():
            if hasattr(item, key):
                setattr(item, key, value)
                
        db_model = await self.manager.add_record(item, err_msg="Failed to update equipment item")
        if db_model:
            return EquipmentItemRead.model_validate(db_model)
        return None

    async def delete_item(self, item_id: int) -> bool:
        query = select(EquipmentItem).where(EquipmentItem.id == item_id)
        item = await self.manager.get_first(query, err_msg=f"Error finding item {item_id}")
        
        if not item:
            return False
            
        await self.manager.delete_record(item, err_msg=f"Failed to delete equipment item {item_id}")
        return True

    async def delete_equipment_record(self, data_id: int) -> bool:
        query = select(EquipmentData).where(EquipmentData.id == data_id)
        entry = await self.manager.get_first(query, err_msg=f"Error finding data entry {data_id}")
        
        if not entry:
            return False
            
        await self.manager.delete_record(entry, err_msg=f"Failed to delete data entry {data_id}")
        return True
