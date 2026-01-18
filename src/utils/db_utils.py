import logging
from typing import Type, TypeVar, List, Any, Sequence, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import select, Executable
from fastapi import HTTPException, status
from inventory_system.models import Base, Card


logger = logging.getLogger(__name__)
T = TypeVar("T")
ModelType = TypeVar("ModelType", bound=Base)

class DatabaseManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_record(self, model_instance: Any, err_msg: str = "Error adding record") -> Any:
        try:
            self.session.add(model_instance)
            await self.session.commit()
            await self.session.refresh(model_instance)
            return model_instance
        except SQLAlchemyError:
            await self.session.rollback()
            logger.exception(err_msg)
            raise

    async def delete_record(self, model_instance: Any, err_msg: str = "Error deleting record") -> None:
        try:
            await self.session.delete(model_instance)
            await self.session.commit()
        except IntegrityError:
            # This block catches Foreign Key violations
            await self.session.rollback()
            logger.warning(f"Integrity error during deletion: {err_msg}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot delete this record because it is currently in use by other entities."
            )
        except SQLAlchemyError:
            await self.session.rollback()
            logger.exception(err_msg)
            raise

    async def delete_record_by_id(self, model: Type[ModelType], record_id: int, err_msg: str) -> None:
        query = select(model).where(model.id == record_id)
        record = await self.get_first(query, err_msg="Error finding record for deletion")
        
        if not record:
            raise HTTPException(status_code=404, detail=f"Record with id={record_id} not found")
            
        await self.delete_record(record, err_msg=err_msg)

    async def get_first(self, query: Executable, err_msg: str = "Error executing query") -> Optional[Any]:
        try:
            result = await self.session.scalars(query)
            return result.first()
        except SQLAlchemyError:
            logger.exception(err_msg)
            raise

    async def get_all(self, query: Executable, err_msg: str = "Error fetching record list") -> Sequence[Any]:
        try:
            result = await self.session.scalars(query)
            return result.all()
        except SQLAlchemyError:
            logger.exception(err_msg)
            raise

    async def get_all_cards(self) -> List[Card]:
        query = select(Card)
        
        return await self.get_all(
            query=query, 
            err_msg=f"Error loading card table {Card.__tablename__}"
        )
    
    async def get_card(self, id: int) -> Card:
        query = select(Card).where(Card.id == id)
        card = await self.get_first(query, err_msg="Error finding card with id '{id}'")
        
        if not card:
            raise HTTPException(status_code=404, detail=f"Record with id={id} not found")
        
        return card

    async def get_all_lookups(self, model: Type[ModelType]) -> List[ModelType]:
        """
        Universal method to retrieve all records of a lookup table.
        
        Args:
            model: SQLAlchemy model class (e.g., District, PropertyType)
        """
        query = select(model).order_by(model.value)
        
        return await self.get_all(
            query=query, 
            err_msg=f"Error loading lookup table {model.__tablename__}"
        )

    async def get_all_model_records(self, model: Type[ModelType]) -> List[ModelType]:
        """
        Universal method to retrieve all records of a certain table.
        
        Args:
            model: SQLAlchemy model class (e.g., District, PropertyType)
        """
        query = select(model).order_by(model.value)
        
        return await self.get_all(
            query=query, 
            err_msg=f"Error loading lookup table {model.__tablename__}"
        )
    
    async def get_or_create_lookup(self, model: Type[ModelType], value: str, err_msg: str) -> ModelType:
        """
        Searches for a record by value. 
        - If found: returns it (does not create a duplicate).
        - If not found: creates a new one, saves and returns it.
        """
        # 1. Check existence
        query = select(model).where(model.value == value)
        result = await self.get_first(query, err_msg="Error checking existing record")
        
        if result:
            # If record exists - simply return it.
            return result
        
        # 2. If not - create new
        new_instance = model(value=value)
        return await self.add_record(new_instance, err_msg=err_msg)
    
    async def update_lookup_record(
        self, 
        model: Type[ModelType], 
        record_id: int, 
        new_value: str, 
        err_msg: str
    ) -> ModelType:
        # 1. First find record by ID
        query = select(model).where(model.id == record_id)
        record = await self.get_first(query, err_msg="Error finding record for update")
        
        if not record:
            raise HTTPException(status_code=404, detail=f"Record with id={record_id} not found")
            
        # 2. Update value
        record.value = new_value
        
        return await self.add_record(record, err_msg=err_msg)