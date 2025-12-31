from typing import Union, Annotated

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from inventory_system.schemas import DisplayMainPageCard, CardUpdateSchema

from utils.db_utils import DatabaseManager
from database import get_session

from inventory_system.repositories.card import CardRepository

from inventory_system.routers import lookups_router

app = FastAPI()

async def return_card():
    return {
        "inventory_number": "7q947847197",
        "inventory_number_eskd": "sjkvhsjkvhjksvs",

        "gas_pipeline_section": "upper",

        "property_type": "goverment",

        # TODO Clarify what does this column in original table even mean
        "described_name": "HZ",

        # TODO Clarify what does 'OZ' mean
        "build_date_dn": "06.12.2025",

        "total_length": "35.6",

        "district": "Saltov",
        "object_name": "Test",
    }

async def get_hello_world():
    return {"Hello": "World"}

@app.get("/")
async def read_root():
    return await get_hello_world()

@app.get("/cards/{card_id}: int")
async def read_card(card_id: int):
    #TODO Actually implement this endpoint instead of test implementation
    card = await return_card()
    card["id"] = card_id
    return card

@app.post("/cards")
async def create_card(card: DisplayMainPageCard, session: Annotated[AsyncSession, Depends(get_session)]):
    db_manager = DatabaseManager(session)
    repo = CardRepository(db_manager=db_manager)
    #
    return await repo.create(**card.model_dump())

@app.patch("/cards/{card_id}: int")
async def update_card(card_id: int, new_data: CardUpdateSchema, session: Annotated[AsyncSession, Depends(get_session)]):
    db_manager = DatabaseManager(session)
    repo = CardRepository(db_manager=db_manager)
    
    update_data = new_data.model_dump(exclude_unset=True)

    updated_card = await repo.update(**update_data)

    if not updated_card:
        raise HTTPException(status_code=404, detail="Card wasn't found")
        
    return updated_card

app.include_router(lookups_router)
