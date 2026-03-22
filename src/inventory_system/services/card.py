from enum import Enum
from inventory_system.schemas import CardCreateSchema, CardUpdateSchema, CardFilter, PaginatedResponse
from inventory_system.schemas import PipeDataCreate, ValveDataCreate
from inventory_system.ports.card import ICardRepository
from inventory_system.ports.equipment import IEquipmentRepository
from inventory_system.exceptions.card import CardCreationError, CardNotFoundError, CardUpdateError
from inventory_system.exceptions.equipment import EquipmentMigrationError, EquipmentRecordNotFoundError, UnknownEquipmentTypeError
from ..constants import CutTypeCode, ColumnType


class CardService:
    def __init__(self, card_repo: ICardRepository, equipment_repo: IEquipmentRepository):
        self.card_repo = card_repo
        self.equipment_repo = equipment_repo
    
    async def get_card(self, card_id: int):
        card = await self.card_repo.get_card(card_id)
        if not card:
            raise CardNotFoundError(card_id)
        return card

    async def list_cards(self, filter_params: CardFilter) -> PaginatedResponse:
        return await self.card_repo.list_cards(filter_params)

    async def create_card(self, card_data: CardCreateSchema):
        card = await self.card_repo.create(**card_data.model_dump())
        if not card:
            raise CardCreationError("Failed to create new card")
        return card

    async def update_card(self, card_id: int, update_data: CardUpdateSchema):
        current_card = await self.card_repo.get_by_id(card_id)
        if not current_card:
            raise CardNotFoundError(card_id)

        is_cut_type_changing = (
            update_data.cut_type_id is not None and 
            update_data.cut_type_id != current_card.cut_type_id
        )

        update_dict = update_data.model_dump(exclude_unset=True, exclude={"cut_column_data_source"})
        try:
            updated_card = await self.card_repo.update(card_id, **update_dict)
            if not updated_card:
                raise CardUpdateError(card_id)
        except Exception as e:
            raise CardUpdateError(card_id) from e

        if is_cut_type_changing and update_data.cut_column_data_source:
            fresh_card = await self.card_repo.get_by_id(card_id)
            if not fresh_card:
                raise CardNotFoundError(card_id)

            if fresh_card.cut_code == CutTypeCode.FULL:
                await self._migrate_to_full_cut(
                    card_id, 
                    source_column=update_data.cut_column_data_source
                )

        return updated_card

    async def _migrate_to_full_cut(self, card_id: int, source_column: str):
        try:
            equipment_items = await self.equipment_repo.get_card_equipment_items(card_id)

            target_col = str(getattr(source_column, 'value', source_column)).upper()

            for item in equipment_items:
                source_entries = [
                    e for e in item.data_entries 
                    if str(getattr(e.column_type, 'value', e.column_type)).upper() == target_col
                ]

                cut_entries = [
                    e for e in item.data_entries 
                    if str(getattr(e.column_type, 'value', e.column_type)).upper() == "CUT"
                ]
                for cut_entry in cut_entries:
                    deleted = await self.equipment_repo.delete_equipment_record(cut_entry.id)
                    if not deleted:
                        raise EquipmentRecordNotFoundError(f"Failed to delete old CUT: {cut_entry.id}")
                
                for source_entry in source_entries:
                    entry_type = source_entry.type
                    
                    entry_dict = source_entry.model_dump(exclude={"id"})
                    entry_dict["column_type"] = "CUT" 

                    if entry_type == "pipe_data":
                        new_cut_schema = PipeDataCreate(**entry_dict)
                    elif entry_type == "valve_data":
                        new_cut_schema = ValveDataCreate(**entry_dict)
                    else:
                        raise UnknownEquipmentTypeError(entry_type)
                    
                    added_record = await self.equipment_repo.add_equipment_record(item.id, new_cut_schema)

                    if not added_record:
                        raise EquipmentMigrationError(f"DB failed to insert CUT for item {item.id}")

                fact_entries = [
                    e for e in item.data_entries 
                    if str(getattr(e.column_type, 'value', e.column_type)).upper() == "FACT"
                ]
                for fact in fact_entries:
                    deleted = await self.equipment_repo.delete_equipment_record(fact.id)
                    if not deleted:
                        raise EquipmentRecordNotFoundError(f"Failed to delete old FACT: {fact.id}")
                        
        except (EquipmentRecordNotFoundError, UnknownEquipmentTypeError) as e:
            raise EquipmentMigrationError(f"Migration failed for card {card_id}: {str(e)}") from e
        except Exception as e:
            raise EquipmentMigrationError(f"Unexpected error during migration for card {card_id}") from e
    
    async def delete_card(self, card_id: int):
        deleted = await self.card_repo.delete(card_id)
        if not deleted:
            raise CardNotFoundError(card_id)