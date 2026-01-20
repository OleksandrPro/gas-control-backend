from enum import Enum
from typing import List, Set
from fastapi import HTTPException, status

from inventory_system.repositories.equipment import EquipmentRepository
from inventory_system.repositories.card import CardRepository
from inventory_system.schemas import EquipmentItemCreate, EquipmentDataCreate
from inventory_system.models import ColumnType

# Enum that matches 'code' column in 'cut_types' table
class CutTypeCode(str, Enum):
    NONE = "none"       # No cut
    FULL = "full"       # Full cut
    PARTIAL = "partial" # Partial cut

class EquipmentService:
    def __init__(self, equipment_repo: EquipmentRepository, card_repo: CardRepository):
        self.equipment_repo = equipment_repo
        self.card_repo = card_repo

    async def add_equipment_to_card(self, card_id: int, item_in: EquipmentItemCreate):
        """
        Orchestrates adding equipment with business validation.
        Enforces strict structure rules based on card cut type.
        """
        card = await self.card_repo.get_by_id(card_id)
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")

        # Get the cut code. If cut_type is None, we treat it as NONE (No cut).
        cut_code = card.cut_type.code if card.cut_type else CutTypeCode.NONE

        self._validate_entries_structure(cut_code, item_in.data_entries)

        item = await self.equipment_repo.create_item(
            card_id, 
            item_in.item_type, 
            item_in.description
        )
        
        for entry in item_in.data_entries:
            await self.equipment_repo.add_data_entry(item.id, entry)
            
        return await self.equipment_repo.get_item_by_id(item.id)

    def _validate_entries_structure(self, cut_code: str, entries: List[EquipmentDataCreate]):
        """
        Validates that the list of data entries strictly matches the required columns
        for the given cut type.
        """
        input_types = [entry.column_type for entry in entries]
        unique_types = set(input_types)

        # Check for duplicates (e.g., two BALANCE entries for one item are not allowed)
        if len(input_types) != len(unique_types):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Duplicate column types provided for a single equipment item."
            )

        required_types: Set[str] = set()

        if cut_code == CutTypeCode.NONE:
            # Rule: No Cut -> Must have BALANCE and FACT. No CUT allowed.
            required_types = {ColumnType.BALANCE, ColumnType.FACT}
            error_detail = "Card without cut must have exactly BALANCE and FACT data entries."

        elif cut_code == CutTypeCode.FULL:
            # Rule: Full Cut -> Must have BALANCE and CUT. No FACT allowed.
            required_types = {ColumnType.BALANCE, ColumnType.CUT}
            error_detail = "Card with Full Cut must have exactly BALANCE and CUT data entries."

        elif cut_code == CutTypeCode.PARTIAL:
            # Rule: Partial Cut -> Must have BALANCE, FACT, and CUT.
            required_types = {ColumnType.BALANCE, ColumnType.FACT, ColumnType.CUT}
            error_detail = "Card with Partial Cut must have BALANCE, FACT, and CUT data entries."
        
        else:
            # Fallback for unknown cut codes
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown cut type code: {cut_code}"
            )

        # Strict comparison
        # The set of input types must be exactly equal to the required set
        if unique_types != required_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid data structure. {error_detail} Got: {[t.value for t in unique_types]}"
            )