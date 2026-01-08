from typing import List, Union, Annotated

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from inventory_system.schemas import DisplayMainPageCard, CardUpdateSchema
from inventory_system.schemas import EquipmentItemCreate, EquipmentItemRead

from utils.db_utils import DatabaseManager
from database import get_session

from inventory_system.repositories.card import CardRepository

from inventory_system.routers import lookups_router

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


from inventory_system.schemas import (
    EquipmentItemCreate, 
    EquipmentItemRead,
    EquipmentDataCreate # Union схема для обновления
)

@app.post("/cards/{card_id}/equipment", response_model=EquipmentItemRead)
async def create_equipment(
    card_id: int, 
    item_in: EquipmentItemCreate, 
    session: Annotated[AsyncSession, Depends(get_session)]
):
    db_manager = DatabaseManager(session)
    repo = EquipmentRepository(db_manager)
    
    # 1. Создаем контейнер
    item = await repo.create_item(card_id, item_in.item_type)
    
    # 2. Создаем записи данных (Баланс, Факт и т.д.)
    for data_entry in item_in.data_entries:
        await repo.add_data_entry(item.id, data_entry)
    
    # 3. Перезагружаем объект, чтобы подтянуть созданные связи для ответа
    # (Pydantic ожидает полную структуру)
    return await repo.get_item_by_id(item.id)


@app.get("/cards/{card_id}/equipment", response_model=List[EquipmentItemRead])
async def get_card_equipment(
    card_id: int, 
    session: Annotated[AsyncSession, Depends(get_session)]
):
    db_manager = DatabaseManager(session)
    repo = EquipmentRepository(db_manager)
    return await repo.get_items_by_card(card_id)


# --- НОВЫЙ ПУТЬ ДЛЯ ОБНОВЛЕНИЯ ---
# Обновляем конкретную "строчку" данных (например, Факт у трубы)
# data_id - это ID из таблицы equipment_data (не Item!)

@app.patch("/equipment-data/{data_id}") 
async def update_equipment_data(
    data_id: int,
    update_data: dict, # Или специальная схема EquipmentDataUpdate
    session: Annotated[AsyncSession, Depends(get_session)]
):
    db_manager = DatabaseManager(session)
    repo = EquipmentRepository(db_manager)
    
    # Очищаем None значения, если используем схему с Optional
    # clean_data = update_schema.model_dump(exclude_unset=True) 
    
    result = await repo.update_data_entry(data_id, **update_data)
    if not result:
        raise HTTPException(status_code=404, detail="Data entry not found")
        
    return result

app.include_router(lookups_router)
