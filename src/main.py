from fastapi import FastAPI
from inventory_system.routers import lookups_router, cards_router, equipment_router, analytics_router

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

app.include_router(cards_router)
app.include_router(equipment_router)
app.include_router(lookups_router)
app.include_router(analytics_router)
