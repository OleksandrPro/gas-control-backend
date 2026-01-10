from typing import List, Union, Annotated

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from inventory_system.schemas import DisplayMainPageCard, CardUpdateSchema
from inventory_system.schemas import EquipmentItemCreate, EquipmentItemRead

from utils.db_utils import DatabaseManager
from database import get_session

from inventory_system.repositories.card import CardRepository

from inventory_system.routers import lookups_router

from fastapi import HTTPException, Response, status

app = FastAPI()


async def get_hello_world():
    return {"Hello": "World"}

@app.get("/")
async def read_root():
    return await get_hello_world()

@app.get("/cards")
async def read_all_cards(session: Annotated[AsyncSession, Depends(get_session)]):
    #TODO later add proper response_model to avoid potential mistakes with auto jsonable_encoder
    db_manager = DatabaseManager(session)
    cards = await db_manager.get_all_cards()
    return cards

@app.get("/cards/{id}")
async def read_card(id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    #TODO later add proper response_model to avoid potential mistakes with auto jsonable_encoder
    db_manager = DatabaseManager(session)
    card = await db_manager.get_card(id)
    return card

@app.post("/cards")
async def create_card(card: DisplayMainPageCard, session: Annotated[AsyncSession, Depends(get_session)]):
    db_manager = DatabaseManager(session)
    repo = CardRepository(db_manager=db_manager)
    return await repo.create(**card.model_dump())

@app.patch("/cards/{id}")
async def update_card(id: int, new_data: CardUpdateSchema, session: Annotated[AsyncSession, Depends(get_session)]):
    db_manager = DatabaseManager(session)
    repo = CardRepository(db_manager=db_manager)
    
    update_data = new_data.model_dump(exclude_unset=True)

    updated_card = await repo.update(**update_data)

    if not updated_card:
        raise HTTPException(status_code=404, detail="Card wasn't found")
        
    return updated_card

@app.delete("/cards/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_card(
    card_id: int, 
    session: Annotated[AsyncSession, Depends(get_session)]
):
    db_manager = DatabaseManager(session)
    repo = CardRepository(db_manager)
    
    deleted = await repo.delete(card_id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Card not found")
    
    # 204 No Content is standard for delete operations
    return Response(status_code=status.HTTP_204_NO_CONTENT)


from inventory_system.schemas import (
    EquipmentItemCreate, 
    EquipmentItemRead,
    EquipmentDataCreate
)

@app.post("/cards/{card_id}/equipment", response_model=EquipmentItemRead)
async def create_equipment(
    card_id: int, 
    item_in: EquipmentItemCreate, 
    session: Annotated[AsyncSession, Depends(get_session)]
):
    db_manager = DatabaseManager(session)
    repo = EquipmentRepository(db_manager)
    
    item = await repo.create_item(card_id, item_in.item_type)
    
    for data_entry in item_in.data_entries:
        await repo.add_data_entry(item.id, data_entry)
    
    return await repo.get_item_by_id(item.id)

@app.get("/cards/{card_id}/equipment", response_model=List[EquipmentItemRead])
async def get_card_equipment(
    card_id: int, 
    session: Annotated[AsyncSession, Depends(get_session)]
):
    db_manager = DatabaseManager(session)
    repo = EquipmentRepository(db_manager)
    return await repo.get_items_by_card(card_id)

@app.patch("/equipment-data/{equipment_id}") 
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

# Delete Equipment Data Entry Endpoint
# This deletes specific data (e.g. removes "Fact" data, keeping "Balance")
@app.delete("/equipment-data/{equipment_id}", status_code=status.HTTP_204_NO_CONTENT)
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
@app.delete("/equipment-items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
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

app.include_router(lookups_router)
