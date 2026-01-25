from typing import Generic, TypeVar, Any
from sqlalchemy import select, func, Executable
from sqlalchemy.ext.asyncio import AsyncSession

from inventory_system.schemas.base import PaginatedResponse
from db_utils import DatabaseManager

class Paginator(Generic[T]):
    def __init__(self, manager: DatabaseManager):
        self.manager = manager

    async def paginate(
        self, 
        query: Executable, 
        page: int, 
        size: int
    ) -> dict:
        
        count_query = select(func.count()).select_from(query.order_by(None).subquery())
        total = await self.manager.session.scalar(count_query) or 0

        offset_value = (page - 1) * size
        paginated_query = query.offset(offset_value).limit(size)
        
        items = await self.manager.get_all(paginated_query, err_msg="Error retrieving page of data")
        
        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size if size > 0 else 0
        )