from enum import Enum
from fastapi import HTTPException
from inventory_system.repositories.card import CardRepository
from inventory_system.repositories.equipment import EquipmentRepository
from inventory_system.schemas import CardUpdateSchema
from inventory_system.schemas import PipeDataCreate, ValveDataCreate
from inventory_system.models import ColumnType

class CutTypeCode(str, Enum):
    NONE = "none"
    FULL = "full"
    PARTIAL = "partial"

class CardService:
    def __init__(self, card_repo: CardRepository, equipment_repo: EquipmentRepository):
        self.card_repo = card_repo
        self.equipment_repo = equipment_repo

    async def update_card(self, card_id: int, update_data: CardUpdateSchema):
        current_card = await self.card_repo.get_by_id(card_id)
        if not current_card:
            raise HTTPException(status_code=404, detail="Card wasn't found")

        is_cut_type_changing = (
            update_data.cut_type_id is not None and 
            update_data.cut_type_id != current_card.cut_type_id
        )

        update_dict = update_data.model_dump(exclude_unset=True, exclude={"cut_column_data_source"})
        updated_card = await self.card_repo.update(card_id, **update_dict)

        if is_cut_type_changing and update_data.cut_column_data_source:
            fresh_card = await self.card_repo.get_by_id(card_id)
            new_cut_type = fresh_card.cut_type if fresh_card else None
            
            if new_cut_type and new_cut_type.code == CutTypeCode.FULL:
                await self._migrate_to_full_cut(
                    card_id, 
                    source_column=update_data.cut_column_data_source
                )

        return updated_card

    async def _migrate_to_full_cut(self, card_id: int, source_column: str):
        equipment_items = await self.equipment_repo.get_items_by_card(card_id)

        for item in equipment_items:
            source_entries = [e for e in item.data_entries if e.column_type == source_column]

            cut_entries = [e for e in item.data_entries if e.column_type == ColumnType.CUT]
            for cut_entry in cut_entries:
                await self.equipment_repo.delete_data_entry(cut_entry.id)
            
            for source_entry in source_entries:
                if source_entry.type == "pipe_data":
                    schema_obj = PipeDataCreate.model_validate(source_entry)
                elif source_entry.type == "valve_data":
                    schema_obj = ValveDataCreate.model_validate(source_entry)
                else:
                    raise ValueError(f"Unknown equipment data type: {source_entry.type}")
                
                new_cut_schema = schema_obj.model_copy(update={"column_type": ColumnType.CUT})
                
                await self.equipment_repo.add_data_entry(item.id, new_cut_schema)

            fact_entries = [e for e in item.data_entries if e.column_type == ColumnType.FACT]
            for fact in fact_entries:
                await self.equipment_repo.delete_data_entry(fact.id)