from typing import Union, Annotated

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from inventory_system.schemas import DisplayMainPageCard, CardUpdateSchema

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

app.include_router(lookups_router)
