from .base import InventorySystemError

class EquipmentItemNotFoundError(InventorySystemError):
    def __init__(self, item_id: int):
        super().__init__(f"EquipmentItem with id {item_id} not found")

class EquipmentRecordNotFoundError(InventorySystemError):
    def __init__(self, record_id: int):
        super().__init__(f"EquipmentRecord with id {record_id} not found")

class EquipmentMigrationError(InventorySystemError):
    def __init__(self, card_id: int):
        super().__init__(f"Failed to automigrate equipment for Cut type change to Full. Card id: {card_id}")

class UnknownEquipmentTypeError(InventorySystemError):
    def __init__(self, unknown_type: str):
        super().__init__(f"Unknown equipment type '{unknown_type}'")
