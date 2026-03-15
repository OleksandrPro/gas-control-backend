from typing import List, Union, Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from inventory_system.services.equipment import EquipmentService
from inventory_system.repositories.equipment import EquipmentRepository
from inventory_system.repositories.card import CardRepository
from utils.db_utils import DatabaseManager
from database import get_session

from inventory_system.schemas import (
    EquipmentItemCreate, 
    EquipmentItemRead,
    EquipmentDataCreate,
    EquipmentItemUpdate
)


equipment_router = APIRouter(tags=["Equipment"])

def get_equipment_service(session: AsyncSession = Depends(get_session)) -> EquipmentService:
    db_manager = DatabaseManager(session)
    equipment_repo = EquipmentRepository(db_manager)
    card_repo = CardRepository(db_manager)
    return EquipmentService(equipment_repo, card_repo)

@equipment_router.post("/cards/{card_id}/equipment", response_model=EquipmentItemRead)
async def create_equipment(
    card_id: int, 
    item_in: EquipmentItemCreate, 
    service: Annotated[EquipmentService, Depends(get_equipment_service)]
):
    return await service.add_equipment_to_card(card_id, item_in)

@equipment_router.get("/cards/{card_id}/equipment", response_model=List[EquipmentItemRead])
async def get_card_equipment(
    card_id: int, 
    session: Annotated[AsyncSession, Depends(get_session)]
):
    db_manager = DatabaseManager(session)
    repo = EquipmentRepository(db_manager)
    return await repo.get_items_by_card(card_id)

@equipment_router.patch("/equipment-data/{equipment_id}") 
async def update_equipment_data(
    equipment_id: int,
    update_data: dict, # TODO try to implement something like EquipmentDataUpdate
    session: Annotated[AsyncSession, Depends(get_session)]
):
    db_manager = DatabaseManager(session)
    repo = EquipmentRepository(db_manager)
    
    # Clear None values when using a schema with Optional fields
    # clean_data = update_schema.model_dump(exclude_unset=True)
    
    result = await repo.update_data_entry(equipment_id, **update_data)
    if not result:
        raise HTTPException(status_code=404, detail="Data entry not found")
        
    return result

@equipment_router.patch("/equipment-items/{item_id}", response_model=EquipmentItemRead)
async def update_equipment_item(
    item_id: int,
    update_data: EquipmentItemUpdate,
    service: Annotated[EquipmentService, Depends(get_equipment_service)]
):
    return await service.update_equipment_item(item_id, update_data)

# Delete Equipment Data Entry Endpoint
# This deletes specific data (e.g. removes "Fact" data, keeping "Balance")
@equipment_router.delete("/equipment-data/{equipment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_equipment_data(
    equipment_id: int,
    session: Annotated[AsyncSession, Depends(get_session)]
):
    db_manager = DatabaseManager(session)
    repo = EquipmentRepository(db_manager)
    
    deleted = await repo.delete_data_entry(equipment_id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Data entry not found")
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Delete Equipment Item (Container) Endpoint
# This deletes the whole "row" of equipment (e.g. "Pipe #1" + Balance + Fact + Cut)
@equipment_router.delete("/equipment-items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_equipment_item(
    item_id: int,
    session: Annotated[AsyncSession, Depends(get_session)]
):
    db_manager = DatabaseManager(session)
    repo = EquipmentRepository(db_manager)
    
    deleted = await repo.delete_item(item_id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Equipment item not found")
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)
