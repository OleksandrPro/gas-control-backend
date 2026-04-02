from .base import InventorySystemError

class CardCreationError(InventorySystemError):
    def __init__(self):
        super().__init__(f"Failed to create Card")

class CardNotFoundError(InventorySystemError):
    def __init__(self, id: int):
        super().__init__(f"Card with id {id} not found")

class CardUpdateError(InventorySystemError):
    def __init__(self, id: int):
        super().__init__(f"Failed to update Card with id {id}")