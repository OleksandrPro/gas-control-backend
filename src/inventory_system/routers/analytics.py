from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from inventory_system.schemas.card import CardFilter
from inventory_system.schemas.analytics import PipeLengthStats
from inventory_system.repositories.card import CardRepository
from utils.db_utils import DatabaseManager
from database import get_session

analytics_router = APIRouter(prefix="/analytics", tags=["Analytics"])

@analytics_router.get("/pipes-length", response_model=PipeLengthStats)
async def get_pipes_length_stats(
    filter_params: Annotated[CardFilter, Depends()], 
    session: Annotated[AsyncSession, Depends(get_session)]
):
    db_manager = DatabaseManager(session)
    repo = CardRepository(db_manager)
    
    return await repo.get_pipes_length_sum(filter_params)