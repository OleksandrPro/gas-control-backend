from .base import InventorySystemError

class LookupRecordNotFoundError(InventorySystemError):
    def __init__(self, record_id: int):
        super().__init__(f"Lookup record with id {record_id} not found")