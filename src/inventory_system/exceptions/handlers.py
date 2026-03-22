from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from inventory_system.exceptions.base import InventorySystemError
from inventory_system.exceptions.card import CardNotFoundError, CardUpdateError
from inventory_system.exceptions.equipment import (
    EquipmentMigrationError,
    EquipmentItemNotFoundError,
    EquipmentRecordNotFoundError,
    UnknownEquipmentTypeError
)

EXCEPTION_STATUS_MAP = {
    CardNotFoundError: status.HTTP_404_NOT_FOUND,
    EquipmentItemNotFoundError: status.HTTP_404_NOT_FOUND,
    EquipmentRecordNotFoundError: status.HTTP_404_NOT_FOUND,
    
    EquipmentMigrationError: status.HTTP_409_CONFLICT,
    
    CardUpdateError: status.HTTP_400_BAD_REQUEST,
    UnknownEquipmentTypeError: status.HTTP_400_BAD_REQUEST,
}

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(InventorySystemError)
    async def domain_exception_handler(request: Request, exc: InventorySystemError):
        status_code = EXCEPTION_STATUS_MAP.get(type(exc), status.HTTP_400_BAD_REQUEST)
        
        return JSONResponse(
            status_code=status_code,
            content={"detail": str(exc)}, 
        )