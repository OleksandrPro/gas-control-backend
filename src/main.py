from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.cors import get_origins_list
from constants import cors_origins_str
from inventory_system.routers import lookups_router, cards_router, equipment_router, analytics_router
from inventory_system.exceptions.handlers import register_exception_handlers

app = FastAPI()

origins_list = get_origins_list(cors_origins_str)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins_list, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

app.include_router(cards_router)
app.include_router(equipment_router)
app.include_router(lookups_router)
app.include_router(analytics_router)

register_exception_handlers(app)
