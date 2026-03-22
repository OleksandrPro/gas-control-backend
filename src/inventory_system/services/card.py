from enum import Enum
from inventory_system.schemas import CardCreateSchema, CardUpdateSchema, CardFilter, PaginatedResponse
from inventory_system.schemas import PipeDataCreate, ValveDataCreate
from inventory_system.models import ColumnType
from inventory_system.ports.card import ICardRepository
from inventory_system.ports.equipment import IEquipmentRepository
from inventory_system.exceptions.card import CardCreationError, CardNotFoundError, CardUpdateError
from inventory_system.exceptions.equipment import EquipmentMigrationError, EquipmentRecordNotFoundError, UnknownEquipmentTypeError
from ..constants import CutTypeCode


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

            new_cut_type = fresh_card.cut_type if fresh_card else None
            
            if new_cut_type and new_cut_type.code == CutTypeCode.FULL:
                await self._migrate_to_full_cut(
                    card_id, 
                    source_column=update_data.cut_column_data_source
                )

        return updated_card

    async def _migrate_to_full_cut(self, card_id: int, source_column: str):
        try: 
            equipment_items = await self.equipment_repo.get_card_equipment_items(card_id)

            for item in equipment_items:
                source_entries = [e for e in item.data_entries if e.column_type == source_column]

                cut_entries = [e for e in item.data_entries if e.column_type == ColumnType.CUT]
                for cut_entry in cut_entries:
                    deleted = await self.equipment_repo.delete_equipment_record(cut_entry.id)
                    if not deleted:
                        raise EquipmentRecordNotFoundError(cut_entry.id)
                
                for source_entry in source_entries:
                    entry_type = source_entry.type
                    if entry_type== "pipe_data":
                        schema_obj = PipeDataCreate.model_validate(source_entry)
                    elif entry_type == "valve_data":
                        schema_obj = ValveDataCreate.model_validate(source_entry)
                    else:
                        raise UnknownEquipmentTypeError(entry_type)
                    
                    new_cut_schema = schema_obj.model_copy(update={"column_type": ColumnType.CUT})
                    
                    added_record = await self.equipment_repo.add_equipment_record(item.id, new_cut_schema)

                    if not added_record:
                        raise EquipmentMigrationError(card_id)

                fact_entries = [e for e in item.data_entries if e.column_type == ColumnType.FACT]
                for fact in fact_entries:
                    deleted = await self.equipment_repo.delete_equipment_record(fact.id)
                    if not deleted:
                        raise EquipmentRecordNotFoundError(fact.id)
        
        except (EquipmentRecordNotFoundError, UnknownEquipmentTypeError) as e:
            raise EquipmentMigrationError(card_id) from e
        except Exception as e:
            raise EquipmentMigrationError(card_id) from e
    
    async def delete_card(self, card_id: int):
        deleted = await self.card_repo.delete(card_id)
        if not deleted:
            raise CardNotFoundError(card_id)