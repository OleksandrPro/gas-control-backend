from .base import InventorySystemError

class EquipmentItemCreationError(InventorySystemError):
    def __init__(self, item_id: int):
        super().__init__(f"Failed to create EquipmentItem {item_id}")

class EquipmentRecordCreationError(InventorySystemError):
    def __init__(self, item_id: int):
        super().__init__(f"Failed to create EquipmentRecord {item_id}")

class EquipmentItemNotFoundError(InventorySystemError):
    def __init__(self, item_id: int):
        super().__init__(f"EquipmentItem with id {item_id} not found")

class EquipmentRecordNotFoundError(InventorySystemError):
    def __init__(self, record_id: int):
        super().__init__(f"EquipmentRecord with id {record_id} not found")

class EquipmentItemUpdateError(InventorySystemError):
    def __init__(self, item_id: int):
        super().__init__(f"Failed to update EquipmentItem {item_id}")

class EquipmentRecordUpdateError(InventorySystemError):
    def __init__(self, item_id: int):
        super().__init__(f"Failed to update EquipmentRecord {item_id}")

class EquipmentMigrationError(InventorySystemError):
    def __init__(self, card_id: int):
        super().__init__(f"Failed to automigrate equipment for Cut type change to Full. Card id: {card_id}")

class UnknownEquipmentTypeError(InventorySystemError):
    def __init__(self, unknown_type: str):
        super().__init__(f"Unknown equipment type '{unknown_type}'")

class DuplicateBalanceEntryError(InventorySystemError):
    def __init__(self):
        super().__init__("Only one BALANCE entry is allowed per equipment item.")

class UnknownCutTypeError(InventorySystemError):
    def __init__(self, cut_code: str):
        super().__init__(f"Unknown cut type code: '{cut_code}'")

class EquipmentStructureViolationError(InventorySystemError):
    def __init__(self, rule_desc: str, expected: list, got: list):
        self.rule_desc = rule_desc
        self.expected = expected
        self.got = got
        super().__init__(
            f"Invalid equipment data structure. Rule: {rule_desc}. "
            f"Expected column types: {expected}, but got: {got}"
        )
