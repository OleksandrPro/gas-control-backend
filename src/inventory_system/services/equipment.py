from enum import Enum
from typing import List, Set

from inventory_system.ports.card import ICardRepository
from inventory_system.ports.equipment import IEquipmentRepository
from inventory_system.schemas import EmptyEquipmentItemCreate, EquipmentItemCreate, EquipmentDataCreate, EquipmentItemUpdate
from inventory_system.models import ColumnType
from inventory_system.exceptions.card import CardNotFoundError, CardUpdateError
from inventory_system.exceptions.equipment import (
    EquipmentMigrationError,
    EquipmentItemNotFoundError,
    EquipmentRecordNotFoundError,
    EquipmentItemUpdateError,
    EquipmentRecordUpdateError,
    UnknownEquipmentTypeError
)

# Enum that matches 'code' column in 'cut_types' table
class CutTypeCode(str, Enum):
    NONE = "none"       # No cut
    FULL = "full"       # Full cut
    PARTIAL = "partial" # Partial cut

class EquipmentService:
    def __init__(self, equipment_repo: IEquipmentRepository, card_repo: ICardRepository):
        self.equipment_repo = equipment_repo
        self.card_repo = card_repo

    async def add_equipment_to_card(self, card_id: int, item_in: EquipmentItemCreate):
        """
        Orchestrates adding equipment with business validation.
        Enforces strict structure rules based on card cut type.
        """
        card = await self.card_repo.get_by_id(card_id)
        if not card:
            raise CardNotFoundError(card_id)

        cut_code = card.cut_type.code if card.cut_type else CutTypeCode.NONE

        self._validate_entries_structure(cut_code, item_in.data_entries)

        item = await self.equipment_repo.create_item(
            card_id, 
            item_in.item_type, 
            item_in.description
        )
        
        if not item:
            raise EquipmentItemCreationError(card_id)
        
        for entry in item_in.data_entries:
            added = await self.equipment_repo.add_equipment_record(item.id, entry)
            if not added:
                raise EquipmentRecordCreationError(item.id)
            
        return await self.equipment_repo.get_by_id(item.id)
    
    async def get_card_equipment(self, card_id: int):
        card = await self.card_repo.get_by_id(card_id)
        if not card:
            raise CardNotFoundError(card_id)
        
        return await self.equipment_repo.get_card_equipment_items(card_id)

    async def update_equipment_record(self, record_id: int, update_data: dict):
        updated = await self.equipment_repo.update_equipment_record(record_id, **update_data)
        if not updated:
            raise EquipmentRecordNotFoundError(record_id)
        return updated

    async def update_equipment_item(self, item_id: int, update_data: EquipmentItemUpdate):
        item = await self.equipment_repo.get_by_id(item_id)
        if not item:
            raise EquipmentItemNotFoundError(item_id)

        if update_data.description is not None:
            updated = await self.equipment_repo.update_item(item_id, description=update_data.description)
            if not updated:
                raise EquipmentItemUpdateError(item_id)

        if update_data.data_entries is not None:
            card = await self.card_repo.get_by_id(item.card_id)
            if not card:
                raise CardNotFoundError(item.card_id)

            cut_code = card.cut_type.code if card.cut_type and card.cut_type.code else CutTypeCode.NONE
            self._validate_entries_structure(cut_code, update_data.data_entries)

            existing_ids = {entry.id for entry in item.data_entries}
            incoming_ids = set()

            for entry_schema in update_data.data_entries:
                if entry_schema.id and entry_schema.id in existing_ids:
                    update_dict = entry_schema.model_dump(exclude={'id', 'type'})
                    updated = await self.equipment_repo.update_equipment_record(entry_schema.id, **update_dict)
                    if not updated:
                        raise EquipmentRecordUpdateError(entry_schema.id)
                    incoming_ids.add(entry_schema.id)
                else:
                    added = await self.equipment_repo.add_equipment_record(item_id, entry_schema)
                    if not added:
                        raise EquipmentRecordCreationError(item_id)

            to_delete_ids = existing_ids - incoming_ids
            for del_id in to_delete_ids:
                deleted = await self.equipment_repo.delete_equipment_record(del_id)
                if not deleted:
                    raise EquipmentRecordNotFoundError(del_id)

        return await self.equipment_repo.get_item_by_id(item_id)

    def _validate_entries_structure(self, cut_code: str, entries: List[EquipmentDataCreate]):
        """
        Validates that the list of data entries strictly matches the required columns
        for the given cut type.
        """
        input_types = [entry.column_type for entry in entries]
        unique_types = set(input_types)

        # Check constraints (e.g., only one BALANCE entry for one item is allowed, entry can have multiple FACTs and CUTs)
        if input_types.count(ColumnType.BALANCE) > 1:
            raise DuplicateBalanceEntryError()

        required_types: Set[str] = set()

        if cut_code == CutTypeCode.NONE:
            required_types = {ColumnType.BALANCE, ColumnType.FACT}
            rule_desc = "Card without cut must have exactly BALANCE and FACT data entries. No CUT allowed."

        elif cut_code == CutTypeCode.FULL:
            required_types = {ColumnType.BALANCE, ColumnType.CUT}
            rule_desc = "Card with Full Cut must have exactly BALANCE and CUT data entries. No FACT allowed."

        elif cut_code == CutTypeCode.PARTIAL:
            required_types = {ColumnType.BALANCE, ColumnType.FACT, ColumnType.CUT}
            rule_desc = "Card with Partial Cut must have BALANCE, FACT, and CUT data entries."
        
        else:
            raise UnknownCutTypeError(cut_code)

        if unique_types != required_types:
            raise EquipmentStructureViolationError(
                rule_desc=rule_desc,
                expected=[t.value for t in required_types],
                got=[t.value for t in unique_types]
            )

    async def delete_equipment_record(self, record_id: int):
        deleted = await self.equipment_repo.delete_equipment_record(record_id)
        if not deleted:
            raise EquipmentRecordNotFoundError(record_id)

    async def delete_equipment_item(self, item_id: int):
        deleted = await self.equipment_repo.delete_item(item_id)
        if not deleted:
            raise EquipmentItemNotFoundError(item_id)
